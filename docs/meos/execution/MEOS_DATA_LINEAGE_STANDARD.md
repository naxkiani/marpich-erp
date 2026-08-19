# MEOS Data Lineage Standard

**Date:** 2026-08-19T06:20:00Z  
**Reuse** event schemas, OpenAPI, analytics graph catalog. **Not** a new lineage product.

## Law

Field-level SOURCE → TRANSFORM → PRODUCT → APPLICATION → DECISION is required for production claims. Missing hops → **LINEAGE_INCOMPLETE**. AI-suggested edges → **INFERRED_UNVERIFIED** until human validation.

## Current state

| Hop | Actual |
|-----|--------|
| SQL migrations | Present (55) — schema change history, not runtime lineage |
| Integration events | JSON schemas (47) — **TD-EVENT-PAYLOAD-SCHEMA** open |
| Analytics `/graph/lineage` | Catalog surface |
| Production pipeline lineage | **NOT_AVAILABLE** |

Overall: **LINEAGE_INCOMPLETE**. Do not draw fake graphs on the executive home.
