-- P5.3 — Messenger Postgres schema (E2EE ciphertext + LiveKit room refs; no cross-schema joins)

CREATE SCHEMA IF NOT EXISTS messenger;

CREATE TABLE IF NOT EXISTS messenger.conversations (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    title VARCHAR(128) NOT NULL,
    member_ids JSONB NOT NULL DEFAULT '[]'::jsonb,
    e2ee_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    livekit_room_name VARCHAR(256),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS messenger.messages (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(63) NOT NULL,
    conversation_id UUID NOT NULL REFERENCES messenger.conversations(id) ON DELETE CASCADE,
    sender_id VARCHAR(64) NOT NULL,
    body TEXT NOT NULL DEFAULT '',
    ciphertext TEXT,
    ciphertext_type VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_messenger_conversations_tenant
    ON messenger.conversations (tenant_id);
CREATE INDEX IF NOT EXISTS idx_messenger_messages_tenant_conversation
    ON messenger.messages (tenant_id, conversation_id, created_at);
