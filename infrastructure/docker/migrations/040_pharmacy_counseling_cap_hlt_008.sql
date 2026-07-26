-- CAP-HLT-008 depth: counseling columns on pharmacy.prescriptions
ALTER TABLE pharmacy.prescriptions
    ADD COLUMN IF NOT EXISTS counseling_notes TEXT,
    ADD COLUMN IF NOT EXISTS counselled_at TIMESTAMPTZ;
