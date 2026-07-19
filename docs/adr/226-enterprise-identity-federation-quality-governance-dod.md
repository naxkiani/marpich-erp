# ADR-226: EIFTP Quality, Governance, Documentation & Definition of Done (P200-B12)

## Status

Accepted — Official EIFTP Quality / Governance / Series DoD closeout (V03-C03)

## Context

P200-B11 standardized deploy/ops. P200-B12 closes the Cursor series with enterprise quality gates, testing matrix, documentation/governance standards, traceability, compliance validation hooks, release certification, and a machine-checkable Definition of Done for EIFTP.

## Decision

1. Law: `docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_QUALITY_GOVERNANCE_DOD.md`
2. Catalogs: `docs/architecture/identity/eiftp/QA_*.v1.yaml` + series readiness report
3. Facade: `FederationQualityPlatform` — gates · Dod · traceability · readiness (not a QA Platform BC)
4. REST: `/api/v1/federation/qa/*`
5. Series validator composes B2–B11 foundations + B12 artifacts; rejects `contexts/eiftp`
6. Platform Testing / Audit / Compliance / AuthZ remain SoRs — EIFTP publishes evidence & checklists only
7. B1 foundation remainder (D2 / Scope / Stakeholders / Principles) tracked as explicit backlog in readiness report — not silently marked complete

## Consequences

- CI can invoke `validate_quality_governance_foundation` as release gate
- EIFTP Cursor series B2–B12 marked done; B1 backlog remains governance debt

## References

ADR-212…225 · ENGINEERING_QUALITY_STANDARD · ARCHITECTURE_VALIDATION · DEVELOPMENT_PROTOCOL
