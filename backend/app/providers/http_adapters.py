import asyncio
import logging
import httpx
from .base import ProviderAdapter, ProviderResult

logger = logging.getLogger('pa_nexus.providers')


def _error_detail(response: httpx.Response) -> str:
    try:
        body = response.json()
        if isinstance(body, dict):
            err = body.get('error')
            if isinstance(err, dict):
                detail = err.get('message') or err.get('detail') or err.get('code')
                if detail:
                    return str(detail)[:500]
            for key in ('message', 'detail', 'error'):
                value = body.get(key)
                if isinstance(value, str) and value:
                    return value[:500]
        text = response.text.strip()
        return text[:500] if text else f'HTTP {response.status_code}'
    except Exception:
        text = response.text.strip()
        return text[:500] if text else f'HTTP {response.status_code}'


class OpenAICompatibleAdapter(ProviderAdapter):
    name = 'openai-compatible'

    def __init__(self, provider_type: str = 'custom'):
        self.provider_type = provider_type

    def capabilities(self, model):
        return ['text', 'code', 'structured']

    def _url(self, base_url: str | None) -> str:
        base = (base_url or 'https://api.openai.com/v1').rstrip('/')
        return base if base.endswith('/chat/completions') else base + '/chat/completions'

    def _headers(self, credential: str | None) -> dict[str, str]:
        return {
            'Authorization': f'Bearer {credential}' if credential else '',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def _payload(self, model: str, messages: list[dict], *, health: bool = False) -> dict:
        # Keep health probes and real chat requests on the same API contract.
        # Some current OpenAI reasoning models use max_completion_tokens instead
        # of max_tokens, while Gemini/NVIDIA/OpenAI-compatible models accept
        # max_tokens.  The chat method can retry the OpenAI variant when needed.
        payload = {
            'model': model,
            'messages': messages,
            'stream': False,
        }
        # Google's OpenAI compatibility layer accepts the core chat schema; keep
        # the Gemini request minimal to avoid translating provider-specific
        # generation parameters that may differ between model generations.
        if self.provider_type == 'gemini':
            return payload
        if self.provider_type == 'nvidia':
            # Nemotron 3 Ultra is a frontier reasoning model. NVIDIA documents
            # reasoning_effort={none,medium,high}; disabling reasoning for the
            # health probe prevents a credential check from waiting on a full
            # reasoning trace. Normal chat uses medium effort for responsive
            # interactive use.
            payload['max_tokens'] = 32 if health else 4096
            payload['temperature'] = 0.2 if health else 0.7
            payload['reasoning_effort'] = 'none' if health else 'medium'
            return payload
        if self.provider_type == 'openai' and any(model.lower().startswith(prefix) for prefix in ('gpt-5', 'o1', 'o3', 'o4')):
            payload['max_completion_tokens'] = 16 if health else 2048
        else:
            payload['max_tokens'] = 16 if health else 2048
            payload['temperature'] = 0.2
        return payload

    async def _poll_nvidia(self, base_url: str, headers: dict[str, str], request_id: str, timeout: httpx.Timeout) -> httpx.Response:
        # NVIDIA NIM can return 202 for long-running inference and exposes the
        # completed result at /status/{requestId}. Without this polling a valid
        # key/model can be reported as a failed chat even though the invocation
        # is still running.
        status_url = base_url.rstrip('/') + f'/status/{request_id}'
        deadline = asyncio.get_running_loop().time() + min(timeout.read or 180.0, 180.0)
        async with httpx.AsyncClient(timeout=httpx.Timeout(20.0, connect=10.0)) as client:
            while asyncio.get_running_loop().time() < deadline:
                response = await client.get(status_url, headers=headers)
                if response.status_code != 202:
                    return response
                await asyncio.sleep(1.0)
        raise httpx.ReadTimeout('NVIDIA invocation remained pending until the polling deadline.')

    async def health_check(self, model, credential, base_url=None):
        base = (base_url or 'https://api.openai.com/v1').rstrip('/')
        url = base + '/chat/completions'
        headers = self._headers(credential)
        timeout = httpx.Timeout(180.0 if self.provider_type == 'nvidia' else 60.0, connect=15.0)
        payload = self._payload(model, [{'role': 'user', 'content': 'Reply with OK in one short word.'}], health=True)
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(url, headers=headers, json=payload)
            request_id = response.headers.get('x-request-id') or response.headers.get('request-id') or ''
            if self.provider_type == 'nvidia' and response.status_code == 202:
                try:
                    pending = response.json()
                    request_id = request_id or str(pending.get('requestId') or pending.get('request_id') or '')
                except Exception:
                    pending = {}
                if request_id:
                    response = await self._poll_nvidia(base, headers, request_id, timeout)
            detail = '' if 200 <= response.status_code < 300 else _error_detail(response)
            healthy = 200 <= response.status_code < 300
            logger.info('[PROVIDER TEST] provider=%s model=%s status=%s request_id=%s error=%s', self.provider_type, model, response.status_code, request_id or '-', detail or '-')
            return {
                'healthy': healthy,
                'status': response.status_code,
                'latency_ms': None,
                'request_id': request_id,
                'error': detail,
                'category': 'ok' if healthy else self._status_category(response.status_code),
            }
        except httpx.RequestError as exc:
            detail = self._request_error(exc)
            logger.error('[PROVIDER TEST] provider=%s model=%s network_error=%s', self.provider_type, model, detail)
            return {'healthy': False, 'status': None, 'latency_ms': None, 'request_id': '', 'error': detail, 'category': 'network'}
        except Exception as exc:
            detail = str(exc)[:500]
            logger.exception('[PROVIDER TEST] provider=%s model=%s unexpected_error=%s', self.provider_type, model, detail)
            return {'healthy': False, 'status': None, 'latency_ms': None, 'request_id': '', 'error': detail, 'category': 'unexpected'}

    @staticmethod
    def _status_category(status: int) -> str:
        if status in {401, 403}:
            return 'authentication'
        if status == 404:
            return 'model_or_endpoint'
        if status == 429:
            return 'rate_limit_or_quota'
        if 400 <= status < 500:
            return 'request_rejected'
        if status >= 500:
            return 'provider_server_error'
        return 'provider_error'

    @staticmethod
    def _request_error(exc: Exception) -> str:
        if isinstance(exc, httpx.TimeoutException):
            return 'Provider request timed out. The model may be slow; retry or use a faster model.'
        return str(exc)[:500]

    async def _post_chat(self, url: str, headers: dict[str, str], payload: dict, timeout: httpx.Timeout) -> httpx.Response:
        async with httpx.AsyncClient(timeout=timeout) as client:
            return await client.post(url, headers=headers, json=payload)

    async def chat(self, model, credential, messages, base_url=None):
        url = self._url(base_url)
        headers = self._headers(credential)
        timeout = httpx.Timeout(180.0 if self.provider_type == 'nvidia' else 90.0, connect=15.0)
        payload = self._payload(model, messages)
        last_error = None

        for attempt in range(2):
            try:
                response = await self._post_chat(url, headers, payload, timeout)
                request_id = response.headers.get('x-request-id') or response.headers.get('request-id') or '-'
                if self.provider_type == 'nvidia' and response.status_code == 202:
                    try:
                        pending = response.json()
                        request_id = request_id if request_id != '-' else str(pending.get('requestId') or pending.get('request_id') or '-')
                    except Exception:
                        pending = {}
                    if request_id != '-':
                        response = await self._poll_nvidia((base_url or 'https://integrate.api.nvidia.com/v1'), headers, request_id, timeout)
                logger.info('[PROVIDER CHAT] provider=%s model=%s status=%s request_id=%s attempt=%s', self.provider_type, model, response.status_code, request_id, attempt + 1)

                # A few OpenAI models reject max_tokens. Retry once with the
                # modern parameter instead of incorrectly declaring the provider dead.
                if response.status_code == 400 and self.provider_type == 'openai' and 'max_tokens' in payload:
                    detail = _error_detail(response).lower()
                    if 'max_tokens' in detail and ('unsupported' in detail or 'not supported' in detail or 'max_completion_tokens' in detail):
                        payload.pop('max_tokens', None)
                        payload.pop('temperature', None)
                        payload['max_completion_tokens'] = 2048
                        continue

                if response.status_code in {408, 429, 500, 502, 503, 504} and attempt == 0:
                    await asyncio.sleep(0.75)
                    continue

                if not 200 <= response.status_code < 300:
                    detail = _error_detail(response)
                    category = self._status_category(response.status_code)
                    logger.error('[PROVIDER CHAT ERROR] provider=%s model=%s status=%s category=%s request_id=%s error=%s', self.provider_type, model, response.status_code, category, request_id, detail)
                    raise RuntimeError(f'HTTP {response.status_code} [{category}] {detail}')

                data = response.json()
                choices = data.get('choices') or []
                if not choices:
                    raise RuntimeError('Provider returned no choices')
                message = choices[0].get('message') or {}
                text = message.get('content')
                if isinstance(text, list):
                    text = ''.join(str(part.get('text', '')) for part in text if isinstance(part, dict))
                if not text:
                    # Some reasoning responses may place visible output in a
                    # secondary field. Use it only when present; never fabricate text.
                    text = message.get('reasoning_content') or choices[0].get('text')
                if not text:
                    raise RuntimeError('Provider returned an empty response')
                usage = (data.get('usage') or {}).get('total_tokens')
                return ProviderResult(str(text), self.name, model, usage, 'exact' if usage is not None else 'estimated')
            except httpx.RequestError as exc:
                last_error = RuntimeError(self._request_error(exc))
                logger.error('[PROVIDER CHAT ERROR] provider=%s model=%s network_error=%s attempt=%s', self.provider_type, model, last_error, attempt + 1)
                if attempt == 0:
                    await asyncio.sleep(0.75)
                    continue
                raise last_error from exc

        raise last_error or RuntimeError('AI provider request failed')


class AnthropicAdapter(ProviderAdapter):
    name = 'anthropic'

    def _url(self, base_url: str | None) -> str:
        base = (base_url or 'https://api.anthropic.com/v1').rstrip('/')
        return base if base.endswith('/messages') else base + '/messages'

    def _headers(self, credential: str | None) -> dict[str, str]:
        return {
            'x-api-key': credential or '',
            'anthropic-version': '2023-06-01',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    @staticmethod
    def _messages(messages):
        system = []
        normal = []
        for item in messages:
            role = item.get('role')
            content = item.get('content', '')
            if role == 'system':
                system.append(content)
            elif role in {'user', 'assistant'}:
                normal.append({'role': role, 'content': content})
        return system, normal

    async def health_check(self, model, credential, base_url=None):
        url = self._url(base_url)
        headers = self._headers(credential)
        payload = {'model': model, 'max_tokens': 16, 'messages': [{'role': 'user', 'content': 'Reply with OK in one short word.'}]}
        timeout = httpx.Timeout(60.0, connect=10.0)
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(url, headers=headers, json=payload)
            request_id = response.headers.get('request-id') or response.headers.get('x-request-id') or ''
            detail = '' if 200 <= response.status_code < 300 else _error_detail(response)
            healthy = 200 <= response.status_code < 300
            if healthy:
                try:
                    data = response.json()
                    text = ''.join(str(x.get('text', '')) for x in (data.get('content') or []) if isinstance(x, dict))
                    if not text:
                        healthy = False
                        detail = 'Anthropic returned HTTP 200 but no text content.'
                except Exception:
                    healthy = False
                    detail = 'Anthropic returned an invalid JSON response.'
            logger.info('[PROVIDER TEST] provider=anthropic model=%s status=%s request_id=%s error=%s', model, response.status_code, request_id or '-', detail or '-')
            return {'healthy': healthy, 'status': response.status_code, 'latency_ms': None, 'request_id': request_id, 'error': detail, 'category': 'ok' if healthy else ('authentication' if response.status_code in {401,403} else 'provider_error')}
        except httpx.RequestError as exc:
            detail = OpenAICompatibleAdapter._request_error(exc)
            logger.error('[PROVIDER TEST] provider=anthropic model=%s network_error=%s', model, detail)
            return {'healthy': False, 'status': None, 'request_id': '', 'error': detail, 'category': 'network'}

    async def chat(self, model, credential, messages, base_url=None):
        system, normal = self._messages(messages)
        payload = {'model': model, 'max_tokens': 2048, 'messages': normal}
        if system:
            payload['system'] = '\n\n'.join(str(x) for x in system)
        url = self._url(base_url)
        headers = self._headers(credential)
        timeout = httpx.Timeout(90.0, connect=10.0)
        for attempt in range(2):
            try:
                async with httpx.AsyncClient(timeout=timeout) as client:
                    response = await client.post(url, headers=headers, json=payload)
                request_id = response.headers.get('request-id') or response.headers.get('x-request-id') or '-'
                logger.info('[PROVIDER CHAT] provider=anthropic model=%s status=%s request_id=%s attempt=%s', model, response.status_code, request_id, attempt + 1)
                if response.status_code in {408,429,500,502,503,504} and attempt == 0:
                    await asyncio.sleep(0.75)
                    continue
                if not 200 <= response.status_code < 300:
                    detail = _error_detail(response)
                    category = OpenAICompatibleAdapter._status_category(response.status_code)
                    logger.error('[PROVIDER CHAT ERROR] provider=anthropic model=%s status=%s category=%s request_id=%s error=%s', model, response.status_code, category, request_id, detail)
                    raise RuntimeError(f'HTTP {response.status_code} [{category}] {detail}')
                data = response.json()
                text = ''.join(str(x.get('text', '')) for x in (data.get('content') or []) if isinstance(x, dict) and x.get('type') == 'text')
                if not text:
                    raise RuntimeError('Anthropic returned an empty response')
                usage_data = data.get('usage') or {}
                usage = (usage_data.get('input_tokens') or 0) + (usage_data.get('output_tokens') or 0)
                return ProviderResult(text, self.name, model, usage or None, 'exact' if usage else 'estimated')
            except httpx.RequestError as exc:
                detail = OpenAICompatibleAdapter._request_error(exc)
                logger.error('[PROVIDER CHAT ERROR] provider=anthropic model=%s network_error=%s attempt=%s', model, detail, attempt + 1)
                if attempt == 0:
                    await asyncio.sleep(0.75)
                    continue
                raise RuntimeError(detail) from exc
        raise RuntimeError('Anthropic request failed')
