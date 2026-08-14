-- Banking deposit / loan money-path satellites
-- Document JSONB + indexed lookup columns (extends 041).

CREATE SCHEMA IF NOT EXISTS banking;

CREATE TABLE IF NOT EXISTS banking.deposit_profiles (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    account_id VARCHAR(64) NOT NULL,
    customer_id VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'pending_approval',
    document JSONB NOT NULL DEFAULT '{}',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_banking_deposit_profiles_tenant_account
    ON banking.deposit_profiles (tenant_id, account_id);
CREATE INDEX IF NOT EXISTS ix_banking_deposit_profiles_tenant_customer
    ON banking.deposit_profiles (tenant_id, customer_id);
CREATE INDEX IF NOT EXISTS ix_banking_deposit_profiles_tenant_status
    ON banking.deposit_profiles (tenant_id, status);

CREATE TABLE IF NOT EXISTS banking.deposit_transactions (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    deposit_id VARCHAR(64) NOT NULL,
    transaction_ref VARCHAR(64) NOT NULL,
    document JSONB NOT NULL DEFAULT '{}',
    UNIQUE (tenant_id, transaction_ref)
);

CREATE INDEX IF NOT EXISTS ix_banking_deposit_tx_deposit
    ON banking.deposit_transactions (tenant_id, deposit_id);

CREATE TABLE IF NOT EXISTS banking.deposit_accruals (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    deposit_id VARCHAR(64) NOT NULL,
    document JSONB NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS ix_banking_deposit_accruals_deposit
    ON banking.deposit_accruals (tenant_id, deposit_id);

CREATE TABLE IF NOT EXISTS banking.profit_rules (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    rule_code VARCHAR(64) NOT NULL,
    document JSONB NOT NULL DEFAULT '{}',
    UNIQUE (tenant_id, rule_code)
);

CREATE TABLE IF NOT EXISTS banking.loan_profiles (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    account_id VARCHAR(64) NOT NULL,
    loan_ref VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'draft',
    document JSONB NOT NULL DEFAULT '{}',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, loan_ref)
);

CREATE INDEX IF NOT EXISTS ix_banking_loan_profiles_tenant_account
    ON banking.loan_profiles (tenant_id, account_id);
CREATE INDEX IF NOT EXISTS ix_banking_loan_profiles_tenant_status
    ON banking.loan_profiles (tenant_id, status);

CREATE TABLE IF NOT EXISTS banking.loan_transactions (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    loan_id VARCHAR(64) NOT NULL,
    transaction_ref VARCHAR(64) NOT NULL,
    document JSONB NOT NULL DEFAULT '{}',
    UNIQUE (tenant_id, transaction_ref)
);

CREATE INDEX IF NOT EXISTS ix_banking_loan_tx_loan
    ON banking.loan_transactions (tenant_id, loan_id);

CREATE TABLE IF NOT EXISTS banking.loan_installments (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    loan_id VARCHAR(64) NOT NULL,
    document JSONB NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS ix_banking_loan_installments_loan
    ON banking.loan_installments (tenant_id, loan_id);

CREATE TABLE IF NOT EXISTS banking.loan_collaterals (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    loan_id VARCHAR(64) NOT NULL,
    document JSONB NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS ix_banking_loan_collaterals_loan
    ON banking.loan_collaterals (tenant_id, loan_id);

CREATE TABLE IF NOT EXISTS banking.loan_guarantors (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    loan_id VARCHAR(64) NOT NULL,
    document JSONB NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS ix_banking_loan_guarantors_loan
    ON banking.loan_guarantors (tenant_id, loan_id);

CREATE TABLE IF NOT EXISTS banking.loan_credit_risks (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    loan_id VARCHAR(64) NOT NULL,
    document JSONB NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS ix_banking_loan_credit_risks_loan
    ON banking.loan_credit_risks (tenant_id, loan_id);
