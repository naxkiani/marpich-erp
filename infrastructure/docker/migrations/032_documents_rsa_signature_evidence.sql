-- P5.1 Document Exchange — persist RSA signature evidence on signature_requests
ALTER TABLE documents.signature_requests
    ADD COLUMN IF NOT EXISTS algorithm VARCHAR(64),
    ADD COLUMN IF NOT EXISTS signature_hash TEXT,
    ADD COLUMN IF NOT EXISTS content_checksum VARCHAR(128),
    ADD COLUMN IF NOT EXISTS key_id VARCHAR(128);
