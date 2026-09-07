import hashlib,secrets,time
from cryptography.fernet import Fernet
from argon2 import PasswordHasher
from ..config.settings import settings

password_hash=PasswordHasher()
# A stable local key is derived only for development; production should set PA_NEXUS_SECRET_KEY.
_key=hashlib.sha256(settings.secret_key.encode()).digest()
import base64
fernet=Fernet(base64.urlsafe_b64encode(_key))
def hash_password(p): return password_hash.hash(p)
def verify_password(p,h):
    try: return password_hash.verify(h,p)
    except Exception: return False
def hash_token(t): return hashlib.sha256(t.encode()).hexdigest()
def new_token(): return secrets.token_urlsafe(32)
def encrypt_secret(s): return fernet.encrypt(s.encode()).decode()
def decrypt_secret(s): return fernet.decrypt(s.encode()).decode()
