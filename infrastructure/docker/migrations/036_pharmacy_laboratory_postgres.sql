-- P5.4 — Pharmacy + Laboratory Postgres + hospital/clinic lab result projections

CREATE SCHEMA IF NOT EXISTS pharmacy;
CREATE SCHEMA IF NOT EXISTS laboratory;
CREATE SCHEMA IF NOT EXISTS clinic;

CREATE TABLE IF NOT EXISTS pharmacy.prescriptions (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    rx_number VARCHAR(32) NOT NULL,
    patient_ref VARCHAR(64) NOT NULL,
    drug_code VARCHAR(32) NOT NULL,
    drug_name VARCHAR(128) NOT NULL,
    quantity NUMERIC(18, 4) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'received',
    source_encounter_ref VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, rx_number)
);

CREATE TABLE IF NOT EXISTS pharmacy.dispenses (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    prescription_id UUID NOT NULL REFERENCES pharmacy.prescriptions(id) ON DELETE CASCADE,
    patient_ref VARCHAR(64) NOT NULL,
    drug_code VARCHAR(32) NOT NULL,
    quantity_dispensed NUMERIC(18, 4) NOT NULL,
    dispensed_by VARCHAR(64),
    dispensed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_pharmacy_prescriptions_tenant
    ON pharmacy.prescriptions (tenant_id);
CREATE INDEX IF NOT EXISTS idx_pharmacy_dispenses_tenant
    ON pharmacy.dispenses (tenant_id, dispensed_at);

CREATE TABLE IF NOT EXISTS laboratory.test_orders (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    order_number VARCHAR(32) NOT NULL,
    patient_ref VARCHAR(64) NOT NULL,
    test_code VARCHAR(32) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'ordered',
    result_value TEXT,
    result_unit VARCHAR(32),
    source_encounter_ref VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finalized_at TIMESTAMPTZ,
    UNIQUE (tenant_id, order_number)
);

CREATE TABLE IF NOT EXISTS laboratory.samples (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    order_id UUID NOT NULL REFERENCES laboratory.test_orders(id) ON DELETE CASCADE,
    accession_number VARCHAR(32) NOT NULL,
    specimen_type VARCHAR(64) NOT NULL,
    patient_ref VARCHAR(64) NOT NULL,
    received_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_laboratory_orders_tenant
    ON laboratory.test_orders (tenant_id);
CREATE INDEX IF NOT EXISTS idx_laboratory_samples_tenant
    ON laboratory.samples (tenant_id, received_at);

-- Local projections only (peer order_id / patient_ref — no cross-schema joins)
CREATE TABLE IF NOT EXISTS hospital.lab_result_projections (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    order_id VARCHAR(64) NOT NULL,
    patient_ref VARCHAR(64) NOT NULL,
    test_code VARCHAR(32) NOT NULL,
    result_value TEXT NOT NULL,
    result_unit VARCHAR(32),
    source_event_id VARCHAR(64) NOT NULL,
    projected_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, source_event_id)
);

CREATE TABLE IF NOT EXISTS clinic.lab_result_projections (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    order_id VARCHAR(64) NOT NULL,
    patient_ref VARCHAR(64) NOT NULL,
    test_code VARCHAR(32) NOT NULL,
    result_value TEXT NOT NULL,
    result_unit VARCHAR(32),
    source_event_id VARCHAR(64) NOT NULL,
    projected_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, source_event_id)
);

CREATE INDEX IF NOT EXISTS idx_hospital_lab_proj_tenant
    ON hospital.lab_result_projections (tenant_id, projected_at);
CREATE INDEX IF NOT EXISTS idx_clinic_lab_proj_tenant
    ON clinic.lab_result_projections (tenant_id, projected_at);
