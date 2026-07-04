-- Marpich ERP — Python bounded contexts (Hospital, Accounting, Finance)
-- Run after init-db.sql and 002_identity_full.sql

-- Normalize identity.users tenant column
DO $$ BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_schema = 'identity' AND table_name = 'users' AND column_name = 'tenant_slug'
  ) THEN
    ALTER TABLE identity.users RENAME COLUMN tenant_slug TO tenant_id;
  END IF;
END $$;

CREATE SCHEMA IF NOT EXISTS hospital;
CREATE SCHEMA IF NOT EXISTS accounting;
CREATE SCHEMA IF NOT EXISTS finance;

-- Identity: simplify RBAC for Python repos (permission_ids on roles, role_ids on users)
ALTER TABLE identity.roles
  ADD COLUMN IF NOT EXISTS permission_ids JSONB NOT NULL DEFAULT '[]';

ALTER TABLE identity.users
  ADD COLUMN IF NOT EXISTS role_ids JSONB NOT NULL DEFAULT '[]';

-- Hospital
CREATE TABLE IF NOT EXISTS hospital.patients (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    mrn VARCHAR(32) NOT NULL,
    first_name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64) NOT NULL,
    date_of_birth DATE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, mrn)
);

CREATE INDEX IF NOT EXISTS idx_hospital_patients_tenant ON hospital.patients(tenant_id);

CREATE TABLE IF NOT EXISTS hospital.admissions (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    patient_id UUID NOT NULL REFERENCES hospital.patients(id),
    ward VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    admitted_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_hospital_admissions_tenant ON hospital.admissions(tenant_id);

CREATE TABLE IF NOT EXISTS hospital.encounters (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    patient_id UUID NOT NULL,
    admission_id UUID NOT NULL REFERENCES hospital.admissions(id),
    status VARCHAR(32) NOT NULL DEFAULT 'in_progress',
    procedure_codes JSONB NOT NULL DEFAULT '[]',
    diagnosis_codes JSONB NOT NULL DEFAULT '[]',
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_hospital_encounters_tenant ON hospital.encounters(tenant_id);

-- Accounting
CREATE TABLE IF NOT EXISTS accounting.billing_encounters (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    external_encounter_id VARCHAR(64) NOT NULL,
    patient_ref UUID NOT NULL,
    procedure_codes JSONB NOT NULL DEFAULT '[]',
    line_items JSONB NOT NULL DEFAULT '[]',
    total_amount NUMERIC(14, 2) NOT NULL,
    currency VARCHAR(8) NOT NULL DEFAULT 'USD',
    status VARCHAR(32) NOT NULL DEFAULT 'pending',
    correlation_id VARCHAR(64) NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, external_encounter_id)
);

CREATE INDEX IF NOT EXISTS idx_accounting_billing_tenant ON accounting.billing_encounters(tenant_id);

-- Finance
CREATE TABLE IF NOT EXISTS finance.accounts (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    code VARCHAR(16) NOT NULL,
    name VARCHAR(128) NOT NULL,
    account_type VARCHAR(32) NOT NULL,
    balance NUMERIC(14, 2) NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, code)
);

CREATE INDEX IF NOT EXISTS idx_finance_accounts_tenant ON finance.accounts(tenant_id);

CREATE TABLE IF NOT EXISTS finance.fiscal_periods (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    name VARCHAR(64) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(16) NOT NULL DEFAULT 'open',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    closed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_finance_periods_tenant ON finance.fiscal_periods(tenant_id);

CREATE TABLE IF NOT EXISTS finance.journal_entries (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    external_journal_id VARCHAR(64) NOT NULL,
    source_type VARCHAR(64) NOT NULL,
    source_id VARCHAR(64) NOT NULL,
    currency VARCHAR(8) NOT NULL DEFAULT 'USD',
    lines JSONB NOT NULL DEFAULT '[]',
    correlation_id VARCHAR(64) NOT NULL DEFAULT '',
    posted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, external_journal_id)
);

CREATE INDEX IF NOT EXISTS idx_finance_journals_tenant ON finance.journal_entries(tenant_id);
CREATE INDEX IF NOT EXISTS idx_finance_journals_source ON finance.journal_entries(tenant_id, source_type, source_id);

-- Platform tenant registry: align slug column naming for Python repos
DO $$ BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_schema = 'tenant' AND table_name = 'tenants' AND column_name = 'tenant_slug'
  ) THEN
    NULL;
  END IF;
END $$;
