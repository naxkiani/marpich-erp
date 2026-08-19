# MEOS Developer Governance

**Date:** 2026-08-18T11:30:00Z  
**Identity SoR:** `contexts/identity` · permissions on plugin routes  
**Certification SoR:** [MEOS_PLUGIN_CERTIFICATION.md](./MEOS_PLUGIN_CERTIFICATION.md) (P322) — **no listing CERTIFIED**

## Accounts and least privilege

Developer tooling defaults:

| Default | Actual |
|---------|--------|
| Auth required on plugin APIs | JWT + `require_permissions` |
| Tenant context | `X-Tenant-ID` |
| No hardcoded secrets in SDK examples | Demo **fingerprints** only — not live keys |
| Production admin via SDK | **Not granted** |
| `pack`/`sign`/`publish` success | **Forbidden** — CLI exits 2 |

Unsafe: treating `community`/`verified` trust labels or a valid manifest as production authorization.

## Environments

```
LOCAL (compose :5433) → DEVELOPMENT → TEST → STAGING → CERTIFICATION → PRODUCTION
```

Evidenced today: **LOCAL** (docker-compose.dev) and workstation pytest. Staging/certification/production clusters: **NOT_AVAILABLE** (G26).  
Ordinary `validate`/`init` **must not** require production credentials.

## Publishing (P322)

```
DEVELOP → VALIDATE (manifest) → SECURITY_SCAN → CERTIFY → SUBMIT → REVIEW → PUBLISH
```

| Step | Status |
|------|--------|
| VALIDATE manifest | **IMPLEMENTED** |
| SECURITY_SCAN (CVE/signing) | **NOT_AVAILABLE** |
| CERTIFY | Gates defined · **0 passed** |
| SUBMIT `plugins.publish` | API exists · production ops **NOT_AVAILABLE** |
| Uncontrolled production install via CLI | **Blocked** (pack/publish fail closed) |

## Partner developers

Partner → sandbox → certification → approval → production: **NOT_IMPLEMENTED**. No partner identities invented.

## Audit

Plugin Platform publishes `plugin.registered|published|installed|enabled|disabled|upgraded|uninstalled|sandbox.violation` with envelope actor/tenant. Production bus **NOT_AVAILABLE**. CLI init/validate are local filesystem actions — **not** automatically audited until submit APIs are used.
