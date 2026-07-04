#!/usr/bin/env bash
# Apply SQL migrations to Marpich PostgreSQL
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DOCKER_DIR="$ROOT/infrastructure/docker"

PGHOST="${PGHOST:-127.0.0.1}"
PGPORT="${PGPORT:-5432}"
PGUSER="${PGUSER:-marpich}"
PGPASSWORD="${PGPASSWORD:-marpich}"
PGDATABASE="${PGDATABASE:-marpich_platform}"
export PGPASSWORD

psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f "$DOCKER_DIR/init-db.sql"
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f "$DOCKER_DIR/migrations/002_identity_full.sql"
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f "$DOCKER_DIR/migrations/003_contexts.sql"
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f "$DOCKER_DIR/migrations/004_notifications.sql"
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f "$DOCKER_DIR/migrations/005_settings.sql"
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f "$DOCKER_DIR/migrations/006_organization.sql"
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f "$DOCKER_DIR/migrations/007_audit.sql"
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f "$DOCKER_DIR/migrations/008_documents.sql"
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f "$DOCKER_DIR/migrations/009_workflow.sql"
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f "$DOCKER_DIR/migrations/010_integration.sql"
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f "$DOCKER_DIR/migrations/011_media.sql"
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f "$DOCKER_DIR/migrations/012_analytics.sql"
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f "$DOCKER_DIR/migrations/013_event_fabric.sql"
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f "$DOCKER_DIR/migrations/014_search.sql"

echo "Migrations applied."
