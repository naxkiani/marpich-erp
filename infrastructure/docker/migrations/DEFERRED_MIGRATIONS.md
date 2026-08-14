# Identity / AuthZ platform migrations

**P1 (2026-08-14):** the historically missing SQL files are on disk and listed in
`scripts/run-migrations.sh` `POST_WAVE01_MIGRATIONS`. They are no longer skipped
for “file missing”.

| File | Schema | Postgres adapter |
|------|--------|------------------|
| `018_enterprise_directory_service.sql` | `directory` | `contexts.directory` when `use_postgres()` |
| `020_enterprise_organization_directory.sql` | `organization_directory` | SQL only (no live context package) |
| `021_enterprise_identity_graph.sql` | `identity_graph` | SQL only (no live context package) |
| `022_enterprise_authentication_platform.sql` | `authentication` | `contexts.authentication` when `use_postgres()` |
| `023_enterprise_password_authentication_engine.sql` | `password_auth` | SQL only (hashes live on `identity.users`) |
| `024_security_trusted_devices.sql` | `trusted_devices` | SQL only (`mfa` package still deferred) |
| `025_enterprise_passkey_webauthn_platform.sql` | `authentication` | `contexts.authentication` WebAuthn repo |
| `026_enterprise_adaptive_mfa_platform.sql` | `adaptive_mfa` | SQL only (`mfa` / `adaptive_authentication` deferred) |
| `027_enterprise_adaptive_risk_auth_engine.sql` | `identity_risk` | `contexts.identity_risk` when `use_postgres()` |
| `030_enterprise_authorization_platform.sql` | `"authorization"` | `contexts.authorization` when `use_postgres()` |
| `037_identity_governance.sql` | `identity_governance` | `contexts.identity_governance` when `use_postgres()` |

Do **not** treat this as `PRODUCTION_READY`. Memory path remains the default unless
Postgres is configured. `apply_migration` still warns-and-skips if a file is absent
(safety net), but these eleven files are expected to be present.
