# ADR-088: Banking Customer and Account Platform

## Status

Accepted

## Context

The Enterprise Banking Platform (ADR-087) requires a foundational customer and account module supporting individual, business, government, and NGO customers; joint, savings, current, fixed deposit, loan, and virtual accounts; operational statuses (dormant, blocked, frozen, closed); multi-currency products; interest, minimum balance, and overdraft configuration; KYC and risk rating; approval workflows; and mandatory linkage to the Financial Kernel for every account.

## Decision

Implement the **Banking Customer and Account Platform** at `backend/contexts/banking/` with hexagonal architecture:

- **Aggregates:** `BankingCustomer`, `BankingCustomerKYC`, `BankingAccountProduct`, `BankingAccount`, `BankingAccountAudit`
- **API prefix:** `/api/v1/banking`
- **Kernel integration:** Every approved account resolves a GL control account via `customer_deposits` or `loans_receivable` account keys and sets `kernel_linked=true` with subledger reference
- **Policy Engine:** Minimum balance and overdraft checks delegate to `retail.account.minimum_balance` and `retail.overdraft.limit` policy keys
- **Events:** `banking.customer.created`, `banking.kyc.verified`, `banking.account.opened`, `banking.account.status.changed`
- **Bridge:** `BankingPostingBridge` in Financial Kernel subscribes to `banking.account.opened` and `banking.deposit.posted`

Account status transitions follow a defined workflow map. Customer and account opening require approval for high-risk, government, NGO, and large-balance scenarios.

## Consequences

- Banking accounts are subledger entities linked to kernel GL control accounts — not duplicate ledger systems
- Product catalog seeds on tenant provision (SAV-STD, CUR-STD, FD-12M, LOAN-PER, VIRT-POOL, JOINT-STD)
- Opening balance posting uses `bank_deposit` posting rule when balance > 0 at approval
- Status workflow enforces valid transitions; reactivation from blocked/frozen/dormant requires kernel link

## Alternatives considered

- Store GL balances in banking — rejected (kernel is source of truth)
- Skip kernel link for virtual accounts — rejected (all accounts must link)
- Hardcoded minimum balance thresholds — rejected (Policy Engine owns limits)
