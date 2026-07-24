# ADR-223: Enterprise Security, Zero Trust & Compliance Platform — Federation Control Plane (P200-B9)

## Status

Accepted — Official Federation Security / Zero Trust / Compliance control plane (V03-C03)

## Context

P200-B6–B8 delivered Trust Fabric, IdP management, and cross-tenant trust. P200-B9 establishes the **security control plane for EIFTP**: Zero Trust by default, continuous verification, risk & threat detection, AI security governance, and compliance posture — without duplicating Audit, Compliance Framework, Policy Engine, or Authorization PDP (P200-A).

## Decision

1. Law: `docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_SECURITY_ZERO_TRUST.md`
2. Catalogs: `docs/architecture/identity/eiftp/SECURITY_ZT_*.v1.yaml`
3. Logical domains (Security Control, Zero Trust, Risk, Compliance Posture, SecOps signals, AI Security) live **inside** `identity_federation`
4. Facade: `FederationSecurityControlPlane` composes ZT engine, risk engine, trust fabric, federation security validators, continuous verification
5. Zero Trust **federation gate** actions: `allow` · `allow_with_conditions` · `challenge` · `require_mfa` · `require_step_up` · `deny` · `quarantine` · `escalate` — these are **security gate outcomes**, not AuthZ resource Permit/Deny
6. Full enterprise Compliance/Audit remain Platform SoRs; B9 emits evidence refs + posture summaries + integration events
7. CQRS + REST `/api/v1/federation/security/*`; GraphQL/gRPC deferred to B10
8. No hardcoded tenant policies — local security baseline + `IPolicyEvaluator` for runtime policy keys
9. DevSecOps / K8s hardening catalogs reference existing ARCH_DEPLOYMENT patterns; deep deploy is B11

## Consequences

- B10 packages event contracts + OHS APIs on this plane
- B11 deepens observability + DevSecOps pipeline wiring
- Modules subscribe to `federation.security.*` / `federation.zt.*` events via ACL

## References

ADR-204 · 205 · 220–222 · ENTERPRISE_AUDIT_PLATFORM · ENTERPRISE_COMPLIANCE_FRAMEWORK · SECURITY_STANDARD
