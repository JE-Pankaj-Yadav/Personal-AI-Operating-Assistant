from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / 'data'
UPLOAD_DIR = ROOT / 'uploads'
LOG_DIR = ROOT / 'logs'
DB_PATH = DATA_DIR / 'pa_nexus.db'
DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

class Settings:
    app_name = 'PA NEXUS'
    secret_key = os.getenv('PA_NEXUS_SECRET_KEY', 'dev-only-change-me')
    database_url = os.getenv('DATABASE_URL', f'sqlite:///{DB_PATH.as_posix()}')
    cors_origins = [x.strip() for x in os.getenv('CORS_ORIGINS','http://127.0.0.1:8011,http://localhost:8011').split(',') if x.strip()]
    session_ttl_hours = int(os.getenv('SESSION_TTL_HOURS','24'))
    max_upload_mb = int(os.getenv('MAX_UPLOAD_MB','50'))
settings = Settings()
