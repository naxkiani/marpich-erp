#!/usr/bin/env bash
# Apply SQL migrations to Marpich PostgreSQL (idempotent via platform.schema_migrations).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MIGRATIONS="$ROOT/infrastructure/docker/migrations"

PGHOST="${PGHOST:-127.0.0.1}"
PGPORT="${PGPORT:-5433}"
PGUSER="${PGUSER:-marpich}"
PGPASSWORD="${PGPASSWORD:-marpich}"
PGDATABASE="${PGDATABASE:-marpich_platform}"
export PGPASSWORD

psql_cmd() {
  psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" "$@"
}

if ! psql_cmd -tAc "SELECT to_regclass('tenant.tenants')" 2>/dev/null | grep -q "tenant.tenants"; then
  echo "Applying init-db.sql..."
  psql_cmd -f "$ROOT/infrastructure/docker/init-db.sql"
fi

migration_applied() {
  local version="$1"
  psql_cmd -tAc "SELECT 1 FROM platform.schema_migrations WHERE version = '${version}'" 2>/dev/null | grep -q 1
}

apply_migration() {
  local file="$1"
  local version
  version="$(basename "$file")"
  if migration_applied "$version"; then
    echo "Skipping ${version} (already applied)."
    return 0
  fi
  echo "Applying ${version}..."
  if ! psql_cmd -v ON_ERROR_STOP=1 -f "$MIGRATIONS/$file"; then
    echo "ERROR: migration ${version} failed." >&2
    exit 1
  fi
  psql_cmd -c "INSERT INTO platform.schema_migrations (version) VALUES ('${version}');"
}

apply_migration "000_schema_migrations.sql"

WAVE01_MIGRATIONS=(
  002_identity_full.sql
  003_contexts.sql
  004_notifications.sql
  005_settings.sql
  006_organization.sql
  007_audit.sql
  008_documents.sql
  009_workflow.sql
  010_integration.sql
  011_media.sql
  012_analytics.sql
  013_event_fabric.sql
  014_search.sql
  015_policy.sql
  016_identity_rls_principals.sql
)

POST_WAVE01_MIGRATIONS=(
  017_eif_fabric_schema.sql
  018_enterprise_directory_service.sql
  019_identity_lifecycle_platform.sql
  020_enterprise_organization_directory.sql
  021_enterprise_identity_graph.sql
  022_enterprise_authentication_platform.sql
  023_enterprise_password_authentication_engine.sql
  024_security_trusted_devices.sql
  025_enterprise_passkey_webauthn_platform.sql
  026_enterprise_adaptive_mfa_platform.sql
  027_enterprise_adaptive_risk_auth_engine.sql
  028_enterprise_identity_federation_platform.sql
  029_enterprise_identity_digital_twin.sql
  030_enterprise_authorization_platform.sql
  031_enterprise_identity_digital_twin_p199a.sql
  032_documents_rsa_signature_evidence.sql
  033_clinic_walkin_encounters.sql
  034_university_inventory_postgres.sql
  035_messenger_postgres.sql
  036_hospital_beds_cap_hlt_004.sql
  037_identity_governance.sql
  046_crm_contacts_opportunities.sql
  047_sales_quotations_orders.sql
  048_inventory_stock_reserved.sql
  049_accounting_ar_invoices.sql
  050_procurement_requisitions.sql
  051_procurement_goods_received.sql
  052_accounting_payment_received.sql
  053_human_resources_employees.sql
  054_payroll_employees_runs.sql
  055_tax_liabilities_returns.sql
)

for migration in "${WAVE01_MIGRATIONS[@]}"; do
  apply_migration "$migration" || exit 1
done

if [[ "${MEOS_WAVE01_ONLY:-0}" == "1" ]]; then
  echo "Wave 01 migrations applied (MEOS_WAVE01_ONLY=1; stopped after 016)."
  exit 0
fi

for migration in "${POST_WAVE01_MIGRATIONS[@]}"; do
  apply_migration "$migration" || exit 1
done

echo "All platform migrations applied (idempotent)."
