-- Wave 02 — Procurement goods receipt (CAP-ENT-040) closes loop to inventory restock
ALTER TABLE procurement.requisitions
    ADD COLUMN IF NOT EXISTS received_at TIMESTAMPTZ;
