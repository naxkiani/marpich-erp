-- Financial Kernel money-path (GL) — schema isolated from legacy finance.*
-- Document JSONB holds full aggregate; indexed columns support lookups.

CREATE SCHEMA IF NOT EXISTS financial_kernel;

CREATE TABLE IF NOT EXISTS financial_kernel.chart_of_accounts (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    code VARCHAR(64) NOT NULL,
    account_key VARCHAR(128),
    parent_account_id VARCHAR(64),
    tree_id VARCHAR(64),
    document JSONB NOT NULL DEFAULT '{}',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, code)
);

CREATE INDEX IF NOT EXISTS ix_fk_coa_tenant_key
    ON financial_kernel.chart_of_accounts (tenant_id, account_key);

CREATE TABLE IF NOT EXISTS financial_kernel.journals (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    idempotency_key VARCHAR(128) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'draft',
    period_id VARCHAR(64),
    posted_at TIMESTAMPTZ,
    document JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, idempotency_key)
);

CREATE INDEX IF NOT EXISTS ix_fk_journals_tenant_posted
    ON financial_kernel.journals (tenant_id, posted_at DESC);

CREATE TABLE IF NOT EXISTS financial_kernel.fiscal_years (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    name VARCHAR(128) NOT NULL,
    document JSONB NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS ix_fk_fy_tenant
    ON financial_kernel.fiscal_years (tenant_id);

CREATE TABLE IF NOT EXISTS financial_kernel.fiscal_periods (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    fiscal_year_id VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'open',
    organization_id VARCHAR(64),
    document JSONB NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS ix_fk_fp_tenant_status
    ON financial_kernel.fiscal_periods (tenant_id, status);
CREATE INDEX IF NOT EXISTS ix_fk_fp_tenant_year
    ON financial_kernel.fiscal_periods (tenant_id, fiscal_year_id);
