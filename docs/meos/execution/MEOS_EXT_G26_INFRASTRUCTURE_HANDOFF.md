# MEOS EXT-G26 Infrastructure Handoff Pack

**Date:** 2026-08-19T10:05:00Z  
**EXT-G26:** **UNRESOLVED**  
**G26_READY:** **FALSE** (validator). **P0 = 1** (unchanged).  
**P313 auto-start:** **false**. GO_LIVE **NOT APPROVED**. **ACTIVE = 0**.  
**Machine:** [MEOS_EXT_G26_INFRASTRUCTURE.v1.yaml](./MEOS_EXT_G26_INFRASTRUCTURE.v1.yaml)  
**Validator:** `scripts/meos-ext-g26-readiness.py`  
**Reuse:** existing Helm `marpich-iam`, Flux HelmRelease, CI `identity-federation-enterprise.yml`, GHCR. No second deploy platform.

This pack is the executable dependency contract. It does **not** provision cloud, simulate TLS, or execute GO-LIVE.

**P349 (2026-08-19):** Discovery complete — **REQUIREMENTS_IDENTIFIED**, not G26 PASS. Compatibility [MEOS_EXT_G26_PROVIDER_COMPATIBILITY.md](./MEOS_EXT_G26_PROVIDER_COMPATIBILITY.md). Dependencies [MEOS_EXT_G26_EXTERNAL_DEPENDENCIES.v1.yaml](./MEOS_EXT_G26_EXTERNAL_DEPENDENCIES.v1.yaml). BOM [MEOS_EXT_G26_PRODUCTION_BOM.md](./MEOS_EXT_G26_PRODUCTION_BOM.md). Plan [MEOS_EXT_G26_INFRASTRUCTURE_IMPLEMENTATION_PLAN.md](./MEOS_EXT_G26_INFRASTRUCTURE_IMPLEMENTATION_PLAN.md). Machine [MEOS_P349_INFRASTRUCTURE_DISCOVERY.v1.yaml](./MEOS_P349_INFRASTRUCTURE_DISCOVERY.v1.yaml).  
**P350 (2026-08-19):** Provisioning **BLOCKED**. [MEOS_P350_PROVISIONING_REPORT.md](./MEOS_P350_PROVISIONING_REPORT.md) · [MEOS_EXT_G26_PROVISIONING_STATUS.v1.yaml](./MEOS_EXT_G26_PROVISIONING_STATUS.v1.yaml).

## Resources

| Resource | Purpose | Required state | Evidence (now) | Owner | Dependency | Validation command | Blocking effect |
|----------|---------|----------------|----------------|-------|------------|--------------------|-----------------|
| G26-01 cluster | Production compute | Authorized cluster reachable | KUBECONFIG missing | NOT_AVAILABLE | Hosting account | `test -n "$KUBECONFIG" -o -f "$HOME/.kube/config"` | G26 BLOCKED |
| G26-02 Postgres | Production data | Managed Postgres, not :5433/:5444 | Workstation/compose only | NOT_AVAILABLE | G26-01 | Host not localhost; port not 5433/5444 | G26 BLOCKED |
| G26-03 TLS | Public HTTPS | Public DNS + public CA | Public CA missing | NOT_AVAILABLE | DNS ownership | `MEOS_PUBLIC_CA_TLS=1` + non-local DNS | G26 BLOCKED |
| G26-04 secrets | Credential injection | Secret manager available | Availability unset | NOT_AVAILABLE | Secret store | `MEOS_SECRET_MANAGER_AVAILABLE=1` (no values printed) | G26 BLOCKED |
| G26-05 release | Immutable artifact | `git status --short` empty + digest | `47258dfd-dirty` FORBIDDEN | NOT_AVAILABLE | Clean tree | `git status --short` | G26 FAIL |
| G26-06 CI deploy | Traceable deploy | Existing CI + digest + credentials | Workflow DESIGNED | NOT_AVAILABLE | G26-01 + G26-05 | existing GHCR workflow + `MEOS_IMAGE_DIGEST` | G26 BLOCKED |
| G26-07 network | Ingress/DNS | Non-local DNS | NOT_AVAILABLE | NOT_AVAILABLE | G26-01 | `MEOS_PRODUCTION_DNS` non-localhost | G26 BLOCKED |
| G26-08 runtime | Running identity | Deployed commit/digest; not local /health | NOT_LAUNCHED | NOT_AVAILABLE | G26-01…07 | `MEOS_DEPLOYED_COMMIT` / `MEOS_DEPLOYED_DIGEST` | G26 BLOCKED |
| G26-09 identity | Commit=digest match | Deployed = certified | NOT_AVAILABLE | NOT_AVAILABLE | G26-05/06/08 | deployed commit equals HEAD; digest equals CI | G26 BLOCKED |
| G26-10 rollback | Recoverability | Exercised N→N+1→N | Helm CONFIGURED, not verified | NOT_AVAILABLE | First prod release | `MEOS_ROLLBACK_EXERCISED=1` after real rollback | G27 stays BLOCKED |

## P313 re-entry

```
IF G26_READY = TRUE
THEN STOP P348
THEN START P313 RE-CERTIFICATION (explicit; not automatic)
P313 recalculates P0 independently
```

Do **not** start P313 from this validator. Do **not** approve GO-LIVE.

## Validator

```bash
python3 scripts/meos-ext-g26-readiness.py
```

Exit 2 while G26 is not ready. Does not print secret values.
