#!/usr/bin/env bash
# LOCAL adapters — NON_PRODUCTION (compose.dev :5433 + uvicorn).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CMD="${1:-help}"
case "$CMD" in
  start) "$ROOT/scripts/dev-up.sh" ;;
  stop)
    docker compose -f "$ROOT/infrastructure/docker/compose/docker-compose.dev.yml" stop
    echo "LOCAL_STOP=TRUE"
    ;;
  backup)
    export PGPORT="${PGPORT:-5433}"
    "$ROOT/scripts/meos-postgres-backup.sh"
    ;;
  restore)
    export PGPORT="${PGPORT:-5433}"
    "$ROOT/scripts/meos-postgres-restore-drill.sh"
    ;;
  health)
    curl -fsS --max-time 5 http://127.0.0.1:8000/api/v1/health >/dev/null
    curl -fsS --max-time 5 http://127.0.0.1:8000/api/v1/ready >/dev/null
    echo "LOCAL_HEALTH=PASS"
    echo "LOCALHOST_IS_PRODUCTION=FALSE"
    ;;
  help|*)
    echo "Usage: $0 start|stop|backup|restore|health"
    echo "LOCALHOST_IS_PRODUCTION=FALSE"
    ;;
esac
