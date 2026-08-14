-- Wave 02 — Payroll employees projection + runs (CAP-ENT-015)
CREATE SCHEMA IF NOT EXISTS payroll;

CREATE TABLE IF NOT EXISTS payroll.employees (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    hr_employee_id UUID NOT NULL,
    email VARCHAR(256) NOT NULL,
    full_name VARCHAR(128) NOT NULL,
    job_title VARCHAR(128) NOT NULL DEFAULT '',
    department VARCHAR(128) NOT NULL DEFAULT '',
    employee_number VARCHAR(64) NOT NULL DEFAULT '',
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    base_salary NUMERIC(18, 4) NOT NULL DEFAULT 5000,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS ix_payroll_employees_tenant_hr
    ON payroll.employees (tenant_id, hr_employee_id);
CREATE INDEX IF NOT EXISTS ix_payroll_employees_tenant_status
    ON payroll.employees (tenant_id, status);

CREATE TABLE IF NOT EXISTS payroll.runs (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    period_label VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'draft',
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    total_gross NUMERIC(18, 4) NOT NULL DEFAULT 0,
    total_net NUMERIC(18, 4) NOT NULL DEFAULT 0,
    payslips JSONB NOT NULL DEFAULT '[]'::jsonb,
    correlation_id VARCHAR(64) NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS ix_payroll_runs_tenant_status
    ON payroll.runs (tenant_id, status);
