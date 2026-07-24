# Hospital Architecture Brief — CAP-HLT-001 / 004 / 005

**Domain type:** Core Domain (industry) — acute hospital  
**Must not merge with:** clinic, laboratory, pharmacy

## Capability → aggregates

| Capability | Aggregate |
|------------|-----------|
| CAP-HLT-001 Patient Lifecycle (acute) | Patient, Admission |
| CAP-HLT-004 Admission & Bed Management | Bed, Admission (assign/transfer/discharge) |
| CAP-HLT-005 Clinical Encounter | Encounter |

Local projections (peer IDs only): `CareEventProjection` from `laboratory.result.available` / `pharmacy.dispense.completed`.

ClinicalOrder / CAP-HLT-010 radiology remain future.

## Lifecycle

`register patient → create bed → admit (+ optional bed) → assign/transfer → encounter → discharge`

No clinic-style walk-in encounters. Discharge releases occupied beds.

## Events

**Publishes:** `hospital.patient.registered` · `hospital.admission.registered` · `hospital.bed.assigned` ·
`hospital.admission.transferred` · `hospital.admission.discharged` ·
`hospital.encounter.started` · `hospital.encounter.completed`

**Subscribes:** `laboratory.result.available` · `pharmacy.dispense.completed` (ACL → `CareEventProjection`)

## Demo UI (P11)

Admin portal encounters tab: **Seed care events** calls Lab/Pharmacy HTTP APIs with peer
`patient_ref` (+ selected encounter when set). Fresh `uniqueKey` per click; timeline refreshes via ACL.
Hospital never imports laboratory/pharmacy domains.

## Persistence

Schema `hospital.*` — patients, admissions (`bed_id`, `discharged_at`), beds, encounters,
`care_event_projections` (unique `(tenant_id, source_event_id)`).  
Migrations: `036_hospital_beds_cap_hlt_004.sql`, `038_hospital_care_event_projections.sql`.  
Memory default; Postgres via `use_postgres()`.

## Core reuse

- Identity: `hospital_staff` (+ `hospital.beds.*`)
- Workflow / Audit / Notifications via integration events
- API: `GET /api/v1/hospital/care-events`
## Demo care seed (UI)

After hospital catalog seed, Connect orchestrates Laboratory/Pharmacy HTTP APIs with real
patient UUIDs so care-event projections fill — no hospital→lab domain imports.
