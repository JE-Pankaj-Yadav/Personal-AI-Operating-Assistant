from sqlalchemy.orm import Session
from ..models import Provider, Capsule, SwitchEvent

def choose_provider(db:Session,user_id:int,conversation_id:int,required=None):
    required=set(required or ['text'])
    providers=db.query(Provider).filter(Provider.user_id==user_id,Provider.enabled==True).order_by(Provider.preferred.desc(),Provider.priority.asc()).all()
    candidates=[p for p in providers if set(p.capabilities or ['text']).issuperset(required) and p.health == 'HEALTHY']
    if not candidates: return None
    return candidates[0]

def ensure_capsule(db, conversation_id, context):
    latest=db.query(Capsule).filter(Capsule.conversation_id==conversation_id).order_by(Capsule.version.desc()).first()
    v=(latest.version+1 if latest else 1)
    data={'objective':context[:300], 'current_task':context[:500], 'requirements':['preserve same conversation'], 'constraints':['capability match','bounded fallback'], 'recent_messages':context[-2000:]}
    c=Capsule(conversation_id=conversation_id,version=v,data=data); db.add(c); db.commit(); return c
