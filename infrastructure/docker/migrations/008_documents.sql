-- Documents schema
CREATE SCHEMA IF NOT EXISTS documents;

CREATE TABLE IF NOT EXISTS documents.folders (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    parent_id UUID REFERENCES documents.folders(id) ON DELETE SET NULL,
    name VARCHAR(128) NOT NULL,
    is_root BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS documents.documents (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    folder_id UUID NOT NULL REFERENCES documents.folders(id) ON DELETE CASCADE,
    title VARCHAR(256) NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    current_version_id UUID,
    status VARCHAR(16) NOT NULL DEFAULT 'active',
    metadata JSONB NOT NULL DEFAULT '{}',
    created_by VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS documents.document_versions (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    document_id UUID NOT NULL REFERENCES documents.documents(id) ON DELETE CASCADE,
    version_number INT NOT NULL,
    file_name VARCHAR(256) NOT NULL,
    content_type VARCHAR(128) NOT NULL,
    content TEXT NOT NULL,
    checksum VARCHAR(64) NOT NULL,
    storage_key VARCHAR(256),
    created_by VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (document_id, version_number)
);

CREATE TABLE IF NOT EXISTS documents.signature_requests (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    document_id UUID NOT NULL REFERENCES documents.documents(id) ON DELETE CASCADE,
    version_id UUID NOT NULL REFERENCES documents.document_versions(id) ON DELETE CASCADE,
    requester_id VARCHAR(64) NOT NULL,
    signers JSONB NOT NULL DEFAULT '[]',
    status VARCHAR(16) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_documents_folders_tenant ON documents.folders(tenant_id);
CREATE INDEX IF NOT EXISTS idx_documents_docs_tenant ON documents.documents(tenant_id);
CREATE INDEX IF NOT EXISTS idx_documents_docs_folder ON documents.documents(tenant_id, folder_id);
CREATE INDEX IF NOT EXISTS idx_documents_versions_doc ON documents.document_versions(document_id);
