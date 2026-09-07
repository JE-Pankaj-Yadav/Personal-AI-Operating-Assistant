import os, tempfile
from pathlib import Path
_tmp = Path(tempfile.mkdtemp(prefix='pa_nexus_workflows_'))
os.environ['DATABASE_URL'] = f"sqlite:///{(_tmp/'test_workflows.db').as_posix()}"
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base,engine
Base.metadata.drop_all(engine); Base.metadata.create_all(engine)

def client(): return TestClient(app)

def test_separate_histories_profile_upload_and_secret_mask():
    c=client(); assert c.post('/api/auth/register',json={'email':'p@example.com','username':'p','display_name':'Pankaj','password':'StrongPassword123!'}).status_code==200
    chat=c.post('/api/conversations',json={'conversation_type':'chat'}).json(); voice=c.post('/api/conversations',json={'conversation_type':'voice'}).json()
    assert chat['conversation_type']=='chat' and voice['conversation_type']=='voice'
    p=c.post('/api/providers',json={'company':'NVIDIA','provider_type':'nvidia','display_name':'NVIDIA NIM','model':'meta/llama-3.1-8b-instruct','api_key':'super-secret','capabilities':['text','code']}).json()
    assert 'super-secret' not in str(p) and p['base_url']=='https://integrate.api.nvidia.com/v1'
    assert c.get('/api/providers').status_code==200
    prof=c.patch('/api/profile',json={'display_name':'Updated','email':'p@example.com','timezone':'Asia/Kolkata','language':'en','theme':'dark'}).json(); assert prof['display_name']=='Updated'
    assert c.get('/api/conversations?type=chat').json()[0]['conversation_type']=='chat'
    assert all(x['conversation_type']=='voice' for x in c.get('/api/conversations?type=voice').json())
    assert c.get('/api/telemetry').status_code==200
    assert c.get('/api/weather').status_code==200
