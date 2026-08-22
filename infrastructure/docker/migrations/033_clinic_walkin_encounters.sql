-- Clinic P0 — schema bootstrap + walk-in encounters (appointment_id optional).
-- Previously assumed clinic.encounters already existed; no prior CREATE SCHEMA clinic.

CREATE SCHEMA IF NOT EXISTS clinic;

CREATE TABLE IF NOT EXISTS clinic.patients (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    patient_number VARCHAR(32) NOT NULL,
    first_name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64) NOT NULL,
    date_of_birth DATE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, patient_number)
);

CREATE INDEX IF NOT EXISTS idx_clinic_patients_tenant
    ON clinic.patients (tenant_id);

CREATE TABLE IF NOT EXISTS clinic.appointments (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    patient_id UUID NOT NULL,
    provider_name VARCHAR(128) NOT NULL,
    scheduled_at TIMESTAMPTZ NOT NULL,
    status VARCHAR(32) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_clinic_appointments_tenant_patient
    ON clinic.appointments (tenant_id, patient_id);

CREATE TABLE IF NOT EXISTS clinic.encounters (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    patient_id UUID NOT NULL,
    appointment_id UUID,
    status VARCHAR(32) NOT NULL,
    diagnosis_codes JSONB NOT NULL DEFAULT '[]',
    started_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_clinic_encounters_tenant
    ON clinic.encounters (tenant_id);

CREATE TABLE IF NOT EXISTS clinic.referrals (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    encounter_id UUID NOT NULL,
    patient_id UUID NOT NULL,
    target_specialty VARCHAR(128) NOT NULL,
    reason TEXT NOT NULL,
    status VARCHAR(32) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    sent_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_clinic_referrals_tenant_encounter
    ON clinic.referrals (tenant_id, encounter_id);

-- Walk-in: appointment_id may be NULL (no-op if already nullable)
ALTER TABLE clinic.encounters
    ALTER COLUMN appointment_id DROP NOT NULL;
