from .http_adapters import AnthropicAdapter, OpenAICompatibleAdapter

DEFAULT_BASE_URLS = {
    'openai': 'https://api.openai.com/v1',
    'nvidia': 'https://integrate.api.nvidia.com/v1',
    'gemini': 'https://generativelanguage.googleapis.com/v1beta/openai',
    'anthropic': 'https://api.anthropic.com/v1',
}


def default_base_url(provider_type: str) -> str | None:
    return DEFAULT_BASE_URLS.get(provider_type)


def adapter_for(provider_type):
    # NVIDIA and Gemini expose OpenAI-compatible chat-completions endpoints.
    # Anthropic is intentionally not silently treated as native Anthropic here;
    # the current UI's endpoint contract is OpenAI-compatible/custom. Keeping
    # the provider type in the adapter allows diagnostics and future native
    # adapters without losing the selected company.
    if provider_type == 'anthropic':
        return AnthropicAdapter()
    return OpenAICompatibleAdapter(provider_type)
