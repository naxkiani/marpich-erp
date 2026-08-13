# Laboratory P0 Architecture Brief — CAP-HLT-007

**Domain type:** Industry Core (healthcare) — LIMS  
**Must not merge with:** hospital, clinic, pharmacy

## Capability → aggregates

| Capability | Aggregate |
|------------|-----------|
| CAP-HLT-007 Laboratory / LIMS | TestOrder, Sample |

Deferred: QualityControl, full instrument integration.

## Lifecycle

`place order → receive sample → finalize result`

Peer `patient_ref` only — never shared EMR patient tables.

## Persistence

- Schema: `laboratory` (migration `039_laboratory_pharmacy_postgres.sql`)
- Adapters: `memory_store` (default/tests) · `postgres_store` when `use_postgres()`

## Events

Publishes: `laboratory.sample.received` · `laboratory.result.available`  
Subscribes (ACL): `hospital.encounter.started` · `hospital.encounter.completed`  
→ idempotent REVIEW order on completed (`HOSP-{encounter}`) with `source_encounter_ref`
