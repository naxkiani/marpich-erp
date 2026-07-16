# Pharmacy P0 Architecture Brief — CAP-HLT-008

**Domain type:** Industry Core (healthcare) — dispensing  
**Must not merge with:** hospital, clinic, laboratory

## Capability → aggregates

| Capability | Aggregate |
|------------|-----------|
| CAP-HLT-008 Pharmacy & Dispensing | Prescription, DispenseRecord |

Deferred: DrugInteraction, PharmacyStock (inventory owns stock rules).

## Lifecycle

`receive prescription (patient_ref) → dispense`

Peer patient IDs only — no shared patient tables with hospital/clinic.

## Events

`pharmacy.prescription.received` · `pharmacy.dispense.completed`

## Persistence

Postgres when `use_postgres()` — schemas `pharmacy.prescriptions` / `pharmacy.dispenses`
(migration `036_pharmacy_laboratory_postgres.sql`). Memory store otherwise.

## Cross-context ACL

Inventory subscribes to `pharmacy.dispense.completed` and decrements stock by
`drug_code` → SKU (idempotent on `dispense_id`). No shared tables; peer IDs only.
