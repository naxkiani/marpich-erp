# MEOS Data Rationalization Runbook

**Date:** 2026-08-19T06:20:00Z  
**P337 overlay.** Feeds **existing** P335/P336 items. **Not** a migration factory.

## Law

No automatic delete/consolidate. No destructive migration without authorization. Static inventory ≠ retire production (0 ACTIVE apps).

## Recommendations (evidence)

| Class | Action | Evidence | Risk | Value |
|-------|--------|----------|------|-------|
| OLTP schemas in use | **RETAIN** | 223 tables; Wave 02 TESTED | R-01 | NOT_MEASURED |
| P212 catalogs | **RETAIN_AS_DESIGNED** | in-memory catalog API | false ACTIVE | NOT_MEASURED |
| Empty industry apps | **FREEZE** | P336 | catalog honesty | NOT_MEASURED |
| Unpublished products | **DO_NOT_PUBLISH** | count 0 | — | — |
| TS vs Python identity data | **CONSOLIDATE** later | P336 FULL_DUPLICATION | dual SoR | NOT_MEASURED |

`retirement_candidates: []`.

## Priority into P335

1. INIT-G26 — production data plane  
2. INIT-G19 — DSAR/erasure before prod PII  
3. TD-EVENT-PAYLOAD-SCHEMA — event contract honesty  

No new data platform initiative.
