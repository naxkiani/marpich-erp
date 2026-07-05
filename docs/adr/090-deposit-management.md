# ADR-090: Deposit Management

## Status

Accepted

## Context

The Banking Customer and Account Platform (ADR-088) opens kernel-linked deposit accounts but does not manage deposit products end-to-end: savings, current, term, and recurring deposits; profit distribution; interest calculation and accrual; maturity and renewal; early withdrawal penalties; certificates and statements; automatic GL posting; approval workflows; and audit trails.

## Decision

Implement **Deposit Management** at `backend/contexts/banking/` as a dedicated module:

- **API prefix:** `/api/v1/banking/deposits`
- **Aggregates:** `DepositProfile`, `DepositTransaction`, `DepositInterestAccrual`, `DepositCertificate`, `DepositStatement`, `DepositWorkflowRequest`, `ProfitDistributionRule`, `DepositAuditEntry`
- **Deposit types:** savings, current, term, recurring
- **Interest:** daily accrual with policy-driven rates; posting credits principal via `interest_accrual` GL rule
- **Term lifecycle:** maturity processing, auto-renewal, manual renewal
- **Early withdrawal:** penalty calculated via Policy Engine (`deposit.early_withdrawal.penalty`)
- **GL integration:** direct kernel posting plus integration events for bridge idempotency (`bank_deposit`, `bank_withdrawal`, `interest_accrual`)
- **Approval:** deposit opening for large principals and all term deposits; transaction workflow for withdrawals above thresholds
- **Profit rules:** tenant-seeded on bank provision; CRUD via API
- **Policy Engine:** six configurable `deposit.*` policy keys

All rates, penalties, and approval levels are evaluated through Policy Engine — no hardcoded jurisdiction rules.

## Consequences

- One `DepositProfile` per kernel-linked account
- Transactions update account balance and deposit principal atomically on approval
- Interest accrual publishes `banking.interest.accrued` for GL bridge
- Certificates and statements are immutable records with audit trail entries
- Term maturity publishes `banking.deposit.matured`; auto-renew chains to `renew_deposit`

## Alternatives considered

- Extend account service only — rejected (insufficient for term/recurring lifecycle)
- Skip GL bridge events — rejected (idempotent cross-context posting requirement)
- Hardcoded penalty tables — rejected (tenant configurability requirement)
