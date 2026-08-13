# Pharmacy P0 Architecture Brief — CAP-HLT-008

**Domain type:** Industry Core (healthcare) — Dispensing  
**Must not merge with:** hospital, clinic, laboratory

## Capability → aggregates

| Capability | Aggregate |
|------------|-----------|
| CAP-HLT-008 Pharmacy / Dispense | Prescription, DispenseRecord |

Deferred: DrugInteraction engine; stock owned by Inventory.

## Lifecycle

`receive prescription → dispense`

Peer `patient_ref` only — never shared EMR patient tables.

## Persistence

- Schema: `pharmacy` (migration `039_laboratory_pharmacy_postgres.sql`)
- Adapters: `memory_store` (default/tests) · `postgres_store` when `use_postgres()`

## Events

Publishes: `pharmacy.prescription.received` · `pharmacy.dispense.completed`  
Subscribes (ACL): `hospital.encounter.completed` · `inventory.stock.adjusted`  
→ idempotent REVIEW Rx on encounter completed; stock facts noted (no inventory schema reads)
