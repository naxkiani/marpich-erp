-- Clinic P0 — allow walk-in encounters without appointment
ALTER TABLE clinic.encounters
    ALTER COLUMN appointment_id DROP NOT NULL;
