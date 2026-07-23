"""Banking context architecture — CAP-BNK analytics surfaces.

Owns deposits, loans, KYC, payments, settlement, branch ops, and banking analytics.
Reuses Core Policy Engine, AI Platform, Audit, and Analytics — never embeds LLM or GL.

## Banking Analytics UI depth (P18)

`BankingAnalyticsDashboardPage` mirrors University/Lab/Pharmacy care depth — UI-only:

- StepProgress derived from catalog → jobs → recommendations → AI
- Status filter + StatusChip on analysis jobs
- Selectable job → detail panel (result snapshot, re-run)
- `useAutosave` draft for AI query + filters (`marpich.banking.analytics.draft`)

Backend APIs remain under `/api/v1/banking/analytics/*` (no new aggregates).
"""
