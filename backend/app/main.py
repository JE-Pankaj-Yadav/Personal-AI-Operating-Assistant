from pathlib import Path
import time,uuid, mimetypes, re, urllib.parse, logging
from fastapi import FastAPI,Depends,Request,Response,HTTPException,UploadFile,File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel,EmailStr
from sqlalchemy.orm import Session as OrmSession
from sqlalchemy import func
from sqlalchemy.orm.exc import StaleDataError
from .database import get_db
from .config.settings import settings,ROOT,UPLOAD_DIR,DB_PATH
from .models import *
from .auth.service import get_current_user,login,register
from .security import encrypt_secret, hash_token, verify_password, hash_password
from .providers.registry import adapter_for, default_base_url
from .routing.service import choose_provider,ensure_capsule

app=FastAPI(title='PA NEXUS API',version='3.0.14')
logger=logging.getLogger('pa_nexus')
_weather_cache:dict[int,tuple[float,dict]]={}
_WEATHER_CACHE_TTL=60
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origins,allow_credentials=True,allow_methods=['*'],allow_headers=['*'])

class LoginIn(BaseModel): email:EmailStr; password:str
class RegisterIn(BaseModel): email:EmailStr; username:str; display_name:str; password:str
class MessageIn(BaseModel): conversation_id:int|None=None; content:str
class ProviderIn(BaseModel): company:str; provider_type:str; display_name:str; model:str; api_key:str|None=None; base_url:str|None=None; capabilities:list[str]=['text','code']; context_window:int=128000
class ProfileIn(BaseModel): display_name:str; email:EmailStr; timezone:str; language:str; theme:str
class WeatherIn(BaseModel): provider:str='openweather'; location:str='Quezon City, PH'; units:str='metric'; api_key:str|None=None
class PasswordIn(BaseModel): current_password:str; new_password:str; confirm_password:str
class OtpRequestIn(BaseModel): email:EmailStr
class OtpVerifyIn(BaseModel): email:EmailStr; otp:str
class ResetPasswordIn(BaseModel): email:EmailStr; otp:str; new_password:str; confirm_password:str

@app.get('/api/health')
def health(db:OrmSession=Depends(get_db)): return {'status':'ok','database':'ok' if DB_PATH.exists() else 'ready','version':app.version}
@app.post('/api/auth/register')
def reg(payload:RegisterIn,response:Response,db:OrmSession=Depends(get_db)):
    u=register(db,payload.email,payload.username,payload.display_name,payload.password); user,token=login(db,payload.email,payload.password); response.set_cookie('pa_session',token,httponly=True,samesite='lax',secure=False,max_age=86400); return {'user':user_out(user)}
@app.post('/api/auth/login')
def log(payload:LoginIn,response:Response,db:OrmSession=Depends(get_db)):
    u,token=login(db,payload.email,payload.password); response.set_cookie('pa_session',token,httponly=True,samesite='lax',secure=False,max_age=86400); return {'user':user_out(u)}
@app.post('/api/auth/logout')
def logout(request:Request,response:Response,db:OrmSession=Depends(get_db)):
    raw=request.cookies.get('pa_session')
    if raw:
        s=db.query(DbSession).filter(DbSession.token_hash==hash_token(raw)).first()
        if s: db.delete(s); db.commit()
    response.delete_cookie('pa_session'); return {'ok':True}
@app.get('/api/auth/me')
def me(request:Request,db:OrmSession=Depends(get_db)): return {'user':user_out(get_current_user(request,db))}
def user_out(u): return {'id':u.id,'email':u.email,'username':u.username,'display_name':u.display_name,'timezone':u.timezone,'language':u.language,'theme':u.theme,'avatar_path':u.avatar_path}

@app.get('/api/conversations')
def conversations(type:str='chat',request:Request=None,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db); rows=db.query(Conversation).filter(Conversation.user_id==u.id,Conversation.conversation_type==type,Conversation.archived==False).order_by(Conversation.updated_at.desc()).all()
    changed=False
    for x in rows:
        normalized=normalize_saved_title(x.title)
        if x.title != normalized: x.title=normalized; changed=True
    if changed: db.commit()
    return [conv_out(x) for x in rows]
