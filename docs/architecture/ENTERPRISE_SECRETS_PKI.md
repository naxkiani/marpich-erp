# Enterprise Secrets — PKI Platform — P209-D

**Prompt:** P209-D · **ADR:** [349](../adr/349-enterprise-secrets-pki.md)  
**Builds on:** P209–P209-C (ADR-345–348)  
**SoR:** `secrets` · **Forbidden:** `contexts/pki_platform/`, sibling PKI BCs  
**API:** `/api/v1/secrets/pki*` · **Law:** Automated PKI; Root CA HSM-protected; KMS separated

---

## Mission

Create an enterprise PKI platform capable of establishing digital trust, operating CAs, managing certificate lifecycle, automating issuance, supporting Zero Trust authentication, enabling secure workload communication, and providing cryptographic identity at enterprise scale.

## Vision

A self-operating Enterprise PKI Fabric where every digital entity has trusted identity, every certificate has lifecycle visibility, every trust chain is verifiable, every certificate operation is automated, every certificate risk is predictable, and every trust relationship is continuously monitored.

## Hierarchy

Enterprise Root CA (offline) → Intermediate CAs → Issuing CAs → Registration Authorities → Certificate Subscribers

## Hard laws

**Never Root CA keys are not protected. Never certificates are manually managed. Never certificate lifecycle is incomplete. Never revocation mechanisms are absent. Never trust chains cannot be validated. Never certificate ownership is unknown. Never audit evidence is unavailable. Never invent sibling pki_platform BC. Never mix PKI ownership into KMS aggregate.**

## Runtime integration

- Root CA keys via HSM (Secrets HSM contracts)
- Approvals via Workflow Engine (RA)
- AI predictions via AI Platform
- Audit immutable trail for every cert operation
- Workload identity via SPIFFE/SPIRE contracts + service mesh

## Definition of Done (P209-D)

PKI foundation ENTERPRISE_GRADE: CA hierarchy, lifecycle, revocation, validation, ownership, audit, `/pki*` API live — verdict **ENTERPRISE_GRADE**.
