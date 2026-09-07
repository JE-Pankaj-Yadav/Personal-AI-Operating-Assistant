from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def test_frontend_architecture():
    pkg=(ROOT/'frontend/package.json').read_text(); assert 'react' in pkg and 'typescript' in pkg and 'vite' in pkg
    for d in ['app','components','layouts','pages','features','hooks','services','stores','types']:
        assert (ROOT/'frontend/src'/d).is_dir()
    assert len(list((ROOT/'frontend/src').rglob('*.tsx'))) >= 8
    assert not (ROOT/'frontend/src/app.js').exists()
def test_backend_boundaries():
    for d in ['api','auth','providers','routing','usage','capsule','files','projects','weather','security','database']:
        assert (ROOT/'backend/app'/d).is_dir()
    assert (ROOT/'backend/migrations').is_dir()
