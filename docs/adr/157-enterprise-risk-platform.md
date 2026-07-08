# ADR-157: Enterprise Risk Platform

## Status

Accepted

## Context

Risk capabilities are distributed across GRC (risk register), Treasury Risk, and FX Risk platforms. There is no unified enterprise risk orchestration layer covering financial, operational, cyber, compliance, vendor, project, treasury, FX, credit, and liquidity risks with matrix, heatmap, dashboard, and AI prediction.

Requirements:
- 10 risk categories with unified register
- Risk matrix (likelihood × impact) and heatmap
- Risk dashboard aggregating all categories
- AI risk prediction (explainable, no autonomous execution)
- Delegation to treasury_risk, fx_risk, grc — no duplication

## Decision

Implement **Enterprise Risk Platform** at `/api/v1/risk`.

### New bounded context

`backend/contexts/risk/` — orchestration layer over domain risk engines.

### Capabilities (15)

| Capability | Category / Feature |
|------------|-------------------|
| Financial Risk | financial |
| Operational Risk | operational |
| Cyber Risk | cyber |
| Compliance Risk | compliance (delegates to grc) |
| Vendor Risk | vendor |
| Project Risk | project |
| Treasury Risk | treasury (delegates to treasury_risk) |
| FX Risk | fx (delegates to fx_risk) |
| Credit Risk | credit |
| Liquidity Risk | liquidity (delegates to treasury_risk) |
| Risk Matrix | likelihood × impact grid |
| Risk Register | canonical enterprise register |
| Risk Dashboard | unified summary |
| Risk Heatmap | category intensity visualization |
| AI Risk Prediction | explainable trend forecasting |

### Aggregates

- `RiskTenantProfile` — matrix size, escalation threshold, enabled categories
- `EnterpriseRiskItem` — unified risk register entry
- `RiskMatrixSnapshot` — persisted matrix state
- `RiskPrediction` — AI prediction with factors and recommendations

### Policy Keys (domain: `tax`)

- `risk.escalation.threshold`
- `risk.matrix.size`
- `risk.ai.confidence_threshold`
- `risk.heatmap.top_n`
- `risk.register.auto_escalate`

### Events

- `risk.item.registered`
- `risk.item.escalated`
- `risk.prediction.generated`
- `risk.matrix.updated`

### API Surface

- `GET /catalog`, `GET /dependency-map`, `POST /seed`
- `GET /dashboard`
- `GET /register`, `POST /register`, `POST /register/{ref}/escalate`
- `GET /matrix`, `GET /heatmap`
- `POST /predict`, `GET /predictions`

## Consequences

- Seed registers 10 risks across all categories with delegation metadata
- Auto-escalation when risk score exceeds policy threshold
- GRC risk register remains for GRC assessments; enterprise risk is canonical enterprise layer
- AI predictions are explainable only — `autonomous_execution: false`

## Alternatives considered

- Extend GRC only — rejected (GRC is governance/compliance focused, not all risk types)
- Per-module risk only — rejected (fragmentation)
- Autonomous risk remediation — rejected (explainable recommendations only)
