# ADR-087: Enterprise Banking Platform

## Status

Accepted

## Context

Marpich requires a core banking industry extension for retail, corporate, microfinance, digital, branch, and agency banking — built on the Enterprise Financial Kernel without duplicating GL, treasury, payments, currency, workflow, security, or audit. Banking context exists as metadata-only stubs. Islamic banking must compose via a separate extension context. All regulatory limits must be configurable through the Policy Engine — never hardcoded by jurisdiction.

## Decision

Implement the **Banking Platform** as a Financial Kernel industry satellite at `backend/contexts/banking/` using Domain-Driven Design with seven capability domains, public kernel port integration (`IFinancialKernel`, `IPolicyEvaluator`), and event-driven GL posting via `BANKING_GL_BRIDGE.md`.

Banking owns customer-facing products (deposits, loans, cards, transfers, KYC). Treasury owns corporate liquidity. Kernel owns all financial posting, payments, currency, workflow, security, and audit.

Regulations, limits, rates, and compliance thresholds are evaluated exclusively through `banking.*` policy keys — no country-specific code paths.

## Consequences

- Single banking codebase serves retail, corporate, microfinance, digital, branch, and agency channels via channel adapters
- Islamic products extend through `islamic_banking` context composing banking aggregates — no kernel fork
- Multi-tenant, multi-organization, multi-branch scoping via platform dimensions
- GL auto-posting through kernel posting rules — banking never builds journal lines

## Alternatives considered

- Banking posts journals directly — rejected (violates kernel law)
- Duplicate payment/currency engines in banking — rejected
- Hardcoded regulatory modules per country — rejected (Policy Engine owns all limits)
- Merge banking into treasury — rejected (customer products ≠ corporate liquidity)
