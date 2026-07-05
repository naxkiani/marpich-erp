# ADR-089: Enterprise KYC Platform

## Status

Accepted

## Context

The Banking Customer and Account Platform (ADR-088) provides basic KYC records but lacks enterprise-grade identity verification, document types, address verification, risk classification, CDD/EDD, PEP and sanctions screening hooks, biometric extension points, workflow approval, periodic review, audit trail, and configurable rules via the Policy Engine.

## Decision

Implement the **Enterprise KYC Platform** at `backend/contexts/banking/` as a dedicated module:

- **API prefix:** `/api/v1/banking/kyc`
- **Aggregates:** `KycCase`, `KycDocument`, `KycAddressVerification`, `KycScreeningResult`, `KycPeriodicReview`, `KycWorkflowRequest`, `KycBiometricHook`, `KycAuditEntry`
- **Document types:** passport, national_id, business_registration, tax_number, address_proof
- **Due diligence:** standard (CDD) and enhanced (EDD) with policy-driven escalation
- **Screening hooks:** PEP and sanctions with external provider reference fields — no hardcoded list logic
- **Policy Engine:** Eight configurable `kyc.*` policy keys seeded on bank tenant provision
- **Workflow:** Multi-level approval based on risk class, EDD, and PEP status
- **Periodic review:** Scheduled on case approval with policy-driven intervals
- **Biometric:** Extension hook pattern — provider callback, no vendor lock-in

All regulatory thresholds, review intervals, and screening outcomes are evaluated through Policy Engine — no hardcoded jurisdiction rules.

## Consequences

- KYC cases are independent aggregates linked to `BankingCustomer` via `customer_id`
- Case approval updates customer `kyc_status` to verified
- Sanctions-blocked cases cannot be approved
- PEP confirmed automatically triggers EDD
- Audit trail captures all case actions with high sensitivity default

## Alternatives considered

- Extend basic `BankingCustomerKYC` only — rejected (insufficient for enterprise KYC)
- Hardcoded sanctions lists in banking — rejected (external hook + policy outcomes)
- Skip Policy Engine for KYC rules — rejected (tenant configurability requirement)
