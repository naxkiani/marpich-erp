-- Enterprise Identity Graph — relationship edges between principals
-- Migration 021 — isolated schema (not identity.* user tables)

CREATE SCHEMA IF NOT EXISTS identity_graph;

CREATE TABLE IF NOT EXISTS identity_graph.nodes (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    node_ref VARCHAR(64) NOT NULL,
    node_type VARCHAR(32) NOT NULL,
    principal_id VARCHAR(128),
    label VARCHAR(256) NOT NULL DEFAULT '',
    attributes JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, node_ref)
);

CREATE INDEX IF NOT EXISTS idx_idgraph_nodes_principal
    ON identity_graph.nodes (tenant_id, principal_id);
CREATE INDEX IF NOT EXISTS idx_idgraph_nodes_type
    ON identity_graph.nodes (tenant_id, node_type);

CREATE TABLE IF NOT EXISTS identity_graph.edges (
    tenant_id VARCHAR(63) NOT NULL,
    id UUID NOT NULL,
    edge_ref VARCHAR(64) NOT NULL,
    source_node_ref VARCHAR(64) NOT NULL,
    target_node_ref VARCHAR(64) NOT NULL,
    relation VARCHAR(64) NOT NULL,
    weight NUMERIC(8, 4) NOT NULL DEFAULT 1,
    attributes JSONB NOT NULL DEFAULT '{}',
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, id),
    UNIQUE (tenant_id, edge_ref)
);

CREATE INDEX IF NOT EXISTS idx_idgraph_edges_source
    ON identity_graph.edges (tenant_id, source_node_ref, relation);
CREATE INDEX IF NOT EXISTS idx_idgraph_edges_target
    ON identity_graph.edges (tenant_id, target_node_ref, relation);

ALTER TABLE identity_graph.nodes ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_graph.edges ENABLE ROW LEVEL SECURITY;

DO $$ BEGIN
    CREATE POLICY idgraph_nodes_tenant ON identity_graph.nodes
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY idgraph_edges_tenant ON identity_graph.edges
        USING (tenant_id = current_setting('app.tenant_id', true));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