DEFAULT_CONVERSATION_TITLE = 'New Conversation — J.A.R.V.I.S'

def make_title(text:str) -> str:
    cleaned=re.sub(r"\s+", " ", re.sub(r"[`*_#~]+", "", text)).strip()
    words=cleaned.split()
    title=" ".join(words[:10])
    if len(words)>10: title += "…"
    if not title: title=DEFAULT_CONVERSATION_TITLE
    if len(title)<20:
        suffix=' — Conversation'
        title=(title + suffix)[:70]
    return title[:70]

def normalize_saved_title(title:str|None) -> str:
    cleaned=re.sub(r"\s+", " ", re.sub(r"[`*_#~]+", "", title or "")).strip()
    if not cleaned or cleaned == 'New Conversation': return DEFAULT_CONVERSATION_TITLE
    if len(cleaned)<20: cleaned=(cleaned + ' — J.A.R.V.I.S Conversation')[:70]
    return cleaned[:70]

def conv_out(c): return {'id':c.id,'title':normalize_saved_title(c.title),'conversation_type':c.conversation_type,'created_at':c.created_at.isoformat(),'updated_at':c.updated_at.isoformat(),'archived':c.archived}

@app.post('/api/conversations')
def create_conv(payload:dict,request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db); typ=payload.get('conversation_type','chat'); c=Conversation(user_id=u.id,conversation_type=typ,title=normalize_saved_title(payload.get('title',DEFAULT_CONVERSATION_TITLE))); db.add(c); db.commit(); db.refresh(c); return conv_out(c)
@app.get('/api/conversations/{cid}/messages')
def msgs(cid:int,request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db); c=db.query(Conversation).filter(Conversation.id==cid,Conversation.user_id==u.id).first()
    if not c: raise HTTPException(404,'Conversation not found')
    return [msg_out(m) for m in db.query(Message).filter(Message.conversation_id==cid).order_by(Message.created_at).all()]
def msg_out(m): return {'id':m.id,'role':m.role,'content':m.content,'provider':m.provider,'model':m.model,'feedback':m.feedback,'created_at':m.created_at.isoformat()}
@app.post('/api/messages/{mid}/feedback')
def message_feedback(mid:int,payload:dict,request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db); m=db.query(Message).join(Conversation,Message.conversation_id==Conversation.id).filter(Message.id==mid,Conversation.user_id==u.id).first()
    if not m: raise HTTPException(404,'Message not found')
    value=payload.get('feedback')
    if value not in {'like','dislike','none'}: raise HTTPException(422,'Feedback must be like, dislike or none')
    m.feedback=None if value=='none' else value; db.commit(); return {'ok':True,'feedback':m.feedback}

def _purge_legacy_mock_providers(db:OrmSession,user_id:int):
    legacy=db.query(Provider).filter(
        Provider.user_id==user_id,
        Provider.provider_type=='mock',
        Provider.model=='jarvis-mock-1'
    ).all()
    if not legacy:
        return
    for provider in legacy:
        db.delete(provider)
    db.commit()


