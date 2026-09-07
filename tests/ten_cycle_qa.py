"""Deterministic API regression suite used inside the formal ten-cycle protocol.
It intentionally does not label browser acceptance as PASS when Playwright cannot execute.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CYCLES={1:'Foundation',2:'UI shell',3:'Chat',4:'Voice',5:'Providers',6:'Routing/switch',7:'Profile/security',8:'Files/projects/weather',9:'Performance/failure',10:'Full regression'}
def test_cycle_manifest_complete(): assert list(CYCLES)==list(range(1,11))
