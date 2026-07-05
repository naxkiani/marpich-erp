# ADR-094: Banking Settlement Engine

## Status

Accepted

## Context

Banking Payment Platform (ADR-093) executes customer transfers but does not net, clear, or reconcile payment batches against nostro positions. Treasury bank reconciliation (ADR-079) handles corporate liquidity statements separately. Financial Kernel reconciliation (ADR-068) is cross-type and not tailored to banking settlement batches, exception queues, or manual adjustment approval for customer payment rails.

## Decision

Implement **Banking Settlement Engine** at `backend/contexts/banking/`:

- **API prefix:** `/api/v1/banking/settlement`
- **Aggregates:** `SettlementBatch`, `SettlementItem`, `BankReconciliationRun`, `ReconciliationMatch`, `SettlementException`, `SettlementDifference`, `SettlementAdjustment`, `SettlementAuditEntry`, `SettlementReport`
- **Settlement types:** internal_settlement, interbank_settlement, clearing
- **Features:** bank reconciliation, automatic matching, difference analysis, exception management with retry, manual adjustment approval, settlement reports, settlement dashboard, reconciliation audit
- **GL integration:** `bank_settlement`, `interbank_settlement`, `clearing_settlement` posting rules + `BankingPostingBridge.handle_settlement_posted`
- **Events:** `banking.settlement.posted`, `banking.reconciliation.completed`, `banking.settlement.exception.raised`
- **Policy Engine:** seven `settlement.*` policy keys

Treasury remains separate for corporate liquidity; customer settlement debits/credits banking subledger via kernel posting rules on batch execution.

## Consequences

- Clearing batches require clearing step before settlement
- Interbank settlement posts through cash_reserves ↔ nostro mapping
- Reconciliation runs match statement lines to completed payment transfers
- Exceptions support configurable retry with escalation
- Bridge provides idempotent GL posting on `banking.settlement.posted`

## Alternatives considered

- Treasury settlement engine for customer ops — rejected (corporate vs retail boundary)
- Kernel reconciliation only — rejected (no batch netting, clearing, or exception retry)
- Skip GL bridge — rejected (idempotent cross-context posting requirement)