@app.post('/api/chat/message')
async def chat(payload:MessageIn,request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db); content=payload.content.strip()
    if not content: raise HTTPException(422,'Message cannot be empty')
    c=db.query(Conversation).filter(Conversation.id==payload.conversation_id,Conversation.user_id==u.id).first() if payload.conversation_id else None
    if not c:
        c=Conversation(user_id=u.id,conversation_type='chat',title=make_title(content)); db.add(c); db.commit(); db.refresh(c)
    elif normalize_saved_title(c.title) == DEFAULT_CONVERSATION_TITLE:
        c.title=make_title(content)
    user_msg=Message(conversation_id=c.id,role='user',content=content); db.add(user_msg); db.commit(); db.refresh(user_msg)
    _purge_legacy_mock_providers(db,u.id)
    provider=choose_provider(db,u.id,c.id,['text'])
    if not provider:
        raise HTTPException(503,'No healthy configured AI provider is available. Open AI Providers, test a provider successfully, and try again.')
    history=[{'role':m.role,'content':m.content} for m in db.query(Message).filter(Message.conversation_id==c.id).order_by(Message.created_at).all()]
    ensure_capsule(db,c.id,content)
    provider_attempts=[]
    fallback_reason=None
    result=None
    while provider:
        provider_attempts.append(provider.id)
        adapter=adapter_for(provider.provider_type); base_url=provider.base_url or default_base_url(provider.provider_type); credential=None
        if provider.encrypted_credential:
            from .security import decrypt_secret
            credential=decrypt_secret(provider.encrypted_credential)
        try:
            result=await adapter.chat(provider.model,credential,history,base_url)
            break
        except Exception as exc:
            error_text=str(exc)[:500]
            # Authentication/model/request errors mean this exact configuration
            # is not usable and should be removed from active routing. Transient
            # 429/5xx/timeouts are not permanent credential failures; keep the
            # provider healthy so a later request can recover automatically.
            permanent = any(token in error_text for token in ('HTTP 400 [authentication]', 'HTTP 401 [', 'HTTP 403 [', 'HTTP 404 [', 'HTTP 422 [', '[model_or_endpoint]', '[authentication]', '[request_rejected]'))
            if permanent:
                provider.health='UNHEALTHY'
            provider.last_tested_at=now()
            db.commit()
            logger.error('[CHAT PROVIDER FAILURE] user=%s provider=%s model=%s permanent=%s error=%s', u.id, provider.company, provider.model, permanent, error_text)
            fallback_reason = f'{provider.company} / {provider.model} failed: {error_text}. Attempting the next configured provider.'
            remaining=db.query(Provider).filter(Provider.user_id==u.id,Provider.enabled==True,Provider.id.notin_(provider_attempts)).order_by(Provider.preferred.desc(),Provider.priority.asc()).all()
            provider=next((candidate for candidate in remaining if candidate.health=='HEALTHY' and set(candidate.capabilities or ['text']).issuperset({'text'})),None)
    if result is None or provider is None:
        detail = fallback_reason or 'No configured provider completed the request.'
        raise HTTPException(503,f'All configured AI providers are currently unavailable. {detail}')
    assistant_msg=Message(conversation_id=c.id,role='assistant',content=result.text,provider=provider.company,model=provider.model); db.add(assistant_msg); c.updated_at=now()
    usage_row=db.query(ProviderUsage).filter(ProviderUsage.user_id==u.id,ProviderUsage.provider_id==provider.id).first()
    if not usage_row: usage_row=ProviderUsage(user_id=u.id,provider_id=provider.id,total_tokens=0,requests=0,exact_tokens=0,estimated_tokens=0); db.add(usage_row)
    used=int(result.usage or 0); usage_row.total_tokens=(usage_row.total_tokens or 0)+used; usage_row.requests=(usage_row.requests or 0)+1
    if result.usage_source == 'exact': usage_row.exact_tokens=(usage_row.exact_tokens or 0)+used
    else: usage_row.estimated_tokens=(usage_row.estimated_tokens or 0)+used
    usage_row.updated_at=now(); db.commit()
    return {'conversation_id':c.id,'conversation':conv_out(c),'user_message_id':user_msg.id,'message_id':assistant_msg.id,'message':result.text,'provider':provider.company,'display_name':provider.display_name,'model':provider.model,'usage':result.usage,'usage_source':result.usage_source,'context_window':provider.context_window,'fallback_reason':fallback_reason}
@app.patch('/api/conversations/{cid}')
def rename_conv(cid:int,payload:dict,request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db); c=db.query(Conversation).filter(Conversation.id==cid,Conversation.user_id==u.id).first();
    if not c: raise HTTPException(404,'Not found')
    c.title=normalize_saved_title(payload.get('title',c.title)); db.commit(); return conv_out(c)
