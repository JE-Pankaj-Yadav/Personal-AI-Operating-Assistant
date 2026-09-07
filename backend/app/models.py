from datetime import datetime, timezone
from sqlalchemy import String, Integer, Boolean, DateTime, Text, ForeignKey, Float, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

def now(): return datetime.now(timezone.utc)
class User(Base):
    __tablename__='users'
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    email: Mapped[str]=mapped_column(String(255),unique=True,index=True)
    username: Mapped[str]=mapped_column(String(100),unique=True,index=True)
    display_name: Mapped[str]=mapped_column(String(120))
    password_hash: Mapped[str]=mapped_column(String(512))
    timezone: Mapped[str]=mapped_column(String(80),default='Asia/Kolkata')
    language: Mapped[str]=mapped_column(String(20),default='en')
    theme: Mapped[str]=mapped_column(String(20),default='dark')
    avatar_path: Mapped[str|None]=mapped_column(String(500),nullable=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)

class Session(Base):
    __tablename__='sessions'
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey('users.id',ondelete='CASCADE'),index=True)
    token_hash: Mapped[str]=mapped_column(String(128),unique=True,index=True)
    expires_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),index=True)

class Conversation(Base):
    __tablename__='conversations'
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey('users.id',ondelete='CASCADE'),index=True)
    conversation_type: Mapped[str]=mapped_column(String(20),index=True)
    title: Mapped[str]=mapped_column(String(255))
    archived: Mapped[bool]=mapped_column(Boolean,default=False)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
    messages=relationship('Message',cascade='all,delete-orphan')
    __table_args__=(UniqueConstraint('id','user_id'),)

class Message(Base):
    __tablename__='messages'
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    conversation_id: Mapped[int]=mapped_column(ForeignKey('conversations.id',ondelete='CASCADE'),index=True)
    role: Mapped[str]=mapped_column(String(20))
    content: Mapped[str]=mapped_column(Text())
    provider: Mapped[str|None]=mapped_column(String(100),nullable=True)
    model: Mapped[str|None]=mapped_column(String(150),nullable=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
    feedback: Mapped[str|None]=mapped_column(String(20),nullable=True)

class Provider(Base):
    __tablename__='providers'
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey('users.id',ondelete='CASCADE'),index=True)
    company: Mapped[str]=mapped_column(String(80))
    provider_type: Mapped[str]=mapped_column(String(80))
    display_name: Mapped[str]=mapped_column(String(120))
    model: Mapped[str]=mapped_column(String(160))
    base_url: Mapped[str|None]=mapped_column(String(500),nullable=True)
    encrypted_credential: Mapped[str|None]=mapped_column(Text(),nullable=True)
    priority: Mapped[int]=mapped_column(Integer,default=1)
    enabled: Mapped[bool]=mapped_column(Boolean,default=True)
    preferred: Mapped[bool]=mapped_column(Boolean,default=False)
    capabilities: Mapped[list]=mapped_column(JSON,default=list)
    health: Mapped[str]=mapped_column(String(30),default='UNCONFIGURED')
    last_tested_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True)
    latency_ms: Mapped[float|None]=mapped_column(Float,nullable=True)
    usage_source: Mapped[str]=mapped_column(String(20),default='estimated')
    context_window: Mapped[int]=mapped_column(Integer,default=128000)

class ProviderUsage(Base):
    __tablename__='provider_usage'
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey('users.id',ondelete='CASCADE'),index=True)
    provider_id: Mapped[int]=mapped_column(ForeignKey('providers.id',ondelete='CASCADE'),index=True)
    total_tokens: Mapped[int]=mapped_column(Integer,default=0)
    requests: Mapped[int]=mapped_column(Integer,default=0)
    exact_tokens: Mapped[int]=mapped_column(Integer,default=0)
    estimated_tokens: Mapped[int]=mapped_column(Integer,default=0)
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)

class Capsule(Base):
    __tablename__='capsules'
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    conversation_id: Mapped[int]=mapped_column(ForeignKey('conversations.id',ondelete='CASCADE'),index=True)
    version: Mapped[int]=mapped_column(Integer)
    data: Mapped[dict]=mapped_column(JSON,default=dict)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)

class SwitchEvent(Base):
    __tablename__='switch_events'
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    conversation_id: Mapped[int]=mapped_column(ForeignKey('conversations.id',ondelete='CASCADE'),index=True)
    from_provider: Mapped[str|None]=mapped_column(String(100),nullable=True)
    to_provider: Mapped[str]=mapped_column(String(100))
    reason: Mapped[str]=mapped_column(String(255))
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)

class Alert(Base):
    __tablename__='alerts'
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey('users.id',ondelete='CASCADE'),index=True)
    severity: Mapped[str]=mapped_column(String(20),default='info')
    title: Mapped[str]=mapped_column(String(160))
    message: Mapped[str]=mapped_column(Text())
    source: Mapped[str]=mapped_column(String(80),default='system')
    read: Mapped[bool]=mapped_column(Boolean,default=False)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)

class FileRecord(Base):
    __tablename__='files'
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey('users.id',ondelete='CASCADE'),index=True)
    original_name: Mapped[str]=mapped_column(String(255))
    stored_name: Mapped[str]=mapped_column(String(255),unique=True)
    mime: Mapped[str]=mapped_column(String(120))
    size: Mapped[int]=mapped_column(Integer)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)

class WeatherConfig(Base):
    __tablename__='weather_configs'
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey('users.id',ondelete='CASCADE'),unique=True,index=True)
    provider: Mapped[str]=mapped_column(String(80),default='openweather')
    location: Mapped[str]=mapped_column(String(160))
    units: Mapped[str]=mapped_column(String(20),default='metric')
    encrypted_key: Mapped[str|None]=mapped_column(Text(),nullable=True)

class OtpChallenge(Base):
    __tablename__='otp_challenges'
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    email: Mapped[str]=mapped_column(String(255),index=True)
    otp_hash: Mapped[str]=mapped_column(String(128))
    expires_at: Mapped[datetime]=mapped_column(DateTime(timezone=True))
    attempts: Mapped[int]=mapped_column(Integer,default=0)
    used: Mapped[bool]=mapped_column(Boolean,default=False)

class Project(Base):
    __tablename__='projects'
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey('users.id',ondelete='CASCADE'),index=True)
    name: Mapped[str]=mapped_column(String(160))
    overview: Mapped[str]=mapped_column(Text(),default='')
    requirements: Mapped[list]=mapped_column(JSON,default=list)
    tasks: Mapped[list]=mapped_column(JSON,default=list)
    decisions: Mapped[list]=mapped_column(JSON,default=list)
    bugs: Mapped[list]=mapped_column(JSON,default=list)
    notes: Mapped[list]=mapped_column(JSON,default=list)
    memory: Mapped[list]=mapped_column(JSON,default=list)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
