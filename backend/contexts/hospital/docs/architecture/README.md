# Hospital P0 Architecture Brief — CAP-HLT-001

**Domain type:** Core Domain (industry) — acute hospital  
**Must not merge with:** clinic, laboratory, pharmacy

## Capability → aggregates

| Capability | Aggregate |
|------------|-----------|
| CAP-HLT-001 Patient Lifecycle (acute) | Patient, Admission |
| CAP-HLT-005 Clinical Encounter | Encounter |

Bed / ClinicalOrder remain future (CAP-HLT-004) — yaml stubs only.

## Lifecycle

`register patient → admit (ward) → start encounter → complete encounter`

No clinic-style walk-in encounters.

## Core reuse

- Identity: `hospital_staff` via `POST /identity/personas/hospital/seed`
- Documents / Workflow / Audit via platform events
- Events: `hospital.patient.registered`, `hospital.admission.registered`,
  `hospital.encounter.started`, `hospital.encounter.completed`

## Lab result projection (ACL)

Subscribes to `laboratory.result.available` → local `lab_result_projections`
(peer `order_id` / `patient_ref` only). List: `GET /hospital/lab-results`.
Idempotent on `source_event_id`. Never merges laboratory or clinic schemas.
