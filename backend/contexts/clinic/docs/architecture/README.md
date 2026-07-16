# Clinic P0 Architecture Brief — CAP-HLT-002 / CAP-HLT-003

**Domain type:** Core Domain (industry) — outpatient clinic  
**Must not merge with:** hospital, laboratory, pharmacy

## Capability → aggregates

| Capability | Aggregate |
|------------|-----------|
| CAP-HLT-002 Outpatient Care | ClinicPatient, OutpatientEncounter |
| CAP-HLT-003 Appointments | Appointment |
| CAP-HLT-006 Referrals | Referral |

## Core reuse

- Identity: `clinic_staff` persona (`POST /identity/personas/clinic/seed`)
- Documents: store `document_id` on patient only
- Audit: integration events → Audit Platform
- Gateway: `X-Tenant-ID` + permissions

## Events

- `clinic.patient.registered`
- `clinic.appointment.scheduled`
- `clinic.encounter.completed`
- `clinic.referral.sent`

## API

`/api/v1/clinic/patients|appointments|encounters|referrals|lab-results`

Walk-in encounters: `POST /encounters` with `patient_id` (no appointment).

## Lab result projection (ACL)

Subscribes to `laboratory.result.available` → local `clinic.lab_result_projections`
(peer IDs only). Idempotent on `source_event_id`. Never merges hospital or laboratory.
