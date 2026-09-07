# Runtime

Recommended: Python 3.14.x (recommended) and Node 22.x. Supported ranges: Python 3.11–3.14, Node 20–22.

Windows: run `run.bat` from any working directory. POSIX: `./run.sh` from any working directory.

The runner resolves its own root, creates `.venv`, runs Alembic against `PROJECT_ROOT/data/pa_nexus.db`, enters `frontend` before npm commands, typechecks, builds, verifies `frontend/dist/index.html`, then starts FastAPI on `127.0.0.1:8011`.

Set `PA_NEXUS_SECRET_KEY` in a local `.env` or process environment for production. Never commit it.
