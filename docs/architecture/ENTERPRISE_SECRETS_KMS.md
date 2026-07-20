# Enterprise Secrets — Key Management Service (KMS) — P209-F

**Prompt:** P209-F · **ADR:** [351](../adr/351-enterprise-secrets-kms.md)  
**Builds on:** P209–P209-E (ADR-345–350)  
**SoR:** `secrets` · **Forbidden:** sibling `kms_platform` BC  
**API:** `/api/v1/secrets/kms*` · **Law:** Protected keys; HSM; governed lifecycle

---

## Mission

Create an enterprise KMS capable of generating cryptographic keys securely, protecting keys throughout their lifecycle, enforcing cryptographic policies, supporting encryption services, providing HSM-backed key protection, enabling enterprise Zero Trust security, and supporting multi-cloud and hybrid environments.

## Vision

An intelligent Enterprise Key Management Fabric where every key has ownership, purpose, and lifecycle governance; every key operation is authorized and auditable; every key risk is predictable; and every cryptographic operation is policy-driven.

## Architecture stack

Enterprise KMS Core → Key Lifecycle → Cryptographic Policy → HSM Integration → Encryption Service → Key Access Control → Audit & Analytics

Deployment modes: On-Prem · Cloud · Hybrid · Multi-Cloud · Federated

## Hard laws

- Never keys are stored without protection
- Never HSM capability is unavailable
- Never key lifecycle is incomplete
- Never key ownership is unknown
- Never rotation is manual only
- Never key operations are unaudited
- Never cryptographic policies are absent
- Never invent sibling KMS BC (`kms_platform`)

## Distinct from peers

| Surface | Focus |
|---|---|
| P209-D `/pki*` | Certificate lifecycle / PKI |
| P209-E `/ca*` | CA hierarchy & trust chain |
| P209-F `/kms*` | Cryptographic key management & encryption |

Cloud KMS federation uses Integration Platform connectors — never embed vendor SDKs in domain.

## Definition of Done (P209-F)

KMS foundation ENTERPRISE_GRADE: architecture, lifecycle, HSM, envelope encryption, policy, federation, `/kms*` API live — verdict **ENTERPRISE_GRADE**.
