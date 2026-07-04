-- Workflow schema
CREATE SCHEMA IF NOT EXISTS workflow;

CREATE TABLE IF NOT EXISTS workflow.process_definitions (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    key VARCHAR(64) NOT NULL,
    name VARCHAR(128) NOT NULL,
    version INT NOT NULL DEFAULT 1,
    steps JSONB NOT NULL DEFAULT '[]',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, key)
);

CREATE TABLE IF NOT EXISTS workflow.process_instances (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    definition_id UUID NOT NULL REFERENCES workflow.process_definitions(id) ON DELETE CASCADE,
    definition_key VARCHAR(64) NOT NULL,
    status VARCHAR(16) NOT NULL,
    current_step_index INT NOT NULL DEFAULT 0,
    context JSONB NOT NULL DEFAULT '{}',
    started_by VARCHAR(64) NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS workflow.tasks (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    instance_id UUID NOT NULL REFERENCES workflow.process_instances(id) ON DELETE CASCADE,
    step_key VARCHAR(64) NOT NULL,
    step_name VARCHAR(128) NOT NULL,
    assignee_id VARCHAR(64) NOT NULL,
    status VARCHAR(16) NOT NULL,
    outcome VARCHAR(16),
    comment TEXT NOT NULL DEFAULT '',
    delegated_from VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_workflow_defs_tenant ON workflow.process_definitions(tenant_id);
CREATE INDEX IF NOT EXISTS idx_workflow_instances_tenant ON workflow.process_instances(tenant_id);
CREATE INDEX IF NOT EXISTS idx_workflow_tasks_assignee ON workflow.tasks(tenant_id, assignee_id, status);
