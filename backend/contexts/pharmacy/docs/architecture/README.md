# Pharmacy Architecture Brief — CAP-HLT-008

**Domain type:** Industry Core (healthcare) — dispensing  
**Must not merge with:** hospital, clinic, laboratory

## Capability → aggregates

| Capability | Aggregate |
|------------|-----------|
| CAP-HLT-008 Pharmacy & Dispensing | Prescription, DispenseRecord |

Deferred: DrugInteraction, PharmacyStock (inventory owns stock rules).

## Lifecycle

`receive prescription (patient_ref) → dispense → counsel`

Peer patient IDs only — no shared patient tables with hospital/clinic.

## Events

| Event | When |
|-------|------|
| `pharmacy.prescription.received` | Rx intake |
| `pharmacy.dispense.completed` | Dispense recorded (hospital ACL → care timeline) |
| `pharmacy.counseling.completed` | Patient counseling after dispense |

## API

- `POST /api/v1/pharmacy/prescriptions`
- `POST /api/v1/pharmacy/dispenses`
- `POST /api/v1/pharmacy/prescriptions/{id}/counsel` — `pharmacy.counseling.write`
- Paginated `GET` lists

## Persistence

Migration `040_pharmacy_counseling_cap_hlt_008.sql` — counseling columns.

## UI

Admin `/healthcare/pharmacy` — StepProgress receive→dispense→counsel desk.
