# ADR-055: Enterprise Financial Documents

## Status

Accepted

## Context

Financial Kernel (ADR-049) requires unified financial document generation across all business modules. Modules currently lack a canonical API for invoices, bills, vouchers, receipts, payment orders, purchase/sales invoices, credit/debit notes, and journal/cash/bank vouchers — with PDF output, digital signatures, QR verification, versioning, and approval workflows.

## Decision

Adopt **`docs/architecture/ENTERPRISE_FINANCIAL_DOCUMENTS.md`** as canonical financial document law within `financial_kernel` context.

Financial Documents Engine:
- `FinancialDocument` and `FinancialDocumentVersion` aggregates
- 12 document types with auto-numbering (`INV-2026-000001`, etc.)
- PDF generation (minimal valid PDF, base64)
- Digital signature (HMAC-SHA256 stub, RS256 algorithm label)
- QR verification with signed tokens
- Immutable versioning with SHA-256 checksums
- Approval workflow (request/complete; delegates to Workflow Engine)
- API prefix: `/api/v1/financial-kernel/financial-documents/*`

Integration events: `document.created`, `document.version.created`, `document.approval.requested`, `document.approved`, `document.signed`, `document.issued`

## Consequences

- All modules create financial documents via kernel API
- Idempotent creation via `idempotency_key`
- Approval required for vouchers, payment orders, purchase/sales invoices, credit/debit notes
- Document Exchange remains general-purpose file storage; kernel owns financial semantics

## Alternatives considered

- Documents in each module — rejected (ADR-049 single kernel)
- Extend Document Exchange only — rejected (financial numbering and GL linkage belong in kernel)
