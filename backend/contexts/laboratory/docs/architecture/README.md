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
