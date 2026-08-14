-- Treasury money-path — accounts, transfers, cash, bank accounts

CREATE SCHEMA IF NOT EXISTS treasury;

CREATE TABLE IF NOT EXISTS treasury.accounts (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    code VARCHAR(64) NOT NULL,
    account_type VARCHAR(32) NOT NULL,
    currency VARCHAR(8) NOT NULL DEFAULT 'USD',
    document JSONB NOT NULL DEFAULT '{}',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, code)
);

CREATE TABLE IF NOT EXISTS treasury.transfers (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    reference VARCHAR(128) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'draft',
    from_account_id VARCHAR(64) NOT NULL,
    to_account_id VARCHAR(64) NOT NULL,
    document JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, reference)
);

CREATE INDEX IF NOT EXISTS ix_treasury_transfers_tenant_status
    ON treasury.transfers (tenant_id, status);

CREATE TABLE IF NOT EXISTS treasury.cash_locations (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    code VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    currency VARCHAR(8) NOT NULL DEFAULT 'USD',
    document JSONB NOT NULL DEFAULT '{}',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, code)
);

CREATE TABLE IF NOT EXISTS treasury.cash_transactions (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    location_id VARCHAR(64) NOT NULL,
    transaction_type VARCHAR(32) NOT NULL,
    document JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_treasury_cash_tx_location
    ON treasury.cash_transactions (tenant_id, location_id);

CREATE TABLE IF NOT EXISTS treasury.bank_accounts (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    bank_id VARCHAR(64) NOT NULL,
    code VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'draft',
    currency VARCHAR(8) NOT NULL DEFAULT 'USD',
    document JSONB NOT NULL DEFAULT '{}',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, code)
);

CREATE INDEX IF NOT EXISTS ix_treasury_bank_accounts_bank
    ON treasury.bank_accounts (tenant_id, bank_id);
