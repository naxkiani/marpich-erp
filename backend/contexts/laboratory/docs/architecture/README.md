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

## Events

`laboratory.sample.received` · `laboratory.result.available`

## Persistence

Postgres when `use_postgres()` — schemas `laboratory.test_orders` / `laboratory.samples`
(migration `036_pharmacy_laboratory_postgres.sql`). Memory store otherwise.

## Cross-context ACL

Hospital and clinic subscribe to `laboratory.result.available` and store **local**
projections (`hospital.lab_result_projections` / `clinic.lab_result_projections`) with
peer `order_id` + `patient_ref` only — never shared EMR patient tables. Idempotent on
`source_event_id`.
