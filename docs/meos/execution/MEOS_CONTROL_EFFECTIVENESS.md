# MEOS Control Effectiveness

**Date:** 2026-08-18T13:00:00Z  
**SoR (catalog):** [MEOS_SECURITY_CONTROL_MATRIX.md](./MEOS_SECURITY_CONTROL_MATRIX.md) — **do not create a parallel control framework.**  
**Machine:** [MEOS_CONTROL_EFFECTIVENESS.v1.yaml](./MEOS_CONTROL_EFFECTIVENESS.v1.yaml)

`production_effective_count: 0` · `monitored_count: 0`

A documented or candidate-tested control is **not** an effective production control.

## Vocabulary

`DESIGNED` → `IMPLEMENTED` → `TESTED` → `EFFECTIVE` | `FAILED`

P328 does **not** mark any control **EFFECTIVE** (production). Candidate P313 tests = **TESTED** / **CANDIDATE**.

## Mapping (actual)

| CONTROL_ID | TYPE | STATUS | EFFECTIVENESS | RISKS |
|------------|------|--------|---------------|-------|
| `CTL-AUTH-JWT` | PREVENT | TESTED | CANDIDATE | — |
| `CTL-AUTHZ-PDP` | PREVENT | TESTED | CANDIDATE | — |
| `CTL-TENANT-ISOLATION` | PREVENT | TESTED | CANDIDATE | — |
| `CTL-AUDIT-MUTATIONS` | DETECT | TESTED | CANDIDATE | — |
| `CTL-HEALTH-PROBES` | DETECT | IMPLEMENTED | WEAK | R-03 |
| `CTL-ALERTING-PROD` | DETECT | FAILED | FAILED | R-03 |
| `CTL-TLS-PROD` | PREVENT | FAILED | FAILED | R-01 |
| `CTL-SECRETS-PROD` | PREVENT | FAILED | FAILED | R-01 |
| `CTL-BACKUP-DRILL` | RECOVER | TESTED | WEAK | R-02 |
| `CTL-IMMUTABLE-SHA` | PREVENT | FAILED | FAILED | R-06 |
| `CTL-AI-ASSIST-AUTH` | PREVENT | TESTED | WEAK | R-04 |
| `CTL-AUTONOMY-GATE` | PREVENT | IMPLEMENTED | CANDIDATE | R-04 |
| `CTL-DSAR-RUNTIME` | DETECT | FAILED | FAILED | R-05 |
| `CTL-CVE-PROGRAM` | DETECT | FAILED | FAILED | (supply chain — no inventory run) |

UNCONTROLLED: **R-07**. WEAK: R-01…R-04. FAILED controls: G23/G26/G25/G19. OVER_CONTROLLED: **none evidenced** (do not invent).
