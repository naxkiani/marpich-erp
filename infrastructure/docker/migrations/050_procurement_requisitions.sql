-- Wave 02 — Procurement requisitions (CAP-ENT-040) from inventory.reorder.triggered
CREATE SCHEMA IF NOT EXISTS procurement;

CREATE TABLE IF NOT EXISTS procurement.requisitions (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    sku VARCHAR(64) NOT NULL,
    quantity NUMERIC(18, 4) NOT NULL,
    quantity_available NUMERIC(18, 4) NOT NULL,
    reorder_threshold NUMERIC(18, 4) NOT NULL,
    stock_id UUID,
    status VARCHAR(32) NOT NULL DEFAULT 'draft',
    reason VARCHAR(256) NOT NULL DEFAULT '',
    correlation_id VARCHAR(64) NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    submitted_at TIMESTAMPTZ,
    approved_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS ix_procurement_requisitions_tenant
    ON procurement.requisitions (tenant_id, status);
