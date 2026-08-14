-- Wave 02 — Human Resources employees (CAP-ENT-010)
CREATE SCHEMA IF NOT EXISTS human_resources;

CREATE TABLE IF NOT EXISTS human_resources.employees (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    email VARCHAR(256) NOT NULL,
    full_name VARCHAR(128) NOT NULL,
    job_title VARCHAR(128) NOT NULL DEFAULT '',
    department VARCHAR(128) NOT NULL DEFAULT '',
    employee_number VARCHAR(64) NOT NULL DEFAULT '',
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    hired_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    terminated_at TIMESTAMPTZ,
    termination_reason VARCHAR(512) NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS ix_hr_employees_tenant_email
    ON human_resources.employees (tenant_id, email);
CREATE INDEX IF NOT EXISTS ix_hr_employees_tenant_status
    ON human_resources.employees (tenant_id, status);
