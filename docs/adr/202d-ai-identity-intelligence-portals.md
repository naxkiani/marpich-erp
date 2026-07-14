# ADR-202d: AI Identity Intelligence & Portals (P198-C2)

## Status
Accepted

## Context
P198-A/B/C1 delivered federation domain, protocol gateway, and fabric trust mesh.
Operators and end users still need explainable AI intelligence, analytics,
administration UX, self-service security, copilot assistance, and compliance
controls — without embedding LLM SDKs or hardcoding thresholds.

## Decision
1. Extend `identity_federation` with Fabric Intelligence (no new BC).
2. AI Identity Intelligence Engine — model registry, feature store schema,
   explainable inference, feedback loop; thresholds from Policy Engine.
3. `application/ai_service.py` implements AI Platform Standard ACL (14 surfaces).
4. Identity Analytics + executive/operational reports + AI insights.
5. Identity Copilot — explain decisions/trust/errors, suggest policies,
   detect misconfig, summarize audit.
6. Privacy engine — GDPR/HIPAA/ISO/SOC2/etc. control catalog, retention, PIA.
7. Admin portal `/enterprise/federation` + end-user `/account/security`.
8. Quality gates YAML for security/architecture/performance/compliance/a11y/docs/explainability.

## Consequences
- API: `/api/v1/federation/intelligence/*`
- Permissions: `federation.ai.read|infer|admin`
- Policy keys: `federation.ai.enabled`, `.confidence.threshold`, `.risk.alert.threshold`, `.explainability.required`
- Production ML training remains off-box; inference remains explainable and auditable

## Compliance
Enterprise Architecture Governance Standard 9.0 — AI Native, Explainable, Auditable.
