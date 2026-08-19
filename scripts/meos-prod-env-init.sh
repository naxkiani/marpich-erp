#!/usr/bin/env bash
# Generate gitignored production-profile secrets (hex — URL-safe).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COMPOSE_DIR="${ROOT}/infrastructure/docker/compose"
OUT="${COMPOSE_DIR}/.env.meos-prod"
CERT_DIR="${COMPOSE_DIR}/certs"

if [[ -f "$OUT" && "${MEOS_PROD_ENV_OVERWRITE:-0}" != "1" ]]; then
  echo "exists: $OUT (set MEOS_PROD_ENV_OVERWRITE=1 to rotate)"
else
  PG_PASS="$(openssl rand -hex 24)"
  JWT="$(openssl rand -hex 32)"
  DOC="$(openssl rand -hex 24)"
  MINIO_USER="meosprod$(openssl rand -hex 4)"
  MINIO_PASS="$(openssl rand -hex 24)"
  REPL_PASS="$(openssl rand -hex 16)"
  cat >"$OUT" <<EOF
POSTGRES_USER=meos_app
POSTGRES_PASSWORD=${PG_PASS}
POSTGRES_DB=marpich_platform
POSTGRES_REPLICATION_PASSWORD=${REPL_PASS}
JWT_SECRET=${JWT}
DOCUMENT_SIGNING_SECRET=${DOC}
MEOS_S3_ACCESS_KEY=${MINIO_USER}
MEOS_S3_SECRET_KEY=${MINIO_PASS}
MEOS_BACKUP_S3_URI=s3://meos-backups/postgres
MEOS_S3_ENDPOINT_URL=http://127.0.0.1:9100
MARPICH_ENVIRONMENT=production
PERSISTENCE_BACKEND=postgres
EVENT_BUS_MODE=outbox
OTEL_ENABLED=true
DATABASE_URL=postgresql+asyncpg://meos_app:${PG_PASS}@postgres:5432/marpich_platform
EOF
  echo "wrote $OUT"
fi

mkdir -p "$CERT_DIR"
if [[ ! -f "${CERT_DIR}/tls.crt" ]]; then
  openssl req -x509 -newkey rsa:2048 -nodes \
    -keyout "${CERT_DIR}/tls.key" \
    -out "${CERT_DIR}/tls.crt" \
    -days 30 \
    -subj "/CN=localhost"
  echo "wrote ${CERT_DIR}/tls.crt (self-signed, local production-profile only)"
fi
