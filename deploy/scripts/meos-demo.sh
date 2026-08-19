#!/usr/bin/env bash
# MEOS DEMO package — one-command start/stop/reset/backup/restore/health.
# COMPOSE_IS_PRODUCTION = FALSE. Does not print secrets. Does not claim G26.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
COMPOSE_DIR="$ROOT/infrastructure/docker/compose"
COMPOSE_FILE="$COMPOSE_DIR/docker-compose.meos-prod.yml"
ENV_FILE="$COMPOSE_DIR/.env.meos-prod"
if [[ ! -f "$ENV_FILE" ]]; then
  ENV_FILE="$COMPOSE_DIR/.env.example"
  echo "WARN: .env.meos-prod missing; using .env.example (DEMO credentials). COMPOSE_IS_PRODUCTION=FALSE"
fi
COMPOSE=(docker compose -p meosprod --env-file "$ENV_FILE" -f "$COMPOSE_FILE")
CMD="${1:-help}"

select_local_image() {
  if [[ -n "${MEOS_IMAGE:-}" ]]; then
    return
  fi
  if docker image inspect meos/backend:p353-local >/dev/null 2>&1; then
    export MEOS_IMAGE=meos/backend:p353-local
  elif docker image inspect meos/backend:local-build >/dev/null 2>&1; then
    export MEOS_IMAGE=meos/backend:local-build
  else
    export MEOS_IMAGE=meos/backend:local-build
  fi
  echo "MEOS_IMAGE=${MEOS_IMAGE}"
  echo "IMAGE_CLASS=NON_PRODUCTION"
}

health_url() {
  local path="$1"
  curl -fsS --max-time 5 "http://127.0.0.1:8080${path}" >/dev/null
}

case "$CMD" in
  start)
    select_local_image
    "${COMPOSE[@]}" up -d --pull never
    echo "DEMO_START=TRUE"
    echo "COMPOSE_IS_PRODUCTION=FALSE"
    echo "API=http://127.0.0.1:8080"
    echo "PROCESS_HEALTH=/api/v1/health"
    echo "APPLICATION_READINESS=/api/v1/ready"
    ;;
  stop)
    "${COMPOSE[@]}" stop
    echo "DEMO_STOP=TRUE"
    ;;
  reset)
    echo "WARN: reset destroys meosprod volumes (NON_PRODUCTION only)."
    select_local_image
    "${COMPOSE[@]}" down -v
    "${COMPOSE[@]}" up -d --pull never
    echo "DEMO_RESET=TRUE"
    echo "COMPOSE_IS_PRODUCTION=FALSE"
    ;;
  backup)
    set -a
    # shellcheck disable=SC1090
    source "$ENV_FILE"
    set +a
    export PGHOST=127.0.0.1
    export PGPORT="${MEOS_DEMO_PGPORT:-5444}"
    export PGUSER="${POSTGRES_USER:-meos_app}"
    export PGDATABASE="${POSTGRES_DB:-marpich_platform}"
    export PGPASSWORD="${POSTGRES_PASSWORD:-}"
    export MEOS_POSTGRES_CONTAINER=meos-prod-postgres
    "$ROOT/scripts/meos-postgres-backup.sh"
    echo "DEMO_BACKUP=TRUE"
    echo "BACKUP_CLASS=LOCAL_NON_PRODUCTION"
    ;;
  restore)
    set -a
    # shellcheck disable=SC1090
    source "$ENV_FILE"
    set +a
    export PGHOST=127.0.0.1
    export PGPORT="${MEOS_DEMO_PGPORT:-5444}"
    export PGUSER="${POSTGRES_USER:-meos_app}"
    export PGDATABASE="${POSTGRES_DB:-marpich_platform}"
    export PGPASSWORD="${POSTGRES_PASSWORD:-}"
    export MEOS_POSTGRES_CONTAINER=meos-prod-postgres
    "$ROOT/scripts/meos-postgres-restore-drill.sh"
    echo "DEMO_RESTORE=TRUE"
    echo "RESTORE_CLASS=LOCAL_NON_PRODUCTION"
    ;;
  health)
    if health_url /api/v1/health; then
      echo "PROCESS_HEALTH=PASS"
    else
      echo "PROCESS_HEALTH=FAIL"
      exit 1
    fi
    if health_url /api/v1/ready; then
      echo "APPLICATION_READINESS=PASS"
    else
      echo "APPLICATION_READINESS=FAIL"
      exit 1
    fi
    echo "PRODUCTION_READINESS=NOT_APPLICABLE"
    echo "COMPOSE_IS_PRODUCTION=FALSE"
    ;;
  help|*)
    echo "Usage: $0 start|stop|reset|backup|restore|health"
    echo "Canonical compose: infrastructure/docker/compose/docker-compose.meos-prod.yml"
    echo "COMPOSE_IS_PRODUCTION=FALSE"
    exit 0
    ;;
esac
