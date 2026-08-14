-- Wave 02 — Tax liabilities + returns (CAP-ENT-026)
CREATE SCHEMA IF NOT EXISTS tax;

CREATE TABLE IF NOT EXISTS tax.liabilities (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    payroll_run_id UUID NOT NULL,
    period_label VARCHAR(64) NOT NULL,
    taxable_base NUMERIC(18, 4) NOT NULL,
    tax_amount NUMERIC(18, 4) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    status VARCHAR(32) NOT NULL DEFAULT 'open',
    correlation_id VARCHAR(64) NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS ix_tax_liabilities_tenant_run
    ON tax.liabilities (tenant_id, payroll_run_id);
CREATE INDEX IF NOT EXISTS ix_tax_liabilities_tenant_status
    ON tax.liabilities (tenant_id, status);

CREATE TABLE IF NOT EXISTS tax.returns (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    period_label VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'draft',
    liability_ids JSONB NOT NULL DEFAULT '[]'::jsonb,
    total_tax NUMERIC(18, 4) NOT NULL DEFAULT 0,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    correlation_id VARCHAR(64) NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    filed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS ix_tax_returns_tenant_status
    ON tax.returns (tenant_id, status);
