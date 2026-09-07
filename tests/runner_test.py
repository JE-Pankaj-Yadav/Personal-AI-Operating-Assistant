from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_runners_resolve_their_own_root():
    for f in ['run.bat','run.ps1','run.sh']:
        assert (ROOT/f).exists()
    ps=(ROOT/'run.ps1').read_text(); sh=(ROOT/'run.sh').read_text()
    assert '$PSScriptRoot' in ps and 'BASH_SOURCE' in sh

def test_canonical_db_path():
    s=(ROOT/'backend/app/config/settings.py').read_text(); assert 'Path(__file__).resolve()' in s and 'pa_nexus.db' in s
