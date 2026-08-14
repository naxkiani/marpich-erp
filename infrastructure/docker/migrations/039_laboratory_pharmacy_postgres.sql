-- CAP-HLT-007 Laboratory + CAP-HLT-008 Pharmacy Postgres schemas
-- Tenant-isolated; peer patient_ref / encounter_ref only — no cross-schema FKs.

CREATE SCHEMA IF NOT EXISTS laboratory;
CREATE SCHEMA IF NOT EXISTS pharmacy;

CREATE TABLE IF NOT EXISTS laboratory.test_orders (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    order_number VARCHAR(64) NOT NULL,
    patient_ref VARCHAR(128) NOT NULL,
    test_code VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'ordered',
    result_value VARCHAR(256),
    result_unit VARCHAR(64),
    source_encounter_ref VARCHAR(128),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finalized_at TIMESTAMPTZ,
    UNIQUE (tenant_id, order_number)
);

CREATE INDEX IF NOT EXISTS ix_laboratory_test_orders_tenant_created
    ON laboratory.test_orders (tenant_id, created_at DESC);
CREATE INDEX IF NOT EXISTS ix_laboratory_test_orders_tenant_patient
    ON laboratory.test_orders (tenant_id, patient_ref);

CREATE TABLE IF NOT EXISTS laboratory.samples (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    order_id UUID NOT NULL,
    accession_number VARCHAR(64) NOT NULL,
    specimen_type VARCHAR(64) NOT NULL,
    patient_ref VARCHAR(128) NOT NULL,
    received_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, accession_number)
);

CREATE INDEX IF NOT EXISTS ix_laboratory_samples_tenant_order
    ON laboratory.samples (tenant_id, order_id);
CREATE INDEX IF NOT EXISTS ix_laboratory_samples_tenant_received
    ON laboratory.samples (tenant_id, received_at DESC);

CREATE TABLE IF NOT EXISTS pharmacy.prescriptions (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    rx_number VARCHAR(64) NOT NULL,
    patient_ref VARCHAR(128) NOT NULL,
    drug_code VARCHAR(64) NOT NULL,
    drug_name VARCHAR(256) NOT NULL,
    quantity NUMERIC(18, 4) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'received',
    source_encounter_ref VARCHAR(128),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, rx_number)
);

CREATE INDEX IF NOT EXISTS ix_pharmacy_prescriptions_tenant_created
    ON pharmacy.prescriptions (tenant_id, created_at DESC);
CREATE INDEX IF NOT EXISTS ix_pharmacy_prescriptions_tenant_patient
    ON pharmacy.prescriptions (tenant_id, patient_ref);

CREATE TABLE IF NOT EXISTS pharmacy.dispense_records (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    prescription_id UUID NOT NULL,
    patient_ref VARCHAR(128) NOT NULL,
    drug_code VARCHAR(64) NOT NULL,
    quantity_dispensed NUMERIC(18, 4) NOT NULL,
    dispensed_by VARCHAR(128),
    dispensed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_pharmacy_dispenses_tenant_rx
    ON pharmacy.dispense_records (tenant_id, prescription_id);
CREATE INDEX IF NOT EXISTS ix_pharmacy_dispenses_tenant_dispensed
    ON pharmacy.dispense_records (tenant_id, dispensed_at DESC);
