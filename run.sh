#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "PA NEXUS root: $ROOT"
command -v python3 >/dev/null || { echo 'Python 3.11-3.14 required'; exit 1; }
python3 - <<'PY'
import sys
if sys.version_info[:2] not in {(3,11),(3,12),(3,13),(3,14)}: raise SystemExit(f'Unsupported Python: {sys.version}')
PY
command -v node >/dev/null || { echo 'Node 20-22 required'; exit 1; }
node -e "const m=+process.versions.node.split('.')[0]; if(m<20||m>22) process.exit(2)" || { echo 'Unsupported Node. Use Node 20-22.'; exit 1; }
python3 -m venv "$ROOT/.venv"
"$ROOT/.venv/bin/python" -m pip install -r "$ROOT/backend/requirements.txt"
cd "$ROOT/backend"
PYTHONPATH=. "$ROOT/.venv/bin/python" -m alembic upgrade head
PYTHONPATH=. "$ROOT/.venv/bin/python" -c 'import app.main'
cd "$ROOT/frontend"
if [[ -f package-lock.json ]]; then npm ci; else echo 'package-lock.json missing; run npm install once to generate it.'; npm install; fi
npm run typecheck
npm run build
test -f "$ROOT/frontend/dist/index.html"
cd "$ROOT"
PYTHONPATH="$ROOT/backend" exec "$ROOT/.venv/bin/python" -m uvicorn app.main:app --host 127.0.0.1 --port 8011
