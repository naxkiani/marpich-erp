#!/usr/bin/env bash
# Apply SQL migrations to Marpich PostgreSQL (015–027 enterprise identity + adaptive auth)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MIGRATIONS="$ROOT/infrastructure/docker/migrations"

PGHOST="${PGHOST:-127.0.0.1}"
PGPORT="${PGPORT:-5432}"
PGUSER="${PGUSER:-marpich}"
PGPASSWORD="${PGPASSWORD:-marpich}"
PGDATABASE="${PGDATABASE:-marpich_platform}"
export PGPASSWORD

psql_cmd() {
  psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" "$@"
}

psql_cmd -f "$ROOT/infrastructure/docker/init-db.sql"

for migration in \
  002_identity_full.sql \
  003_contexts.sql \
  004_notifications.sql \
  005_settings.sql \
  006_organization.sql \
  007_audit.sql \
  008_documents.sql \
  009_workflow.sql \
  010_integration.sql \
  011_media.sql \
  012_analytics.sql \
  013_event_fabric.sql \
  014_search.sql \
  015_policy.sql \
  016_identity_rls_principals.sql \
  017_eif_fabric_schema.sql \
  018_enterprise_directory_service.sql \
  019_identity_lifecycle_platform.sql \
  020_enterprise_organization_directory.sql \
  021_enterprise_identity_graph.sql \
  022_enterprise_authentication_platform.sql \
  023_enterprise_password_authentication_engine.sql \
  024_security_trusted_devices.sql \
  025_enterprise_passkey_webauthn_platform.sql \
  026_enterprise_adaptive_mfa_platform.sql \
  027_enterprise_adaptive_risk_auth_engine.sql \
  028_enterprise_identity_federation_platform.sql
do
  echo "Applying $migration..."
  psql_cmd -f "$MIGRATIONS/$migration"
done

echo "All migrations (002–027) applied."
