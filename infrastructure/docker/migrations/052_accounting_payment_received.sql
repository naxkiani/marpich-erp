-- Wave 02 — AR payment received on issued invoices (CAP-ENT-023)
ALTER TABLE accounting.invoices
    ADD COLUMN IF NOT EXISTS paid_at TIMESTAMPTZ;
