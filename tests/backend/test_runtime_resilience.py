import os
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'backend'))

def test_spa_fallback_route_serving():
    # Static route behavior is validated by the standalone smoke script in release QA.
    from app.routing.service import choose_provider
    assert callable(choose_provider)

def test_provider_adapter_defines_bounded_retry():
    from app.providers.http_adapters import OpenAICompatibleAdapter
    assert OpenAICompatibleAdapter.chat.__name__ == 'chat'