@app.delete('/api/conversations/{cid}')
def delete_conv(cid:int,request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db); c=db.query(Conversation).filter(Conversation.id==cid,Conversation.user_id==u.id).first();
    if not c: raise HTTPException(404,'Not found')
    db.delete(c); db.commit(); return {'ok':True}
@app.post('/api/conversations/{cid}/archive')
def archive(cid:int,request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db); c=db.query(Conversation).filter(Conversation.id==cid,Conversation.user_id==u.id).first();
    if not c: raise HTTPException(404,'Not found')
    c.archived=True; db.commit(); return {'ok':True}

@app.get('/api/providers')
def providers(request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db); _purge_legacy_mock_providers(db,u.id); return [prov_out(p) for p in db.query(Provider).filter(Provider.user_id==u.id).order_by(Provider.priority).all()]
def prov_out(p): return {'id':p.id,'company':p.company,'provider_type':p.provider_type,'display_name':p.display_name,'model':p.model,'base_url':p.base_url,'masked_key':'••••••••' if p.encrypted_credential else 'Not configured','priority':p.priority,'enabled':p.enabled,'preferred':p.preferred,'capabilities':p.capabilities,'health':p.health,'last_tested_at':p.last_tested_at.isoformat() if p.last_tested_at else None,'latency_ms':p.latency_ms,'usage_source':p.usage_source,'context_window':p.context_window}
@app.post('/api/providers')
def add_provider(payload:ProviderIn,request:Request,db:OrmSession=Depends(get_db)):
    if payload.provider_type=='mock':
        raise HTTPException(422,'Mock providers are disabled. Add a real AI provider and its model instead.')
    if not payload.model.strip():
        raise HTTPException(422,'Model name is required.')
    if not payload.api_key:
        raise HTTPException(422,'API key is required for a configured AI provider.')
    u=get_current_user(request,db); _purge_legacy_mock_providers(db,u.id)
    provider_type=payload.provider_type.strip().lower(); model=payload.model.strip()
    duplicate=db.query(Provider).filter(Provider.user_id==u.id,Provider.provider_type==provider_type,Provider.model==model).first()
    if duplicate:
        raise HTTPException(409,f'This model is already configured for {duplicate.company}. Use the existing provider instead of adding a duplicate.')
    maxp=(db.query(func.max(Provider.priority)).filter(Provider.user_id==u.id).scalar() or 0)+1
    p=Provider(user_id=u.id,company=payload.company.strip(),provider_type=provider_type,display_name=payload.display_name.strip(),model=model,base_url=payload.base_url.strip() if payload.base_url else default_base_url(provider_type),encrypted_credential=encrypt_secret(payload.api_key) if payload.api_key else None,priority=maxp,capabilities=payload.capabilities,context_window=max(1024,min(payload.context_window,2000000)),health='UNCONFIGURED')
    db.add(p); db.commit(); db.refresh(p); return prov_out(p)
