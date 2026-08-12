-- Wave 02 — Sales (CAP-ENT-002) quotations + orders (from CRM won opportunities)
CREATE SCHEMA IF NOT EXISTS sales;

CREATE TABLE IF NOT EXISTS sales.quotations (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    contact_id UUID NOT NULL,
    opportunity_id UUID,
    title VARCHAR(256) NOT NULL,
    amount NUMERIC(18, 4) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    status VARCHAR(32) NOT NULL DEFAULT 'draft',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    sent_at TIMESTAMPTZ,
    accepted_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS ix_sales_quotations_tenant
    ON sales.quotations (tenant_id, status);
CREATE INDEX IF NOT EXISTS ix_sales_quotations_opportunity
    ON sales.quotations (tenant_id, opportunity_id);

CREATE TABLE IF NOT EXISTS sales.orders (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    contact_id UUID NOT NULL,
    quotation_id UUID,
    opportunity_id UUID,
    title VARCHAR(256) NOT NULL,
    amount NUMERIC(18, 4) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    status VARCHAR(32) NOT NULL DEFAULT 'confirmed',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_sales_orders_tenant
    ON sales.orders (tenant_id, status);
