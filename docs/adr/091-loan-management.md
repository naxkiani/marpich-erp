# ADR-091: Enterprise Loan Platform

## Status

Accepted

## Context

The Banking Customer and Account Platform (ADR-088) opens kernel-linked loan accounts but does not manage lending end-to-end: personal, business, education, construction, mortgage, microfinance, and agriculture products; origination and approval workflows; collateral and guarantors; amortization schedules and installments; penalty rules; restructuring, settlement, and early closure; automatic GL posting; and AI-ready credit risk analysis.

## Decision

Implement **Enterprise Loan Platform** at `backend/contexts/banking/` as a dedicated module:

- **API prefix:** `/api/v1/banking/loans`
- **Aggregates:** `LoanProfile`, `LoanCollateral`, `LoanGuarantor`, `LoanInstallment`, `LoanTransaction`, `LoanCreditRiskAnalysis`, `LoanWorkflowRequest`, `LoanAuditEntry`
- **Loan types:** personal, business, education, construction, mortgage, microfinance, agriculture
- **Origination:** apply → submit → multi-level approval workflow (policy-driven)
- **Collateral & guarantors:** linked to loan profile before disbursement
- **Credit risk:** deterministic scoring with factor breakdown; publishes `banking.loan.credit_risk.analyzed`
- **Disbursement:** builds amortization schedule, posts via `loan_disbursement` GL rule
- **Repayment:** installment payment with late penalty via `loan.penalty.late_payment` policy
- **Lifecycle:** restructuring (new schedule), settlement, early closure
- **GL integration:** direct kernel posting plus bridge handlers (`loan_disbursement`, `loan_repayment`)
- **Policy Engine:** ten configurable `loan.*` and `lending.*` policy keys

All rates, penalties, approval levels, and risk thresholds are evaluated through Policy Engine — no hardcoded jurisdiction rules.

## Consequences

- One `LoanProfile` per kernel-linked loan account
- Disbursement credits loan account balance; repayments debit
- Credit risk analysis is idempotent per loan (latest analysis linked on profile)
- Restructuring appends new installment rows for remaining tenure
- Bridge handlers provide idempotent GL posting on integration events

## Alternatives considered

- Extend customer account service only — rejected (insufficient for collateral, schedules, risk)
- Treasury loan rules for customer lending — rejected (treasury rules are corporate borrowing)
- External AI-only scoring — rejected (deterministic baseline required for audit and policy integration)
