# ADR-058: Enterprise Financial Security

## Status

Accepted

## Context

Financial Kernel requires enterprise-grade security controls. Modules need maker-checker, four eyes principle, dual approval, digital signatures, immutable audit trails, transaction locking, period/fiscal year closing with dual approval, RBAC/ABAC access policies, encryption, and tamper detection — with a hard rule that financial data modifications never occur without audit.

## Decision

Adopt **`docs/architecture/ENTERPRISE_FINANCIAL_SECURITY.md`** as canonical financial security law within `financial_kernel` context.

Financial Security Engine:
- `MakerCheckerRequest` with maker_checker, four_eyes, dual_approval controls
- `TransactionLock` for resource locking
- `PeriodCloseRequest` with dual approval for period and fiscal year close
- `SecurityPolicy` for RBAC and ABAC
- `SecurityAuditRecord` with chained tamper hashes
- `guarded_modification` endpoint enforcing audit-before-modify
- API prefix: `/api/v1/financial-kernel/security/*`

Integration events: `security.maker_checker.submitted`, `security.maker_checker.approved`, `security.transaction.locked`, `security.period.closed`, `security.audit.recorded`, `security.tamper.detected`

## Consequences

- Maker cannot approve own submissions
- All security actions produce immutable audit records
- Locked resources block guarded modifications
- Period/FY close requires two independent approvers
- Delegates long-term audit retention to Audit Platform

## Alternatives considered

- Security in each module — rejected (ADR-049 single kernel)
- Identity-only RBAC — rejected (financial-specific controls belong in kernel)
