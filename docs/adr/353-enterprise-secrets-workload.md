# ADR-353: Secrets — Workload Identity, SPIFFE/SPIRE & mTLS (P209-H)

## Status

Accepted — P209-H Enterprise Workload Identity, SPIFFE/SPIRE & mTLS Platform

## Context

ADR-345–352 delivered cryptographic trust fabric through Vault. P209-H deepens **machine/workload cryptographic identity**: SPIFFE IDs, SPIRE attestation, SVIDs, mTLS enforcement, service mesh, Kubernetes and cloud federation — still under SoR `secrets`, never a sibling `workload_identity_platform` / `spiffe_platform` BC.

**Hard laws:** SoR remains `secrets`. Surfaces under `/secrets/workload*`. Never workloads without cryptographic identity. Never static credentials required. Never mTLS unenforceable. Never manual-only certificate rotation. Never undefined trust domains. Never unknown workload identity ownership. Never unaudited service communication.

## Decision

1. SoR remains `secrets`
2. Surfaces under `/api/v1/secrets/workload*`
3. Law: `ENTERPRISE_SECRETS_WORKLOAD.md`
4. Catalogs: `SECRETS_WORKLOAD_*.v1.yaml`
5. Runtime: `secrets_platform_workload.py`; aggregates; ACL; foundation
6. Quality gates enforce crypto identity, secretless auth, mTLS, auto rotation, trust domains, ownership, audit
7. Human identity SoR remains `identity`; AuthZ via P208; CA/PKI/KMS/Vault via prior P209 surfaces
8. HSM depth deferred to subsequent roadmap phase

## Consequences

- SPIFFE/SPIRE as workload identity fabric; mTLS everywhere; mesh integrates via Integration/platform adapters
- Distinct from P209-G `/vault*` (secret material) vs `/workload*` (cryptographic machine identity)

## References

ADR-345–352 · SPIFFE · SPIRE · RFC 8446 (TLS 1.3) · Istio/Linkerd patterns
