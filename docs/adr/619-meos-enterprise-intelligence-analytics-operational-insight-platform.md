# ADR 619 — MEOS Enterprise Intelligence Analytics & Operational Insight Platform (P262)

## Status
Accepted

## Context
P261 established MEBRDI over Policy Engine / P224. P262 productizes enterprise intelligence analytics and operational insight as the MEOS Data Intelligence Operating Layer. The `analytics` context (CAP-PLT-BI-001) already owns BI/KPI; P229 owns data mesh/products; Observability owns technical telemetry. MEIAOI must federate those SoRs — never fork `/api/v1/analytics*` or `/api/v1/data-mesh*`, and never reintroduce module-local metrics stores. P263 is planned for Data Intelligence & Data Mesh Operating depth over P229.

## Decision
1. SoR `operational_insight`; fabric `meos_enterprise_intelligence_analytics_operational_insight_platform_framework`; API `/api/v1/operational-insight*`; capability `CAP-PLT-MEIAOI-001`; acronym **MEIAOI**.
2. Logical BCs inside one SoR: Analytics Management overlay, Insight Management, Performance Intelligence, Predictive Intelligence, Anomaly Intelligence, Insight Governance.
3. Federate with `analytics`, P229, Observability, Reporting, P261, P260, P257–P259, P214-Z, P227, P228 — never replace them; never dual-write analytics/mesh tables; never cross-schema analytics SQL.
4. Inference only via P214-Z; insight ≠ execute; explainability required for gated actions; no local metrics/alerting stores in business modules.
5. Roadmap: P262 foundation → P262-A…D; unblocks P263.

## Consequences
Positive: governed operational/predictive insight fabric over canonical analytics and data mesh.  
Negative: BI/KPI and data-product truth remain peer-owned — MEIAOI stores insight/prediction/anomaly campaigns, evidence packs and peer refs only.

## Links
Law: `ENTERPRISE_MEOS_INTELLIGENCE_ANALYTICS_OPERATIONAL_INSIGHT_PLATFORM.md` · Prior: ADR 618 · Next: P262-A · Peer: ADR 620 (P263 MEDIMOP) · Peers: `analytics`, P229 EFDMIFP, Observability
