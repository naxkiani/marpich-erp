# ADR-097: Banking Analytics Platform

## Status

Accepted

## Context

Enterprise Banking Platform (ADR-087) implements deposits, lending, payments, branches, and security as separate capability domains, but lacks a unified analytics layer for executive reporting, portfolio monitoring, and AI-assisted decision support. Treasury has its own analytics engine; banking needs retail/corporate banking KPIs, delinquency tracking, fraud analytics, and explainable recommendations.

## Decision

Implement **Banking Analytics Platform** at `backend/contexts/banking/`:

- **API prefix:** `/api/v1/banking/analytics`
- **Capabilities:** liquidity KPIs, deposit trends, loan portfolio, customer segmentation, branch performance, revenue analysis, risk indicators, portfolio quality, delinquency analysis, forecasting, fraud detection, customer insights, executive dashboard, AI banking assistant
- **Data sources:** aggregates from customer accounts, deposits, loans, payments, branches, and security modules (read-only cross-repo queries)
- **AI layer:** explainable recommendations with evidence, confidence scores, and `autonomous_execution: false`
- **Policy keys:** 8 `analytics.*` thresholds for liquidity, delinquency, fraud, forecast horizon, segmentation, revenue, risk, and portfolio quality
- **Events:** `banking.analytics.report.generated`, `banking.analytics.insight.raised`, `banking.analytics.recommendation.generated`, `banking.analytics.forecast.completed`

## Consequences

- Executives get a single dashboard aggregating deposits, loans, risk, and revenue
- AI assistant provides explainable recommendations without autonomous execution
- Analytics jobs are persisted for audit and replay via `/jobs`
- Treasury analytics remains separate for corporate liquidity; banking analytics covers retail/corporate banking portfolio

## Alternatives considered

- Reuse treasury analytics only — rejected (different data model and KPIs)
- External BI tool only — rejected (policy engine integration and in-app AI assistant required)
- Hardcoded thresholds — rejected (policy engine requirement)
