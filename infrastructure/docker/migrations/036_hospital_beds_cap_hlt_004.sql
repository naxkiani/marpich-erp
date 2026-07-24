-- CAP-HLT-004 — Hospital beds + admission bed/discharge columns

CREATE TABLE IF NOT EXISTS hospital.beds (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    ward VARCHAR(64) NOT NULL,
    room VARCHAR(32) NOT NULL,
    bed_code VARCHAR(32) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'available',
    current_admission_id UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, ward, room, bed_code)
);

CREATE INDEX IF NOT EXISTS idx_hospital_beds_tenant_status
    ON hospital.beds (tenant_id, status);

ALTER TABLE hospital.admissions
    ADD COLUMN IF NOT EXISTS bed_id UUID,
    ADD COLUMN IF NOT EXISTS discharged_at TIMESTAMPTZ;

CREATE INDEX IF NOT EXISTS idx_hospital_admissions_tenant_status
    ON hospital.admissions (tenant_id, status);
CREATE INDEX IF NOT EXISTS idx_hospital_admissions_bed
    ON hospital.admissions (tenant_id, bed_id);
