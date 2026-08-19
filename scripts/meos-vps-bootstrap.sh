#!/usr/bin/env bash
# MEOS VPS launch foundation. Uses existing Compose. Does not provision cloud.
# Does not classify the host as production. Does not print secrets.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COMPOSE="${ROOT}/infrastructure/docker/compose/docker-compose.meos-prod.yml"
ENV_EXAMPLE="${ROOT}/infrastructure/launch/env.production.example"

echo "MEOS VPS foundation (NOT production certification)"
echo "compose=${COMPOSE}"

if ! command -v docker >/dev/null 2>&1; then
  echo "BLOCKED: docker CLI MISSING"
  echo "NEXT: install Docker Engine on the VPS, then re-run"
  exit 2
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "BLOCKED: docker compose MISSING"
  exit 2
fi

if [[ ! -f "$COMPOSE" ]]; then
  echo "BLOCKED: compose file missing"
  exit 2
fi

echo "Docker: AVAILABLE"
echo "Firewall expectation: allow 80/443; do not publish PostgreSQL publicly"
echo "TLS: use Caddyfile.vps.example with a public hostname; localhost certs are DEVELOPMENT ONLY"
echo "Secrets: copy ${ENV_EXAMPLE} to a gitignored env file; never commit values"
echo "Backup: scripts/meos-postgres-backup.sh against the VPS Postgres (not workstation :5433 as production evidence)"
echo "Restore: scripts/meos-postgres-restore-drill.sh"
echo "Release identity: set MEOS_IMAGE to ghcr.io/marpich/marpich-backend@sha256:<digest>"
echo "Do not use :latest as release identity"
echo "CURRENT_ARTIFACT=\${MEOS_IMAGE:-NOT_AVAILABLE}"
echo "PREVIOUS_ARTIFACT=\${MEOS_PREVIOUS_IMAGE:-NOT_AVAILABLE}"
echo "Upgrade: docker compose -p meosprod --env-file <gitignored-env> -f ${COMPOSE} pull && up -d"
echo "Rollback: set MEOS_IMAGE=\${MEOS_PREVIOUS_IMAGE} then compose up -d (digest, not :latest)"
echo "ROLLBACK_TESTED=FALSE (local/VPS rollback is not production G27)"
echo "STATUS: READY_FOR_CREDENTIALS"
echo "This host is NOT G26 production until EXT-G26 validator PASSes."
