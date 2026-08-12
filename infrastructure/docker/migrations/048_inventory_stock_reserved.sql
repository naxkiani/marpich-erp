-- Wave 02 — Inventory reservations (CAP-ENT-042) for sales.order.placed
ALTER TABLE inventory.stock_levels
    ADD COLUMN IF NOT EXISTS quantity_reserved NUMERIC(18, 4) NOT NULL DEFAULT 0;
