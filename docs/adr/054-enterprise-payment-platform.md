# ADR-054: Enterprise Payment Platform

## Status

Accepted

## Context

Financial Kernel (ADR-049) catalog defines a Payment Engine but only documented capabilities without implementation. Business modules (POS, hospital, university) need unified payment processing across cash, bank transfer, cheque, card, wallet, and mobile money — with split payments, partial payments, installments, advance payments, refunds, chargebacks, auto allocation, payment matching, and reconciliation.

## Decision

Adopt **`docs/architecture/ENTERPRISE_PAYMENT_PLATFORM.md`** as canonical payment law within `financial_kernel` context.

Payment Platform:
- `Payment` aggregate with methods, kinds, statuses, allocations
- `InstallmentPlan` for scheduled payments
- `PaymentReconciliation` for bank matching
- `PaymentApplicationService` separate from GL service
- API prefix: `/api/v1/financial-kernel/payments/*`

Integration events: `payment.settled`, `payment.allocated`, `payment.refunded`, `payment.chargeback`, `payment.reconciled`

## Consequences

- All modules initiate payments via kernel API — no duplicate payment logic
- Idempotent payment creation via `idempotency_key`
- Auto-allocation FIFO across open documents
- Gateway connectors delegated to integration platform (future)

## Alternatives considered

- Payments in each module — rejected (ADR-049 single kernel)
- Separate payments bounded context — deferred (kernel owns payment engine per catalog)
