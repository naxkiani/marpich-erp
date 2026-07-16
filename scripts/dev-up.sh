#!/usr/bin/env bash
# Start local platform infra and apply migrations.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COMPOSE_FILE="${COMPOSE_FILE:-$ROOT/infrastructure/docker/compose/docker-compose.dev.yml}"
COMPOSE_PROFILES="${COMPOSE_PROFILES:-}"

cd "$ROOT"

echo "Starting Marpich platform services..."
if [[ -n "$COMPOSE_PROFILES" ]]; then
  COMPOSE_PROFILES="$COMPOSE_PROFILES" docker compose -f "$COMPOSE_FILE" up -d
else
  docker compose -f "$COMPOSE_FILE" up -d
fi

"$ROOT/scripts/wait-for-services.sh"
"$ROOT/scripts/run-migrations.sh"

echo "Local platform is ready."
echo "  Postgres: localhost:5432"
echo "  Redis:    localhost:6379"
echo "  Kafka:    localhost:9092"
echo "Run backend: cd backend && uvicorn core.presentation.api.main:app --reload --port 8000"
