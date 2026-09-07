# Architecture

Frontend: React + TypeScript + Vite + React Router + Lucide icons. UI is divided into layouts, pages, features, services, stores and typed models.

Backend: FastAPI routes → service/adapter boundaries → SQLAlchemy repositories/models → SQLite local database. Alembic owns schema migration. Provider HTTP behavior is isolated in adapters.

Security: Argon2id password hashes, server-side Fernet-encrypted provider credentials, HTTP-only session cookie, ownership filters on user resources, upload extension/MIME/size checks, no credential logging or frontend exposure.

Runtime: canonical project-root paths, Python virtual environment, supported Python 3.11–3.14 and Node 20–22, Windows/PowerShell/POSIX runners, Docker image, health endpoint.
