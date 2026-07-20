# Enterprise Secrets / PKI / KMS — Cryptographic Trust Domain Architecture — P209-C

**Prompt:** P209-C · **ADR:** [348](../adr/348-enterprise-secrets-domain.md)  
**Builds on:** P209, P209-A, P209-B (ADR-345–347)  
**SoR:** `secrets` · **Forbidden:** sibling vault/PKI/KMS BCs; mixing PKI↔KMS ownership  
**API:** `/api/v1/secrets/domain*` · **Law:** Logical BCs inside one deployable unit

---

## Mission

Create a domain architecture capable of managing enterprise cryptographic trust, governing secrets/keys/certificates, supporting PKI lifecycle, enforcing cryptographic policies, providing secure workload identities, supporting Zero Trust communication, and enabling autonomous cryptographic operations.

## Vision

Trust is a first-class enterprise object; cryptographic assets have complete lifecycle management; every key has ownership; every certificate has traceability; every secret has controlled lifecycle; every cryptographic decision is explainable; every trust relationship is discoverable.

## Strategic classification

| Type | Domains |
|---|---|
| Core | Enterprise Cryptographic Trust Fabric |
| Supporting | Certificate Lifecycle · Key Management · Secrets Management · HSM · Crypto Compliance · Trust Analytics · Crypto Monitoring |
| Generic (reuse Core peers) | Identity Federation · Authorization · Audit · Observability · Configuration |

## Logical bounded contexts (not sibling deployables)

Cryptographic Trust · PKI Management · Key Management · Secrets Management · HSM Security · Workload Identity · Cryptographic Governance

## Hard laws

**Never domain boundaries are unclear. Never PKI and KMS responsibilities are mixed. Never secrets are unmanaged. Never trust relationships are not modeled. Never domain events are absent. Never aggregates violate ownership rules. Never cryptographic lifecycle is incomplete. Never invent sibling vault/PKI/KMS BC.**

## Definition of Done (P209-C)

Domain foundation ENTERPRISE_GRADE: BC map, aggregates, events, CQRS, microservice (logical) boundaries, `/domain*` API live — verdict **ENTERPRISE_GRADE**.
