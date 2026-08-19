# MEOS Performance Standard (execution overlay)

**Date:** 2026-08-18T13:50:00Z  
**Engineering law (do not duplicate):** [docs/architecture/PERFORMANCE_STANDARD.md](../../architecture/PERFORMANCE_STANDARD.md)  
**Production health SoR:** [MEOS_PRODUCTION_HEALTH.md](./MEOS_PRODUCTION_HEALTH.md)  
**Operating overlay:** [MEOS_OPERATING_PERFORMANCE.md](./MEOS_OPERATING_PERFORMANCE.md)

This file is **measurement state**, not a second APM/monitoring product.

## Production performance (actual)

| Signal | Production | Local (do not reuse as current prod) |
|--------|------------|--------------------------------------|
| LATENCY | **NOT_MEASURED** | P313 G22 health p95 **81.4ms** (SAMPLES=8) **LOCAL_ONLY / STALE_FOR_P331** |
| THROUGHPUT | **NOT_MEASURED** | **NOT_MEASURED** |
| ERROR_RATE | **NOT_MEASURED** | Baseline HTTP 200 on those 8 samples — not a soak |
| AVAILABILITY | **NOT_MEASURED** | Workstation `/health` is not a prod SLO |
| QUEUE_DEPTH | **NOT_MEASURED** | **NOT_MEASURED** |
| DATABASE_PERFORMANCE | **NOT_MEASURED** | Demo `:5433` not production |
| API_PERFORMANCE | **NOT_MEASURED** | CRM list 39.8ms / search 68.2ms **LOCAL_ONLY** |
| PAGE_PERFORMANCE | **NOT_MEASURED** | Playwright **FAIL** (G20) |
| WORKFLOW_DURATION | **NOT_MEASURED** | **NOT_MEASURED** |

**Law:** Historical local p95 must **not** be reused as P331 production performance without a new measure on a real cluster.

SLO: reliability standard still has **no published SLA**. Candidate SLIs remain unobserved.

Service/application/tenant performance: **UNKNOWN** / **NOT_MEASURED**. No second telemetry collector.
