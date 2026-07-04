# ADR-052: Enterprise Currency Engine — Multi-Currency with Rate Snapshots

## Status

Accepted

## Context

Financial Kernel (ADR-049) and General Ledger (ADR-050) support basic multi-currency journal lines with a single `exchange_rate` field. `convert_currency` was a stub returning hardcoded 1.1. Enterprise requirements demand unlimited currencies, base/reporting/transaction currency roles, historical/spot/average/manual/central bank rates, exchange API auto-updates, currency gain/loss, revaluation, exchange history, and immutable rate snapshots on every financial transaction.

## Decision

Adopt **`docs/architecture/ENTERPRISE_CURRENCY_ENGINE.md`** as canonical currency law within `financial_kernel` context.

Currency Engine extensions:
- `TenantCurrencySettings` — base, reporting, unlimited enabled currencies
- `ExchangeRate` — typed rates with effective dates and sources
- `ExchangeRateSnapshot` — immutable snapshot on every journal post
- Rate providers — central bank + exchange API stubs (production adapters via integration context)
- Revaluation runs with gain/loss computation
- API prefix: `/api/v1/financial-kernel/currency/*`

Journal extension: `reporting_currency`, `reporting_exchange_rate`, `rate_snapshot_id`, `rate_type` on every transaction.

## Consequences

- Every posted journal stores a rate snapshot; lines include base and reporting amounts
- Modules call currency engine for conversion — no hardcoded rates
- Auto-update fetches spot rates when enabled
- Manual rates override API rates by priority

## Alternatives considered

- Hardcoded conversion in each module — rejected (ADR-049 single kernel)
- Snapshot optional — rejected (audit/compliance requirement)
- Separate currency context — rejected (kernel owns currency engine)
