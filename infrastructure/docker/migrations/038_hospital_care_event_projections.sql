-- Hospital care-event projections (lab/pharmacy ACL → local timeline).
-- Peer IDs + summary only — never laboratory/pharmacy aggregates.

CREATE TABLE IF NOT EXISTS hospital.care_event_projections (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    source_event_id VARCHAR(64) NOT NULL,
    source_context VARCHAR(64) NOT NULL,
    event_kind VARCHAR(32) NOT NULL,
    peer_id VARCHAR(64) NOT NULL,
    patient_id UUID NOT NULL,
    admission_id UUID,
    encounter_id UUID,
    summary JSONB NOT NULL DEFAULT '{}',
    correlation_id VARCHAR(64) NOT NULL DEFAULT '',
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, source_event_id)
);

CREATE INDEX IF NOT EXISTS ix_hospital_care_events_tenant_patient
    ON hospital.care_event_projections (tenant_id, patient_id);
CREATE INDEX IF NOT EXISTS ix_hospital_care_events_tenant_encounter
    ON hospital.care_event_projections (tenant_id, encounter_id);
CREATE INDEX IF NOT EXISTS ix_hospital_care_events_tenant_occurred
    ON hospital.care_event_projections (tenant_id, occurred_at DESC);
