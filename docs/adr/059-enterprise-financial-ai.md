# ADR-059: Enterprise Financial AI Platform

## Status

Accepted

## Context

Financial Kernel requires AI-powered financial intelligence: fraud detection, cash flow and revenue prediction, budget forecasting, expense analysis, risk analysis, recommendations, invoice classification, document OCR, financial chatbot, AI dashboard, and CFO assistant. Per `AI_PLATFORM_STANDARD.md`, the kernel owns financial semantics; inference delegates to AI Platform in production.

## Decision

Adopt **`docs/architecture/ENTERPRISE_FINANCIAL_AI.md`** as canonical financial AI law within `financial_kernel` context.

Financial AI Engine:
- `FinancialAIJob` for async analysis with capability, confidence, result
- `FinancialAIChatSession` for chatbot and CFO assistant conversations
- Engine functions for all 13 capabilities using kernel data (journals, payments, budgets)
- API prefix: `/api/v1/financial-kernel/financial-ai/*`
- `autonomous_posting_forbidden: true`

Integration events: `ai.analysis.completed`, `ai.dashboard.generated`, `ai.chat.completed`

## Consequences

- AI never posts journals or modifies financial data autonomously
- All analyses produce auditable jobs with confidence scores
- Production inference delegates to AI Platform via `ai.financial.copilot` surface
- CFO Assistant combines executive summary, KPIs, and recommendations

## Alternatives considered

- AI in Analytics context — rejected (financial semantics belong in kernel)
- Direct LLM calls from API routes — rejected (engine + service layer required)
