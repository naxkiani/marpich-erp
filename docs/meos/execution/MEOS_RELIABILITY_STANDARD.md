# MEOS Reliability Standard

**Date:** 2026-08-18T12:05:00Z  
**SoR for live SRE:** [MEOS_P316_SRE_OPERATIONS.md](./MEOS_P316_SRE_OPERATIONS.md) — **NOT STARTED** (no production).  
**Health table:** [MEOS_PRODUCTION_HEALTH.md](./MEOS_PRODUCTION_HEALTH.md) — all **NOT_AVAILABLE**.  
**Law:** Do not invent SLOs, SLAs, error budgets, or reliability scores.  
**P328 companion:** [MEOS_RESILIENCE_STANDARD.md](./MEOS_RESILIENCE_STANDARD.md) — production RTO/RPO **NOT_VERIFIED**.

## Production precondition

Continuous reliability engineering applies **after** `PRODUCTION_ACTIVE`.  
P314 `GO_LIVE = NOT APPROVED`. P324 `NOT_RELEASE_CANDIDATE`. Therefore this standard is **governance**, not a live SLO contract.

## Candidate SLIs (not commitments)

These are the signals to use **when** production telemetry exists. They are **not** published SLAs.

| SLI | Source when live | Production observation |
|-----|------------------|------------------------|
| Availability | `/api/v1/ready` success ratio | **NOT_MEASURED** |
| Latency | p95 on authenticated APIs | **NOT_MEASURED** |
| Error rate | 5xx / total | **NOT_MEASURED** |
| Data freshness | outbox unpublished age | **NOT_MEASURED** |
| Backup success | scheduled job | **NOT_MEASURED** |

Workstation P313 samples (health p95 **81.4ms**, etc.) are **LOCAL_ONLY**. They are not production SLOs and are **not** error-budget inputs.  
**P331:** those samples are **STALE_FOR_P331** — do not reuse as current production latency.

## Error budget

**NOT_CALCULATED.** No SLO target exists to subtract from.

## Incidents

Production incident count: **none evidenced** (no production traffic). Do not invent post-mortems.  
Playbooks exist in operations docs; **IR is not active**.

## Reliability score

**NOT_MEASURED.** Do not average NOT_AVAILABLE into a fake 0–100 score.
