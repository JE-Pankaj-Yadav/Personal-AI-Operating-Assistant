from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def test_no_real_env_or_credentials():
    assert not (ROOT/'.env').exists()
    for p in ROOT.rglob('*'):
        if p.is_file() and p != Path(__file__) and p.suffix in {'.py','.ts','.tsx','.json','.md','.txt','.bat','.ps1','.sh'}:
            s=p.read_text(errors='ignore').lower()
            assert 'nvapi-' not in s and 'sk-' not in s

def test_release_excludes_caches():
    assert not (ROOT/'node_modules').exists()
    assert not (ROOT/'.venv').exists()
