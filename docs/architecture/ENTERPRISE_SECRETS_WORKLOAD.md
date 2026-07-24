# Enterprise Secrets — Workload Identity, SPIFFE/SPIRE & mTLS — P209-H

**Prompt:** P209-H · **ADR:** [353](../adr/353-enterprise-secrets-workload.md)  
**Builds on:** P209–P209-G (ADR-345–352)  
**SoR:** `secrets` · **Forbidden:** sibling `workload_identity_platform` / `spiffe_platform` BCs  
**API:** `/api/v1/secrets/workload*` · **Law:** Cryptographic workload identity; mTLS; secretless

---

## Mission

Create an enterprise Workload Identity Platform capable of eliminating implicit workload trust, providing cryptographic workload identity, enabling Zero Trust service communication, automating certificate lifecycle, supporting Kubernetes and cloud-native workloads, providing universal machine identity, and enabling secure service-to-service communication.

## Vision

An autonomous Workload Trust Fabric where every workload has a verified identity, every service authenticates cryptographically, every connection is mutually trusted, every certificate rotates automatically, every workload relationship is observable, every trust decision is policy-driven, and every machine identity is governed.

## Identity hierarchy

Human → Machine → Workload → Service → Application → AI Agent → Device

## Hard laws

- Never workloads lack cryptographic identity
- Never static credentials are required
- Never mTLS cannot be enforced
- Never certificate rotation is manual
- Never trust domains are undefined
- Never workload identity ownership is unknown
- Never service communication is unaudited
- Never invent sibling Workload/SPIFFE BC

## Distinct from peers

| Surface | Focus |
|---|---|
| P209-D/E `/pki*` `/ca*` | Certificate authorities & trust chains |
| P209-G `/vault*` | Secret material / dynamic credentials |
| P209-H `/workload*` | SPIFFE/SPIRE SVID, mTLS, mesh identity |
| `identity` BC | Human identity SoR |

## Definition of Done (P209-H)

Workload identity foundation ENTERPRISE_GRADE: SPIFFE/SPIRE, mTLS, attestation, mesh/K8s/cloud, `/workload*` API live — verdict **ENTERPRISE_GRADE**.