@app.post('/api/providers/{pid}/test')
async def test_provider(pid:int,request:Request,db:OrmSession=Depends(get_db)):
    # Provider rows can be deleted/edited while a health-check request is in flight.
    # Never let that race turn into a SQLAlchemy 500 or leave the session in a
    # PendingRollbackError state.
    u=get_current_user(request,db); p=db.query(Provider).filter(Provider.id==pid,Provider.user_id==u.id).first()
    if not p: raise HTTPException(404,'Provider not found')
    provider_type=p.provider_type; model=p.model; base_url=p.base_url or default_base_url(provider_type)
    credential=None
    if p.encrypted_credential:
        from .security import decrypt_secret
        credential=decrypt_secret(p.encrypted_credential)
    start=time.perf_counter()
    try:
        result=await adapter_for(provider_type).health_check(model,credential,base_url)
        latency=round((time.perf_counter()-start)*1000,1)
        status='healthy' if result.get('healthy') else 'unhealthy'
        request_id=result.get('request_id') or str(uuid.uuid4())
        try:
            # Refresh before writing so a concurrent delete/update is detected here.
            fresh=db.query(Provider).filter(Provider.id==pid,Provider.user_id==u.id).first()
            if not fresh:
                db.rollback()
                raise HTTPException(404,'Provider was removed before the health check completed')
            fresh.latency_ms=latency; fresh.last_tested_at=now(); fresh.health='HEALTHY' if status=='healthy' else 'UNHEALTHY'
            db.commit()
        except StaleDataError:
            db.rollback()
            raise HTTPException(409,'Provider changed or was removed while the health check was running')
        return {'status':status,'http_status':result.get('status'),'latency_ms':latency,'request_id':request_id,'message':result.get('error') or ('Connection successful' if status=='healthy' else 'Provider rejected the health-check request. Verify API key, endpoint, and exact model name.')}
    except HTTPException:
        raise
    except Exception as e:
        # Provider/network failures are application-level results, not server errors.
        db.rollback()
        try:
            fresh=db.query(Provider).filter(Provider.id==pid,Provider.user_id==u.id).first()
            if fresh:
                fresh.health='UNHEALTHY'; fresh.last_tested_at=now(); db.commit()
        except Exception:
            db.rollback()
        return {'status':'error','category':'provider_unavailable','message':str(e)[:200],'request_id':str(uuid.uuid4())}
@app.patch('/api/providers/{pid}')
def update_provider(pid:int,payload:dict,request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db); p=db.query(Provider).filter(Provider.id==pid,Provider.user_id==u.id).first();
    if not p: raise HTTPException(404,'Provider not found')
    for k in ['enabled','preferred','model','display_name','base_url','context_window']:
        if k in payload and payload[k] is not None: setattr(p,k,payload[k])
    if 'api_key' in payload and payload.get('api_key'):
        p.encrypted_credential=encrypt_secret(payload['api_key'])
    if p.provider_type in {'openai','nvidia','gemini','anthropic'} and not p.base_url:
        p.base_url=default_base_url(p.provider_type)
    if payload.get('preferred'):
        for other in db.query(Provider).filter(Provider.user_id==u.id,Provider.id!=pid): other.preferred=False
    db.commit(); return prov_out(p)
@app.delete('/api/providers/{pid}')
def remove_provider(pid:int,request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db); p=db.query(Provider).filter(Provider.id==pid,Provider.user_id==u.id).first();
    if not p: raise HTTPException(404,'Provider not found')
    db.delete(p); db.commit(); return {'ok':True}
@app.post('/api/providers/reorder')
def reorder(payload:dict,request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db)
    for idx,pid in enumerate(payload.get('ids',[]),1):
        p=db.query(Provider).filter(Provider.id==pid,Provider.user_id==u.id).first()
        if p:p.priority=idx
    db.commit(); return {'ok':True}

@app.get('/api/profile')
def profile(request:Request,db:OrmSession=Depends(get_db)): return user_out(get_current_user(request,db))
@app.patch('/api/profile')
def profile_update(payload:ProfileIn,request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db); u.display_name=payload.display_name.strip(); u.email=payload.email.lower(); u.timezone=payload.timezone; u.language=payload.language; u.theme=payload.theme; db.commit(); return user_out(u)
@app.post('/api/profile/avatar')
async def avatar(request:Request,file:UploadFile=File(...),db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db); allowed={'image/png','image/jpeg','image/webp'}
    if file.content_type not in allowed: raise HTTPException(415,'Avatar must be PNG, JPG or WEBP')
    data=await file.read()
    if len(data)>5*1024*1024: raise HTTPException(413,'Avatar exceeds 5 MB')
    ext={'image/png':'.png','image/jpeg':'.jpg','image/webp':'.webp'}[file.content_type]; name=f'user-{u.id}-{uuid.uuid4().hex}{ext}'; (UPLOAD_DIR/name).write_bytes(data); u.avatar_path=f'/uploads/{name}'; db.commit(); return {'avatar_path':u.avatar_path}
@app.delete('/api/profile/avatar')
def remove_avatar(request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db); u.avatar_path=None; db.commit(); return {'ok':True}

