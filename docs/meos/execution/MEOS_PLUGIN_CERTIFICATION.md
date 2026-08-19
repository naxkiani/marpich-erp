# MEOS Plugin Certification

**Date:** 2026-08-18T07:45:00Z  
**Decision:** **No extension is CERTIFIED.** Gates are **defined**. Evidence is **missing** for every listing.

## Gates (required to become CERTIFIED)

| Gate | What must be true | Actual (2026-08-18) |
|------|-------------------|---------------------|
| FUNCTIONAL | Install → configure → activate → invoke on declared extension point | API tests on **demo echo** invoke — not a real widget/report runtime |
| SECURITY | AuthZ, sandbox, least privilege, no secret leakage | Permission grants + sandbox **profile names**; OS sandbox runtime **NOT_EVIDENCED** |
| COMPATIBILITY | MEOS / API / event / plugin contract versions | Semver upgrade helper only; no MEOS min/max on aggregate |
| TENANCY | Installations isolated by `tenant_id` | **TESTED** (API): tenant B cannot list tenant A installs |
| PRIVACY | Declared data access; no cross-tenant data | Declared permissions; production DSAR **FAIL** (G19) |
| PERFORMANCE | Catalog/search/install p95 under load | **NOT_AVAILABLE** (no production catalog load) |
| OBSERVABILITY | Real install/runtime/error telemetry | Dashboard `sandbox_violations_24h` is **hardcoded 0** — not telemetry |
| AUDIT | Install/enable/disable/upgrade events on fabric | Events **published** in-process; production bus **NOT_AVAILABLE** |
| DOCUMENTATION | Manifest + changelog + limitations | Seed descriptions only |
| SUPPLY_CHAIN | Signed artifact, provenance, vulnerability scan | `verify_signature` = format check. CVE / SLSA / real Ed25519 verify **NOT_AVAILABLE** |

Critical security failures **must BLOCK_INSTALLATION**. Today install is blocked for missing declared permission grants and unsigned-format checksums. That is **not** supply-chain certification.

## Activation vs certification

`POST /{plugin_id}/enable` does **not** require CERTIFIED. It only requires an installation + `plugins.install`.  

Therefore tenant enablement in tests is **not** a production certification. Global activation of unverified extensions is **forbidden** by this document. Production cluster is **not** live (G26).

## Canary / TEST / ACTIVE

Rollout `DISABLED → TEST → CANARY → ACTIVE` is **NOT_IMPLEMENTED** as a plugin deployment fabric. Only `enabled: true|false` on the installation row.

## Result

| Listing | CERTIFIED? |
|---------|------------|
| `com.marpich.demo-sales-widget` | **No** |
| `com.marpich.demo-report-pack` | **No** |
| Third-party / partner | **None** |

Do not invent security reviews, attestations, or certified partners.
