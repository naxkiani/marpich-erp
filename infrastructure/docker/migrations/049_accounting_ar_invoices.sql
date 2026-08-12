-- Wave 02 — Accounting AR invoices (CAP-ENT-023) from sales.order.placed
CREATE SCHEMA IF NOT EXISTS accounting;

CREATE TABLE IF NOT EXISTS accounting.invoices (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    sales_order_id UUID NOT NULL,
    contact_id UUID NOT NULL,
    title VARCHAR(256) NOT NULL,
    amount NUMERIC(18, 4) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    status VARCHAR(32) NOT NULL DEFAULT 'draft',
    line_items JSONB NOT NULL DEFAULT '[]'::jsonb,
    correlation_id VARCHAR(64) NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    issued_at TIMESTAMPTZ
);

CREATE UNIQUE INDEX IF NOT EXISTS ix_accounting_invoices_order
    ON accounting.invoices (tenant_id, sales_order_id);
CREATE INDEX IF NOT EXISTS ix_accounting_invoices_tenant
    ON accounting.invoices (tenant_id, status);
