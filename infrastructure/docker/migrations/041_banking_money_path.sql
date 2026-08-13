-- Banking money-path — customer / product / account / payment_transfer
-- Document JSONB + indexed lookup columns (mirror financial_kernel 040).

CREATE SCHEMA IF NOT EXISTS banking;

CREATE TABLE IF NOT EXISTS banking.customers (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    email VARCHAR(256) NOT NULL,
    document JSONB NOT NULL DEFAULT '{}',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, email)
);

CREATE TABLE IF NOT EXISTS banking.account_products (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    product_code VARCHAR(64) NOT NULL,
    document JSONB NOT NULL DEFAULT '{}',
    UNIQUE (tenant_id, product_code)
);

CREATE TABLE IF NOT EXISTS banking.accounts (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    customer_id VARCHAR(64) NOT NULL,
    account_number VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'pending',
    document JSONB NOT NULL DEFAULT '{}',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, account_number)
);

CREATE INDEX IF NOT EXISTS ix_banking_accounts_tenant_customer
    ON banking.accounts (tenant_id, customer_id);

CREATE TABLE IF NOT EXISTS banking.payment_transfers (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    transfer_ref VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'draft',
    source_account_id VARCHAR(64) NOT NULL,
    customer_id VARCHAR(64) NOT NULL,
    batch_id VARCHAR(64),
    document JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, transfer_ref)
);

CREATE INDEX IF NOT EXISTS ix_banking_transfers_tenant_status
    ON banking.payment_transfers (tenant_id, status);
CREATE INDEX IF NOT EXISTS ix_banking_transfers_batch
    ON banking.payment_transfers (batch_id);
