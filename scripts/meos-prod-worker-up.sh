#!/usr/bin/env bash
# Production-profile outbox worker (same env as meos-prod-api-up.sh).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="${ROOT}/infrastructure/docker/compose/.env.meos-prod"
set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a
export DATABASE_URL="postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@127.0.0.1:5444/${POSTGRES_DB}"
export MARPICH_ENVIRONMENT=production
export PERSISTENCE_BACKEND=postgres
export EVENT_BUS_MODE=outbox
cd "${ROOT}/backend"
exec .venv/bin/python -m core.presentation.workers.outbox_worker
