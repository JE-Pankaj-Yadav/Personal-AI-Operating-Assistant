import asyncio
import httpx
from app.providers.http_adapters import AnthropicAdapter, OpenAICompatibleAdapter


class FakeResponse:
    def __init__(self, status_code, body, headers=None):
        self.status_code = status_code
        self._body = body
        self.headers = headers or {}
        self.text = str(body)
    def json(self):
        return self._body


class FakeClient:
    response = None
    requests = []
    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs
    async def __aenter__(self): return self
    async def __aexit__(self, *args): pass
    async def post(self, url, headers=None, json=None):
        self.__class__.requests.append((url, headers, json))
        return self.__class__.response


def test_gemini_compatible_payload_and_health(monkeypatch):
    FakeClient.requests = []
    FakeClient.response = FakeResponse(200, {'choices':[{'message':{'content':'OK'}}]}, {'x-request-id':'g-1'})
    monkeypatch.setattr(httpx, 'AsyncClient', FakeClient)
    adapter = OpenAICompatibleAdapter('gemini')
    result = asyncio.run(adapter.health_check('gemini-3.8-flash', 'gem-key', 'https://generativelanguage.googleapis.com/v1beta/openai'))
    assert result['healthy'] is True
    url, headers, body = FakeClient.requests[-1]
    assert url.endswith('/chat/completions')
    assert headers['Authorization'] == 'Bearer gem-key'
    assert body['model'] == 'gemini-3.8-flash'
    assert 'max_tokens' not in body
    assert 'temperature' not in body


def test_openai_reasoning_models_use_modern_token_parameter(monkeypatch):
    FakeClient.requests = []
    FakeClient.response = FakeResponse(200, {'choices':[{'message':{'content':'OK'}}]}, {'x-request-id':'o-1'})
    monkeypatch.setattr(httpx, 'AsyncClient', FakeClient)
    adapter = OpenAICompatibleAdapter('openai')
    result = asyncio.run(adapter.health_check('gpt-5.2', 'key', 'https://api.openai.com/v1'))
    assert result['healthy'] is True
    body = FakeClient.requests[-1][2]
    assert body['max_completion_tokens'] == 16
    assert 'temperature' not in body


def test_anthropic_uses_native_messages_contract(monkeypatch):
    FakeClient.requests = []
    FakeClient.response = FakeResponse(200, {'content':[{'type':'text','text':'OK'}], 'usage':{'input_tokens':2,'output_tokens':1}}, {'request-id':'a-1'})
    monkeypatch.setattr(httpx, 'AsyncClient', FakeClient)
    adapter = AnthropicAdapter()
    result = asyncio.run(adapter.health_check('claude-sonnet-4-5', 'a-key', 'https://api.anthropic.com/v1'))
    assert result['healthy'] is True
    url, headers, body = FakeClient.requests[-1]
    assert url.endswith('/messages')
    assert headers['x-api-key'] == 'a-key'
    assert headers['anthropic-version'] == '2023-06-01'
    assert body['max_tokens'] == 16
    assert body['messages'][0]['role'] == 'user'


def test_nvidia_health_probe_disables_reasoning_and_uses_short_generation(monkeypatch):
    FakeClient.requests = []
    FakeClient.response = FakeResponse(200, {'choices':[{'message':{'content':'OK'}}]}, {'request-id':'n-1'})
    monkeypatch.setattr(httpx, 'AsyncClient', FakeClient)
    adapter = OpenAICompatibleAdapter('nvidia')
    result = asyncio.run(adapter.health_check('nvidia/nemotron-3-ultra-550b-a55b', 'n-key', 'https://integrate.api.nvidia.com/v1'))
    assert result['healthy'] is True
    body = FakeClient.requests[-1][2]
    assert body['max_tokens'] == 32
    assert body['reasoning_effort'] == 'none'


def test_nvidia_202_result_is_polled(monkeypatch):
    calls = []
    class PollClient(FakeClient):
        async def post(self, url, headers=None, json=None):
            calls.append(('post', url))
            return FakeResponse(202, {'requestId':'req-123'}, {})
        async def get(self, url, headers=None):
            calls.append(('get', url))
            return FakeResponse(200, {'choices':[{'message':{'content':'OK'}}]}, {'request-id':'req-123'})
    monkeypatch.setattr(httpx, 'AsyncClient', PollClient)
    adapter = OpenAICompatibleAdapter('nvidia')
    result = asyncio.run(adapter.health_check('nvidia/nemotron-3-ultra-550b-a55b', 'n-key', 'https://integrate.api.nvidia.com/v1'))
    assert result['healthy'] is True
    assert any(kind == 'get' and url.endswith('/status/req-123') for kind, url in calls)
