# Deferred platform migrations (SQL not yet on disk)
#
# These were listed historically in `scripts/run-migrations.sh` but the files
# were never committed. They must NOT block Wave 02+ migrate. Re-add to the
# runner only when the corresponding SQL lands under
# `infrastructure/docker/migrations/`.
#
# Missing as of 2026-08-14:
#   018_enterprise_directory_service.sql
#   020_enterprise_organization_directory.sql
#   021_enterprise_identity_graph.sql
#   022_enterprise_authentication_platform.sql
#   023_enterprise_password_authentication_engine.sql
#   024_security_trusted_devices.sql
#   025_enterprise_passkey_webauthn_platform.sql
#   026_enterprise_adaptive_mfa_platform.sql
#   027_enterprise_adaptive_risk_auth_engine.sql
#   030_enterprise_authorization_platform.sql
#   037_identity_governance.sql
#
# Related contexts may still run on memory stores until these land.
