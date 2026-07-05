# ADR-093: Banking Payment Platform

## Status

Accepted

## Context

Enterprise Banking Platform (ADR-087) catalogs customer transfers and payments as a planned capability with `banking.transfer.posted` events and `bank_transfer` GL rules, but no implementation exists. Treasury handles corporate liquidity transfers separately. Financial Kernel Payment Platform handles settlement rails but not customer transfer orchestration, limits, fraud checks, or approval workflows.

## Decision

Implement **Banking Payment Platform** at `backend/contexts/banking/`:

- **API prefix:** `/api/v1/banking/payments`
- **Aggregates:** `PaymentTransfer`, `PaymentBeneficiary`, `PaymentBatch`, `StandingOrder`, `PaymentWorkflowRequest`, `PaymentFraudCheck`, `PaymentAuditEntry`
- **Transfer types:** internal, inter_branch, bank_to_bank, bulk, bill_payment, government_payment, salary_transfer, merchant_payment, qr_payment, real_time
- **Features:** scheduled transfers, standing orders, transfer limits, multi-level approval, deterministic fraud scoring, audit trail
- **GL integration:** `bank_transfer` posting rule + `BankingPostingBridge.handle_transfer_posted`
- **Events:** `banking.transfer.posted`, `banking.transaction.posted`, `banking.payment.fraud.flagged`
- **Policy Engine:** ten `payment.*` policy keys

Treasury remains separate for corporate liquidity; customer transfers debit/credit banking subledger accounts directly on execution.

## Consequences

- Internal transfers move balance between kernel-linked accounts atomically
- Execute endpoint chains submit → approve → process for real-time payments
- Fraud-blocked transfers cannot execute
- Bridge provides idempotent GL posting on `banking.transfer.posted`

## Alternatives considered

- Treasury transaction engine for customer ops — rejected (corporate vs retail boundary)
- Kernel payment service only — rejected (no limits, fraud, or beneficiary registry)
- Skip GL bridge — rejected (idempotent cross-context posting requirement)
