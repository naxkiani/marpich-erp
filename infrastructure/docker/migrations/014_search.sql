-- Search schema — event-driven index (Elasticsearch/OpenSearch in production)
CREATE SCHEMA IF NOT EXISTS search;

CREATE TABLE IF NOT EXISTS search.indices (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    entity_type VARCHAR(64) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    mapping JSONB NOT NULL DEFAULT '{}',
    document_count INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, entity_type)
);

CREATE TABLE IF NOT EXISTS search.documents (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    entity_type VARCHAR(64) NOT NULL,
    entity_id VARCHAR(128) NOT NULL,
    title VARCHAR(512) NOT NULL,
    body TEXT NOT NULL DEFAULT '',
    facets JSONB NOT NULL DEFAULT '{}',
    source_event VARCHAR(128) NOT NULL DEFAULT '',
    indexed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, entity_type, entity_id)
);

CREATE TABLE IF NOT EXISTS search.queries (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    query_text VARCHAR(512) NOT NULL,
    entity_types JSONB NOT NULL DEFAULT '[]',
    result_count INT NOT NULL DEFAULT 0,
    filters JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_search_documents_tenant ON search.documents(tenant_id);
CREATE INDEX IF NOT EXISTS idx_search_documents_type ON search.documents(tenant_id, entity_type);
CREATE INDEX IF NOT EXISTS idx_search_queries_tenant ON search.queries(tenant_id, created_at DESC);
