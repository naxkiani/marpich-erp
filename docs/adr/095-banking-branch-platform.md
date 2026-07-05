# ADR-095: Branch Banking Platform

## Status

Accepted

## Context

Enterprise Banking Platform (ADR-087) catalogs branch operations as planned with `BankBranch` and `ChannelSession` aggregates but no implementation. Customer accounts, KYC, payments, and settlement reference `branch_id` without a branch hierarchy registry, vault management, teller extensions, or branch KPI analytics.

## Decision

Implement **Branch Banking Platform** at `backend/contexts/banking/`:

- **API prefix:** `/api/v1/banking/branches`
- **Office hierarchy:** head_office, regional_office, branch, sub_branch
- **Extensions:** cash_counter, atm_extension, self_service_kiosk_extension
- **Operations:** branch opening/closing, vault management, cash limits, employee assignment, branch KPIs
- **Analytics:** settlement dashboard and branch analytics endpoints
- **Events:** `banking.branch.opened`, `banking.branch.closed`, `banking.vault.movement`, `banking.branch.kpi.recorded`
- **Policy Engine:** eight `branch.*` policy keys

GL posting for teller transactions remains delegated to deposit/payment modules; branch platform owns operational hierarchy and vault balances.

## Consequences

- Tenant provisioning seeds a default head office with vault
- Office hierarchy validated on create (regional under head office, etc.)
- Vault movements enforce policy limits
- Branch KPI targets resolved from policy when not supplied

## Alternatives considered

- Organization context only — rejected (banking-specific vault, counters, KPIs)
- Treasury cash management — rejected (corporate vs retail boundary)
- Hardcoded branch limits — rejected (policy engine requirement)