@app.post('/api/profile/password')
def change_password(payload:PasswordIn,request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db)
    if not verify_password(payload.current_password,u.password_hash): raise HTTPException(400,'Current password is incorrect')
    if payload.new_password != payload.confirm_password: raise HTTPException(422,'New passwords do not match')
    if len(payload.new_password)<10: raise HTTPException(422,'New password must be at least 10 characters')
    u.password_hash=hash_password(payload.new_password); db.query(DbSession).filter(DbSession.user_id==u.id).delete(); db.commit(); return {'ok':True}

@app.post('/api/auth/request-otp')
def request_otp(payload:OtpRequestIn,db:OrmSession=Depends(get_db)):
    import secrets
    u=db.query(User).filter(User.email==payload.email.lower()).first()
    # Never reveal account existence. Fake-mail mode returns a test challenge marker without exposing an OTP.
    if u:
        code=f'{secrets.randbelow(1000000):06d}'
        from datetime import timedelta,timezone
        ch=OtpChallenge(email=u.email,otp_hash=hash_token(code),expires_at=datetime.now(timezone.utc)+timedelta(minutes=10)); db.add(ch); db.commit()
    return {'ok':True,'message':'If the account exists, a verification code has been issued to the configured mail service.'}

@app.post('/api/auth/verify-otp')
def verify_otp(payload:OtpVerifyIn,db:OrmSession=Depends(get_db)):
    ch=db.query(OtpChallenge).filter(OtpChallenge.email==payload.email.lower(),OtpChallenge.used==False).order_by(OtpChallenge.id.desc()).first()
    if not ch or ch.expires_at < datetime.now(timezone.utc): raise HTTPException(400,'OTP expired or invalid')
    if ch.attempts>=5: raise HTTPException(429,'Too many OTP attempts')
    ch.attempts+=1
    if hash_token(payload.otp)!=ch.otp_hash: db.commit(); raise HTTPException(400,'OTP invalid')
    ch.used=True; db.commit(); return {'ok':True}

@app.get('/api/alerts')
def alerts(request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db); return [{'id':a.id,'severity':a.severity,'title':a.title,'message':a.message,'source':a.source,'read':a.read,'created_at':a.created_at.isoformat()} for a in db.query(Alert).filter(Alert.user_id==u.id).order_by(Alert.created_at.desc()).limit(50)]
@app.post('/api/alerts/{aid}/read')
def mark_alert(aid:int,request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db); a=db.query(Alert).filter(Alert.id==aid,Alert.user_id==u.id).first();
    if a:a.read=True; db.commit()
    return {'ok':True}

@app.post('/api/files')
async def upload(file:UploadFile=File(...),request:Request=None,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db); allowed={'pdf','docx','txt','csv','xlsx','json','png','jpg','jpeg','webp'}; ext=Path(file.filename or '').suffix.lower().lstrip('.')
    if ext not in allowed: raise HTTPException(415,'Unsupported file type')
    data=await file.read();
    if len(data)>settings.max_upload_mb*1024*1024: raise HTTPException(413,'File too large')
    safe=uuid.uuid4().hex+'-'+Path(file.filename or 'file').name.replace('..','_'); (UPLOAD_DIR/safe).write_bytes(data); fr=FileRecord(user_id=u.id,original_name=Path(file.filename or 'file').name,stored_name=safe,mime=file.content_type or mimetypes.guess_type(file.filename or '')[0] or 'application/octet-stream',size=len(data)); db.add(fr); db.commit(); return {'id':fr.id,'name':fr.original_name,'size':fr.size,'mime':fr.mime}
@app.get('/api/files')
def files(request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db); return [{'id':f.id,'name':f.original_name,'size':f.size,'mime':f.mime} for f in db.query(FileRecord).filter(FileRecord.user_id==u.id).order_by(FileRecord.created_at.desc()).all()]

