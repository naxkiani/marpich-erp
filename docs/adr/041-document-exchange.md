# ADR-041: Enterprise Document Exchange

## Status

Accepted

## Context

Marpich modules produce invoices, contracts, medical records, academic credentials, tax filings, and official correspondence. The existing `documents` context provides folders, versioning, basic signature, and archive — but lacks canonical design for ten document classes, approval workflows, QR verification, encryption, watermarks, comments, AI/OCR/translation, retention, and external exchange.

Platform Charter: modules must not store file blobs locally.

## Decision

Adopt **`docs/architecture/ENTERPRISE_DOCUMENT_EXCHANGE.md`** as canonical document law.

### Document classes

Internal, official letters, contracts, invoices, reports, certificates, academic, medical, tax, financial statements — each with type-specific retention, encryption, workflow, and verification rules in `DOCUMENT_TYPES.yaml`.

### Cross-cutting capabilities

Versioning, approval workflow (Workflow Engine), digital signature, QR verification, encryption, watermark, comments, history, AI summaries, translation, OCR, retention policy.

### Exchange

Internal via folders and permissions; external via Integration Platform connectors.

### Module rule

Store `document_id` reference only — all bytes in Document Exchange + object storage.

## Consequences

- Extended aggregates: DocumentComment, DocumentHistory, RetentionPolicy
- Workflow integration for approval gates before publish
- AI/Search integration for OCR and summaries
- Public QR verify endpoint without auth

## Alternatives considered

- Module-local file storage — rejected (compliance, search, retention)
- Third-party DMS only — rejected (tenant control, workflow integration)
- Mutable document versions — rejected (audit and legal requirements)
