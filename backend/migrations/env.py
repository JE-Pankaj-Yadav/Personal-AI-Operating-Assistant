from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config,pool
from app.database import Base
from app.config.settings import settings
import app.models
config=context.config
config.set_main_option('sqlalchemy.url',settings.database_url)
# Logging configuration is optional for this standalone release.
target_metadata=Base.metadata
def run_migrations_offline():
    context.configure(url=settings.database_url,target_metadata=target_metadata,literal_binds=True,compare_type=True)
    with context.begin_transaction(): context.run_migrations()
def run_migrations_online():
    connectable=engine_from_config(config.get_section(config.config_ini_section),prefix='sqlalchemy.',poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection,target_metadata=target_metadata,compare_type=True)
        with context.begin_transaction(): context.run_migrations()
if context.is_offline_mode():run_migrations_offline()
else:run_migrations_online()
