# ADR-092: Interest Calculation Engine

## Status

Accepted

## Context

Deposit Management (ADR-090) embeds a basic `calculate_daily_interest()` for accrual posting, and Loan Management (ADR-091) computes amortization schedule interest. There is no unified engine for daily/monthly/annual frequencies, simple vs compound methods, grace periods, penalty interest, floating/fixed/promotional rates, historical rate changes, profit sharing, simulation mode, or immutable calculation audit history.

## Decision

Implement **Interest Calculation Engine** at `backend/contexts/banking/`:

- **API prefix:** `/api/v1/banking/interest`
- **Aggregates:** `InterestRateProfile`, `InterestRateChange`, `InterestCalculationAudit`
- **Frequencies:** daily, monthly, annual
- **Methods:** simple, compound (policy-driven compounding frequency)
- **Rate types:** fixed, floating (index + spread), promotional (time-bound override)
- **Features:** grace period, penalty interest, profit sharing (extension-ready), historical rate resolution, simulation mode (no side effects beyond audit)
- **Audit:** every calculate/simulate persists `InterestCalculationAudit` with policy snapshot and calculation detail
- **Events:** `banking.interest.calculated`, `banking.interest.simulated`, `banking.interest.rate.changed`
- **Policy Engine:** eight `interest.*` keys plus delegation to `deposit.interest.rate` / `loan.interest.rate`

Deposit accrual endpoints remain at `/banking/deposits/interest/*`; this engine is the canonical cross-product calculator.

## Consequences

- Rate profiles are tenant-scoped with immutable change history
- Simulation writes audit records with `mode=simulation` and does not post GL
- Production calculate publishes integration events for downstream consumers
- Deposit service may delegate to this engine in a future refactor

## Alternatives considered

- Extend deposit module only — rejected (loans and generic products need same engine)
- Hardcoded rate tables — rejected (Policy Engine requirement)
- Skip audit trail — rejected (regulatory traceability requirement)
