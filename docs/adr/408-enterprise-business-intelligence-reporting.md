# ADR-408: Analytics — Enterprise Reporting, Dashboard & Visualization Platform (P213-D)

## Status

Accepted — P213-D Enterprise Reporting, Dashboard & Visualization Platform

## Context

ADR-394–396 established SoR `analytics` with strategy, MVS, and DDD domain map. P213-D catalogs the **MEOS Enterprise Intelligence Experience Fabric**: reporting engine, executive/operational/AI dashboards, visualization lifecycle, self-service BI, real-time streaming views, and AI-assisted narration — as logical capabilities inside `analytics`, not sibling BCs.

**Principle:** Enterprise reporting SHALL not only describe what happened, it SHALL explain why it happened and what should happen next.

**Hard laws:** Surfaces under `/api/v1/analytics/reporting*`. Certified metrics only on published experiences. Reuse Event Fabric, API Gateway, Enterprise AI, Observability, and P212-F/J/L via ACL.

## Decision

1. SoR remains `analytics`
2. Surfaces under `/api/v1/analytics/reporting*`
3. Law: `ENTERPRISE_BUSINESS_INTELLIGENCE_REPORTING.md`
4. Catalogs: `BI_REPORTING_*.v1.yaml`
5. Runtime: `bi_platform_reporting.py`; aggregates; ACL; foundation
6. Quality gates enforce reporting, dashboard, visualization, self-service, AI, real-time, CQRS, events, microservices, API-first, security, scalability, KG/twin visualization alignments

## Consequences

- P213-E+ deepen warehouse/lakehouse analytical serving on the same SoR
- Forbidden siblings unchanged

## References

ADR-394 · ADR-395 · ADR-396 · P212-E…O · CORE_PLATFORM.md · AI_PLATFORM_STANDARD.md
