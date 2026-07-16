# ADR-203a: Digital Twin Type Catalog & Multi-Subject Expansion (Prompt 199-A)

## Status

Accepted — extends ADR-203 (does not replace it)

## Context

ADR-203 delivered an identity-focused twin (user projections, sync, simulation, drift). Prompt **V03-C02-P199-A** requires twins for organizations, devices, sessions, applications, AI agents, and industry entities (banks, hospitals, universities, …), plus trust/risk/compliance/behavior facets, relationship graphs, and stronger governance.

Creating one bounded context per twin kind would violate Platform Charter (duplication) and Service Boundaries (cross-domain tables). Hardcoding twin types in Python enums would violate metadata/config/policy-driven law.

## Decision

1. **Keep a single platform BC** `identity_digital_twin` (schema `identity_twin`) as the Twin Platform.  
2. Introduce a versioned **`TwinKindDefinition` catalog** (`twin_kinds`) — kinds are data, not code.  
3. Expand `DigitalTwin` to `(tenant_id, kind, subject_ref)` uniqueness; identity user twins remain `kind=identity.user`.  
4. Add facet/graph/health/prediction tables per architecture law (migration `031`).  
5. Industry kinds (`bank`, `hospital`, …) are activated by industry pack events; twin never owns industry SoR.  
6. All enablement, lag, retention, shared-scope, and deletion gates evaluate via **Policy Engine**.  
7. Predictions invoke **AI Platform** only; simulations remain non-mutating.

## Consequences

- Delivery is incremental: registry + kinds first, then facets/graph, then industry packs.  
- Consumers must pass `kind` on create/list APIs (default `identity.user` for backward compatibility).  
- Compliance/PHI/secret data stays out of twin JSONB (refs only).  
- Prompt ID **199-A**; this ADR is **203a** to stay sequenced under twin ADR-203.

## References

- [ENTERPRISE_IDENTITY_DIGITAL_TWIN_PLATFORM.md](../architecture/ENTERPRISE_IDENTITY_DIGITAL_TWIN_PLATFORM.md)  
- `docs/architecture/identity/DIGITAL_TWIN_KIND_CATALOG.yaml`  
- `docs/architecture/identity/DIGITAL_TWIN_EVENT_CONTRACTS.v1.yaml`
