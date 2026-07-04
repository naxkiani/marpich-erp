# ADR-049: Enterprise Financial Kernel

## Status

Accepted

## Context

Marpich has nine finance-cluster contexts but fragmented GL ownership: `finance` holds journals and COA while docs assign GL to `accounting`. Industry modules (hospital, POS, banking) lack a single financial foundation. Product leadership mandates an **Enterprise Financial Kernel** — not an accounting module — as the platform financial foundation. Every business module must call Financial Kernel APIs. Twenty industries require industry-specific COA templates.

## Decision

Adopt **`docs/architecture/ENTERPRISE_FINANCIAL_KERNEL.md`** as canonical financial law.

New bounded context **`financial_kernel`** owns:
- General Ledger, Chart of Accounts, Cost/Profit Centers, Budget
- Journal Engine, Voucher Engine, Payment Engine
- Currency Engine, Exchange Rates, Tax Engine (facade)
- Treasury/Cash Management bridges
- Financial Workflow, Reporting, Analytics integration
- Audit, Compliance, AI Financial Assistant hooks

**`accounting`** remains operational AR/AP/billing — posts through kernel, does not own GL.

**`finance`** legacy context: GL migrates to `financial_kernel` (phased deprecation).

Satellite contexts (`banking`, `islamic_banking`, `treasury`, `tax`, `currency_exchange`, `payroll`, `pos`) specialize but **never duplicate** journal/COA logic — call `IFinancialKernel`.

Industry COA templates seeded on `platform.tenant.provisioned` per `INDUSTRY_FINANCIAL_PACKS.yaml`.

## Consequences

- Single financial API surface for all modules
- No duplicate GL in business contexts
- Hospital/POS/banking flows post via kernel port
- Legacy `/api/v1/finance` compat shim during migration
- AI Financial Assistant proposes — Workflow approves — kernel posts

## Alternatives considered

- Expand `accounting` as GL owner — rejected (user mandate: NOT accounting module)
- Expand `finance` in place — rejected (name/scope insufficient for platform foundation)
- Monolithic finance cluster merge — rejected (BOUNDED_CONTEXTS_REGISTRY independence law)
- External ERP as GL (Odoo/SAP) — rejected (platform-native kernel required)