@app.post('/api/links')
async def add_link(payload:dict,request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db); url=str(payload.get('url','')).strip()
    parsed=urllib.parse.urlparse(url)
    if parsed.scheme not in {'http','https'} or not parsed.netloc: raise HTTPException(422,'Enter a valid http(s) URL')
    name='link-'+uuid.uuid4().hex[:10]+'.url.txt'; data=url+'\n'
    (UPLOAD_DIR/name).write_text(data,encoding='utf-8'); fr=FileRecord(user_id=u.id,original_name=url,stored_name=name,mime='text/plain',size=len(data.encode()))
    db.add(fr); db.commit(); return {'id':fr.id,'name':fr.original_name,'size':fr.size,'mime':fr.mime,'url':url}

@app.get('/api/telemetry')
def telemetry(request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db)
    try:
        import psutil
        cpu=round(psutil.cpu_percent(interval=0.05),1)
        vm=psutil.virtual_memory(); ram=round(vm.percent,1)
        disk=psutil.disk_usage(str(ROOT)).percent
        net=psutil.net_io_counters()
        uptime=time.time()-psutil.boot_time()
        return {'cpu':{'value':cpu,'state':'available','source':'server psutil'},'ram':{'value':ram,'used_gb':round(vm.used/1024**3,2),'total_gb':round(vm.total/1024**3,2),'state':'available','source':'server psutil'},'battery':{'value':None,'state':'client-only','source':'browser Battery API'},'network':{'download':None,'upload':None,'ping':None,'state':'client-only','certainty':'browser Network Information API'},'disk':{'value':round(disk,1),'state':'available','source':'server psutil'},'uptime':{'value':round(uptime),'state':'available','source':'server psutil'}}
    except Exception as e:
        return {'cpu':{'value':None,'state':'unavailable','source':'telemetry error'},'ram':{'value':None,'state':'unavailable','source':'telemetry error'},'battery':{'value':None,'state':'client-only','source':'browser Battery API'},'network':{'download':None,'upload':None,'ping':None,'state':'client-only','certainty':'browser Network Information API'},'disk':{'value':None,'state':'unavailable','source':str(e)[:80]},'uptime':{'value':None,'state':'unavailable'}}

@app.get('/api/control-center')
async def control_center(request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db)
    _purge_legacy_mock_providers(db,u.id)
    providers=db.query(Provider).filter(Provider.user_id==u.id,Provider.enabled==True).order_by(Provider.preferred.desc(),Provider.priority.asc()).all()
    active=next((p for p in providers if p.health=='HEALTHY'),None)
    usage=None
    if active:
        usage=db.query(ProviderUsage).filter(ProviderUsage.user_id==u.id,ProviderUsage.provider_id==active.id).first()
    return {'provider': (prov_out(active) if active else None), 'usage': ({'total_tokens':usage.total_tokens,'requests':usage.requests,'exact_tokens':usage.exact_tokens,'estimated_tokens':usage.estimated_tokens,'usage_percent':round((usage.total_tokens/active.context_window)*100,2) if usage and active.context_window else None} if usage else {'total_tokens':0,'requests':0,'exact_tokens':0,'estimated_tokens':0,'usage_percent':0}), 'telemetry': telemetry(request,db), 'weather': await weather(request,db)}

