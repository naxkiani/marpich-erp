-- Treasury liquidity and reconciliation satellites
-- Document JSONB + indexed lookup columns.

CREATE SCHEMA IF NOT EXISTS treasury;

CREATE TABLE IF NOT EXISTS treasury.cash_pools (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    code VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    document JSONB NOT NULL DEFAULT '{}',
    UNIQUE (tenant_id, code)
);

CREATE INDEX IF NOT EXISTS ix_treasury_cash_pools_tenant_status
    ON treasury.cash_pools (tenant_id, status);

CREATE TABLE IF NOT EXISTS treasury.liquidity_snapshots (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    period_type VARCHAR(32) NOT NULL,
    as_of_date VARCHAR(32) NOT NULL,
    document JSONB NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS ix_treasury_liquidity_snapshots_tenant_period_date
    ON treasury.liquidity_snapshots (tenant_id, period_type, as_of_date);

CREATE TABLE IF NOT EXISTS treasury.funding_needs (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'open',
    document JSONB NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS ix_treasury_funding_needs_tenant_status
    ON treasury.funding_needs (tenant_id, status);

CREATE TABLE IF NOT EXISTS treasury.bank_statement_imports (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    treasury_account_id VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'imported',
    document JSONB NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS ix_treasury_bank_statement_imports_account
    ON treasury.bank_statement_imports (tenant_id, treasury_account_id, status);

CREATE TABLE IF NOT EXISTS treasury.bank_reconciliations (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    treasury_account_id VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'draft',
    document JSONB NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS ix_treasury_bank_reconciliations_account
    ON treasury.bank_reconciliations (tenant_id, treasury_account_id, status);

CREATE TABLE IF NOT EXISTS treasury.bank_reconciliation_audits (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    reconciliation_id VARCHAR(64) NOT NULL,
    document JSONB NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS ix_treasury_bank_reconciliation_audits_reconciliation
    ON treasury.bank_reconciliation_audits (tenant_id, reconciliation_id);

CREATE TABLE IF NOT EXISTS treasury.cash_reconciliation_runs (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    location_id VARCHAR(64) NOT NULL,
    branch_id VARCHAR(64),
    status VARCHAR(32) NOT NULL DEFAULT 'draft',
    document JSONB NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS ix_treasury_cash_reconciliation_runs_location
    ON treasury.cash_reconciliation_runs (tenant_id, location_id, status);
CREATE INDEX IF NOT EXISTS ix_treasury_cash_reconciliation_runs_branch
    ON treasury.cash_reconciliation_runs (tenant_id, branch_id);

CREATE TABLE IF NOT EXISTS treasury.cash_reconciliation_audits (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    reconciliation_id VARCHAR(64) NOT NULL,
    document JSONB NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS ix_treasury_cash_reconciliation_audits_reconciliation
    ON treasury.cash_reconciliation_audits (tenant_id, reconciliation_id);
