# MEOS Plugin Governance

**Date:** 2026-08-18T07:45:00Z  
**SoR:** `contexts/plugins` · `/api/v1/plugins` · catalog `docs/architecture/plugins/PLUGIN_CATALOG.yaml`  
**P322:** [MEOS_P322_EXTENSION_ECOSYSTEM.md](./MEOS_P322_EXTENSION_ECOSYSTEM.md) · [MEOS_PLUGIN_CERTIFICATION.md](./MEOS_PLUGIN_CERTIFICATION.md)  
**P323:** [MEOS_P323_DEVELOPER_PLATFORM.md](./MEOS_P323_DEVELOPER_PLATFORM.md) — SDK/CLI fail-closed pack/sign/publish; plugin event schemas registered.  
**Law:** Signed, sandboxed, permission-granted. **Never trust a plugin merely because it is listed.** **Install does not activate.**

## Seed listings (not production ACTIVE)

| PLUGIN_ID | VERSION | TYPE | TRUST (catalog) | CAPABILITIES | STATUS |
|-----------|---------|------|-----------------|--------------|--------|
| `com.marpich.demo-sales-widget` | 1.0.0 | widget | community | `ui.dashboard.widget` | seed / **NOT_CERTIFIED** / production **DISABLED** |
| `com.marpich.demo-report-pack` | 2.1.0 | report | verified | `analytics.report.template` | seed / **NOT_CERTIFIED** / production **DISABLED** |

`verified` is **catalog metadata**, not a security certification.

Permissions on seeds include `analytics.read` / `sales.orders.read` / `finance.reports.read` — **grants at install**, not unrestricted DB/secrets/admin.

## Lifecycle (API exists)

| Action | Route / behavior |
|--------|------------------|
| Discover | `GET /marketplace/listings` (filter type, trust, q) |
| Install | `POST /{id}/install` → `enabled=false` · `plugin.installed` |
| Activate | `POST /{id}/enable` · `plugin.enabled` |
| Deactivate | `POST /{id}/disable` · `plugin.disabled` |
| Invoke | `POST /invoke` — fails `plugins.errors.not_enabled` if disabled |
| Upgrade | upgrade API + semver |
| Uninstall | `DELETE /{id}/install` |
| Rollback | **NOT_IMPLEMENTED** |
| CERTIFIED / AVAILABLE | **No listing** |

Covered by `test_plugin_flow.py` (including tenant isolation and permission denial).  
Production INSTALLED/ACTIVE plugins: **none evidenced**.

## Security

| Must not (unless policy) | Enforcement |
|--------------------------|-------------|
| Direct module imports of plugin code | Architecture law |
| Unsigned packages in production | Catalog `signed_packages_required` — production signing ops **NOT_AVAILABLE** |
| Unrestricted DB / secrets / AI admin | Permission catalog + sandbox **profiles** (OS sandbox **NOT_EVIDENCED**) |
| Treat format `verify_signature` as supply-chain cert | **Forbidden** — checksum prefix check only |

Invoke without tenant/auth: denied by `require_permissions`.

**Never mark plugin ACTIVE in production from seed data.**