async def _weather_current(config:WeatherConfig):
    if not config or not config.encrypted_key: return {'configured':False,'state':'not_configured','message':'Weather API not configured'}
    from .security import decrypt_secret
    cache=_weather_cache.get(config.user_id)
    if cache and time.time()-cache[0] < _WEATHER_CACHE_TTL: return cache[1]
    key=decrypt_secret(config.encrypted_key)
    if config.provider=='mock':
        result={'configured':True,'state':'ok','provider':'mock','location':config.location,'temperature':24,'humidity':60,'wind_speed':3.2,'feels_like':24,'description':'Partly cloudy','icon':'02d'}
        _weather_cache[config.user_id]=(time.time(),result); return result
    q=urllib.parse.quote(config.location)
    url=f'https://api.openweathermap.org/data/2.5/weather?q={q}&appid={urllib.parse.quote(key)}&units={config.units}'
    try:
        import httpx
        async with httpx.AsyncClient(timeout=httpx.Timeout(6.0,connect=3.0)) as client:
            r=await client.get(url)
        if r.status_code>=400:
            return {'configured':True,'state':'error','provider':config.provider,'location':config.location,'message':f'Weather service returned HTTP {r.status_code}'}
        d=r.json(); main=d.get('main',{}); wind=d.get('wind',{}); weather_data=(d.get('weather') or [{}])[0]
        result={'configured':True,'state':'ok','provider':config.provider,'location':d.get('name') or config.location,'temperature':main.get('temp'),'humidity':main.get('humidity'),'wind_speed':wind.get('speed'),'feels_like':main.get('feels_like'),'description':weather_data.get('description'),'icon':weather_data.get('icon'),'units':config.units}
        _weather_cache[config.user_id]=(time.time(),result); return result
    except Exception as e:
        return {'configured':True,'state':'error','provider':config.provider,'location':config.location,'message':'Weather request timed out or could not reach the service.'}

@app.get('/api/weather')
async def weather(request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db); w=db.query(WeatherConfig).filter(WeatherConfig.user_id==u.id).first()
    if not w:return {'state':'not_configured','message':'Weather API not configured','location':None,'configured':False}
    current=await _weather_current(w)
    return {'state':current.get('state','configured'),'provider':w.provider,'location':w.location,'units':w.units,'configured':bool(w.encrypted_key),**current}

@app.post('/api/weather')
def save_weather(payload:WeatherIn,request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db); w=db.query(WeatherConfig).filter(WeatherConfig.user_id==u.id).first()
    if not w:w=WeatherConfig(user_id=u.id); db.add(w)
    w.provider=payload.provider; w.location=payload.location.strip(); w.units=payload.units;
    if payload.api_key: w.encrypted_key=encrypt_secret(payload.api_key.strip())
    db.commit(); _weather_cache.pop(u.id,None); return {'state':'saved','provider':w.provider,'location':w.location,'units':w.units,'configured':bool(w.encrypted_key)}

@app.get('/api/weather/current')
async def weather_current(request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db); w=db.query(WeatherConfig).filter(WeatherConfig.user_id==u.id).first(); return await _weather_current(w)

@app.get('/api/projects')
def projects(request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db); return [{'id':p.id,'name':p.name,'overview':p.overview,'requirements':p.requirements,'tasks':p.tasks,'decisions':p.decisions,'bugs':p.bugs,'notes':p.notes,'memory':p.memory} for p in db.query(Project).filter(Project.user_id==u.id).all()]
@app.post('/api/projects')
def project(payload:dict,request:Request,db:OrmSession=Depends(get_db)):
    u=get_current_user(request,db); p=Project(user_id=u.id,name=payload.get('name','Untitled Project'),overview=payload.get('overview','')); db.add(p); db.commit(); db.refresh(p); return {'id':p.id,'name':p.name,'overview':p.overview}

# Serve built frontend when available. Explicit SPA fallback keeps /chat, /voice, etc.
# working on refresh/direct navigation instead of returning FastAPI 404.
frontend_dist=ROOT/'frontend'/'dist'
app.mount('/uploads',StaticFiles(directory=UPLOAD_DIR),name='uploads')
if frontend_dist.exists():
    assets_dir=frontend_dist/'assets'
    if assets_dir.exists(): app.mount('/assets',StaticFiles(directory=assets_dir),name='assets')
    @app.get('/favicon.ico',include_in_schema=False)
    def favicon():
        f=frontend_dist/'favicon.ico'
        if f.exists(): return FileResponse(f)
        raise HTTPException(404,'Favicon not found')
    @app.get('/{path:path}',include_in_schema=False)
    def spa_fallback(path:str):
        if path.startswith('api/') or path.startswith('uploads/') or path.startswith('assets/'):
            raise HTTPException(404,'Not found')
        index=frontend_dist/'index.html'
        if not index.exists(): raise HTTPException(503,'Frontend build is missing')
        return FileResponse(index)
