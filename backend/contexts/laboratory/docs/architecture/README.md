# Laboratory Architecture Brief — CAP-HLT-007

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

| Event | When |
|-------|------|
| `laboratory.order.placed` | Order created |
| `laboratory.sample.received` | Sample accessioned |
| `laboratory.result.available` | Result finalized (hospital/clinic ACL → care timeline) |

## API

- `POST /api/v1/laboratory/orders`
- `POST /api/v1/laboratory/samples`
- `POST /api/v1/laboratory/orders/{id}/results`
- Paginated `GET` lists (limit ≤ 100)

## UI

Admin `/healthcare/laboratory` — StepProgress order→sample→result desk.
