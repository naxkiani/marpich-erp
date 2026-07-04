# Clinic — ambulatory care bounded context

## Ubiquitous language

| Term | Definition |
|------|------------|
| **Patient** | Outpatient registered in the clinic (not hospital MRN) |
| **Appointment** | Scheduled visit with a provider |
| **Outpatient encounter** | Clinical visit tied to an appointment |
| **Referral** | Transfer request to another specialty or facility |

## Independence

- **Not** merged with `hospital` — separate schema `clinic_*`
- References hospital only via integration events (`clinic.referral.sent`)

## Permissions

- `clinic.patients.read` / `clinic.patients.write`
- `clinic.appointments.read` / `clinic.appointments.write`
- `clinic.encounters.read` / `clinic.encounters.write`
- `clinic.referrals.write`

## Events published

- `clinic.appointment.scheduled`
- `clinic.encounter.completed`
- `clinic.referral.sent`

## API

Prefix: `/api/v1/clinic`
