FROM node:22.16.0-bookworm AS frontend
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install --no-audit --no-fund
COPY frontend ./
RUN npm run build
FROM python:3.14-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt
COPY backend /app/backend
COPY data /app/data
COPY uploads /app/uploads
COPY --from=frontend /app/frontend/dist /app/frontend/dist
COPY .env.example /app/.env.example
ENV PYTHONPATH=/app/backend
RUN useradd -r -u 10001 nexus && chown -R nexus:nexus /app
USER nexus
EXPOSE 8011
HEALTHCHECK --interval=20s --timeout=5s --retries=5 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8011/api/health',timeout=3)"
CMD ["sh","-c","cd /app/backend && alembic upgrade head && python -m uvicorn app.main:app --host 0.0.0.0 --port 8011"]
