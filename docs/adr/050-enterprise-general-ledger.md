# ADR-050: Enterprise General Ledger — Immutable, Reversal-Only

## Status

Accepted

## Context

Financial Kernel (ADR-049) established the platform financial foundation with basic journal posting. Enterprise GL requires unlimited scale dimensions (accounts, journals, fiscal years, periods, orgs, branches), automatic and manual posting, recurring and reversing journals, approval workflow, audit trail, multi-currency, budget validation, and strict immutability — never delete, only reverse.

## Decision

Adopt **`docs/architecture/ENTERPRISE_GENERAL_LEDGER.md`** as canonical GL law within `financial_kernel` context.

GL Engine extensions:
- Immutable journal entries (append-only, no delete, no update after post)
- Reversal-only corrections via `POST /ledger/journals/{id}/reverse`
- Automatic, manual (approval workflow), recurring, reversing posting modes
- Unlimited accounts, journals, fiscal years, periods (tenant/org/branch scoped)
- Multi-currency with rate snapshot on journal
- Budget validation before expense posting

API prefix: `/api/v1/financial-kernel/ledger/*`

## Consequences

- All modules post through kernel; corrections are reversals
- Manual journals require approval before posting
- Audit events on every post, reverse, approval
- Legacy `POST /journals` remains as automatic posting compat

## Alternatives considered

- Soft-delete journals — rejected (audit/compliance)
- Edit posted entries — rejected (SOX/immutability)
- Separate GL context — rejected (kernel owns GL per ADR-049)
