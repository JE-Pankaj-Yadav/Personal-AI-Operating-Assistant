from dataclasses import dataclass
from typing import AsyncIterator
@dataclass
class ProviderResult:
    text: str
    provider: str
    model: str
    usage: int|None=None
    usage_source: str='estimated'
class ProviderAdapter:
    name='base'
    async def health_check(self, model, credential, base_url=None): raise NotImplementedError
    async def list_models(self, credential, base_url=None): return []
    async def chat(self, model, credential, messages, base_url=None): raise NotImplementedError
    async def stream(self, model, credential, messages, base_url=None) -> AsyncIterator[str]:
        r=await self.chat(model,credential,messages,base_url); yield r.text
    def capabilities(self, model): return ['text','code']
    def normalize_error(self,e): return {'category':'provider_unavailable','message':str(e)}
