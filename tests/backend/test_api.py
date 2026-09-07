import os, tempfile
from pathlib import Path
_tmp = Path(tempfile.mkdtemp(prefix='pa_nexus_api_'))
os.environ['DATABASE_URL'] = f"sqlite:///{(_tmp/'test_api.db').as_posix()}"
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base,engine
Base.metadata.drop_all(engine); Base.metadata.create_all(engine)

def test_register_login_chat_provider():
    c=TestClient(app)
    r=c.post('/api/auth/register',json={'email':'qa@example.com','username':'qa','display_name':'QA User','password':'StrongPassword123!'})
    assert r.status_code==200
    r=c.get('/api/providers'); assert r.status_code==200 and not any(p['provider_type']=='mock' for p in r.json())
    r=c.post('/api/providers',json={'company':'Mock','provider_type':'mock','display_name':'Mock','model':'jarvis-mock-1','api_key':'not-secret-returned','capabilities':['text','code']})
    assert r.status_code==422
    r=c.post('/api/chat/message',json={'content':'Hello from the QA test'})
    assert r.status_code==503
    r=c.get('/api/conversations?type=chat'); assert len(r.json())==1 and r.json()[0]['title'].startswith('Hello')
    assert c.get('/api/control-center').status_code==200

def test_provider_test_after_delete_is_controlled_not_500():
    c=TestClient(app)
    r=c.post('/api/auth/register',json={'email':'race2@example.com','username':'race2','display_name':'Race QA 2','password':'StrongPassword123!'})
    assert r.status_code==200
    providers=c.get('/api/providers').json()
    pid=c.post('/api/providers',json={'company':'NVIDIA','provider_type':'nvidia','display_name':'NVIDIA QA','model':'meta/llama-3.1-8b-instruct','api_key':'secret','capabilities':['text','code']}).json()['id']
    assert c.delete(f'/api/providers/{pid}').status_code==200
    # A stale Test Connection click must be handled as a normal not-found response,
    # not as SQLAlchemy StaleDataError/PendingRollbackError/HTTP 500.
    r=c.post(f'/api/providers/{pid}/test')
    assert r.status_code==404
    # The same session/client remains usable after the controlled error.
    r=c.post('/api/providers',json={'company':'NVIDIA','provider_type':'nvidia','display_name':'NVIDIA QA 2','model':'meta/llama-3.1-8b-instruct','api_key':'secret'})
    assert r.status_code==200
    # Network access is not required for this regression; the important contract is that
    # the test endpoint returns a controlled provider result rather than a SQLAlchemy 500.
    r=c.post(f"/api/providers/{r.json()['id']}/test")
    assert r.status_code==200 and r.json()['status'] in {'healthy','unhealthy','error'}


def test_chat_success_returns_response_without_fallback_name_error(monkeypatch):
    from app import main as main_module
    from app.database import SessionLocal
    from app.models import Provider
    from app.providers.base import ProviderResult

    class FakeAdapter:
        async def chat(self, model, credential, messages, base_url=None):
            return ProviderResult(text='Hello! I am ready.', provider='NVIDIA', model=model, usage=7, usage_source='exact')

    c=TestClient(app)
    r=c.post('/api/auth/register',json={'email':'chatok@example.com','username':'chatok','display_name':'Chat OK','password':'StrongPassword123!'})
    assert r.status_code==200
    pid=c.post('/api/providers',json={'company':'NVIDIA','provider_type':'nvidia','display_name':'NVIDIA Chat QA','model':'meta/llama-3.1-8b-instruct','api_key':'secret','capabilities':['text','code']}).json()['id']
    db=SessionLocal()
    try:
        provider=db.query(Provider).filter(Provider.id==pid).first()
        provider.health='HEALTHY'
        db.commit()
    finally:
        db.close()
    monkeypatch.setattr(main_module, 'adapter_for', lambda provider_type: FakeAdapter())
    r=c.post('/api/chat/message',json={'content':'hello'})
    assert r.status_code==200
    body=r.json()
    assert body['message']=='Hello! I am ready.'
    assert body['fallback_reason'] is None
    assert body['user_message_id'] > 0
    assert body['message_id'] > 0
