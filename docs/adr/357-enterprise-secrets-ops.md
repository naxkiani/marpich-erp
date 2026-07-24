# ADR-357: Secrets — CQRS, Events, APIs & Microservices Platform (P209-L)

## Status

Accepted — P209-L CQRS, Events, APIs & Microservices Platform (series closeout)

## Context

ADR-345–356 delivered cryptographic trust capabilities (PKI, CA, KMS, Vault, Workload, Crypto, Signing, HSM/PQC). P209-L defines the **software fabric** that operates them at enterprise scale: CQRS, event sourcing, secure APIs, logical microservice boundaries, observability, and resilient deployment — still under SoR `secrets`, never sibling platform BCs.

**Hard laws:** SoR remains `secrets`. Surfaces under `/secrets/ops*`. Never shared databases across logical services. Never missing events. Never unsecured APIs. Never unauditable cryptographic operations. Never unclear microservice ownership. Never incomplete observability. Never non-scalable deployment.

## Decision

1. SoR remains `secrets` (single BC; logical microservices = deployable units / schemas under `secrets_*`)
2. Surfaces under `/api/v1/secrets/ops*`
3. Law: `ENTERPRISE_SECRETS_OPS.md`
4. Catalogs: `SECRETS_OPS_*.v1.yaml`
5. Runtime: `secrets_platform_ops.py`; aggregates; ACL; foundation
6. Events via Event Fabric + outbox; APIs via API Gateway; AuthZ / Audit / Observability platforms reused
7. Completes P209 series closeout for cryptographic trust application fabric

## Consequences

- Logical service map (pki-management-service, key-management-service, …) are **deployable units**, not separate bounded contexts
- Each unit owns its schema / projections; no cross-service shared DB
- Distinct from capability surfaces (`/pki*`, `/kms*`, `/hsm*`) vs ops fabric (`/ops*`)

## References

ADR-345–356 · ENTERPRISE_EVENT_BUS · API_GATEWAY_ARCHITECTURE · MODULE_ARCHITECTURE · CQRS
