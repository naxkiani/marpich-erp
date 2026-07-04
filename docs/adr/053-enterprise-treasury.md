# ADR-053: Enterprise Treasury — Cash, Liquidity, Reconciliation

## Status

Accepted

## Context

Financial Kernel (ADR-049) defines treasury as a satellite context for cash positions, liquidity, and transfers. The `treasury` bounded context was scaffold-only. Enterprise requirements demand cash/bank/petty cash/vault/safe accounts, multiple payment instruments (cheque, EFT, mobile money, digital wallet), bank reconciliation, cash forecasting, liquidity analysis, treasury dashboard, and approval workflow for transfers.

## Decision

Adopt **`docs/architecture/ENTERPRISE_TREASURY.md`** as canonical treasury law in `backend/contexts/treasury/`.

Treasury capabilities:
- `TreasuryAccount` — cash, bank, petty_cash, vault, safe (unlimited per tenant)
- `TreasuryTransfer` — all payment instruments with draft → approval → execute workflow
- `BankReconciliation` — statement vs book matching
- `CashForecast` — multi-scenario cash flow projection
- Dashboard + liquidity analysis APIs
- Integration events: `treasury.transfer.executed`, `treasury.liquidity.updated`

API prefix: `/api/v1/treasury/*`

Financial Kernel does not duplicate treasury logic — modules call Treasury API for cash operations; journal posting remains via Financial Kernel.

## Consequences

- Tenant provision seeds default treasury accounts
- Transfers require approval by default; auto-execute when `require_approval: false`
- Liquidity events published on balance changes
- Workflow engine can link via `workflow_instance_id` on approve

## Alternatives considered

- Treasury inside financial_kernel — rejected (satellite context per ADR-049)
- No approval workflow — rejected (enterprise control requirement)
