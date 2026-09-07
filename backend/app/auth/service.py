from datetime import datetime,timezone,timedelta
from fastapi import HTTPException,Request
from sqlalchemy.orm import Session
from ..models import User,Session as DbSession
from ..security import hash_password,verify_password,new_token,hash_token
from ..config.settings import settings

def get_current_user(request:Request,db:Session):
    raw=request.cookies.get('pa_session')
    if not raw: raise HTTPException(401,'Authentication required')
    s=db.query(DbSession).filter(DbSession.token_hash==hash_token(raw),DbSession.expires_at>datetime.now(timezone.utc)).first()
    if not s: raise HTTPException(401,'Session expired')
    u=db.get(User,s.user_id)
    if not u: raise HTTPException(401,'User not found')
    return u

def login(db,email,password):
    u=db.query(User).filter(User.email==email.lower().strip()).first()
    if not u or not verify_password(password,u.password_hash): raise HTTPException(401,'Invalid email or password')
    raw=new_token(); db.add(DbSession(user_id=u.id,token_hash=hash_token(raw),expires_at=datetime.now(timezone.utc)+timedelta(hours=settings.session_ttl_hours))); db.commit(); return u,raw

def register(db,email,username,display_name,password):
    if db.query(User).filter((User.email==email.lower()) | (User.username==username)).first(): raise HTTPException(409,'Account already exists')
    u=User(email=email.lower().strip(),username=username.strip(),display_name=display_name.strip() or username,password_hash=hash_password(password)); db.add(u); db.commit(); db.refresh(u)
    return u
