# Enterprise Secrets — Certificate Authority & Trust Chain Platform — P209-E

**Prompt:** P209-E · **ADR:** [350](../adr/350-enterprise-secrets-ca.md)  
**Builds on:** P209–P209-D (ADR-345–349)  
**SoR:** `secrets` · **Forbidden:** sibling `pki_platform` / `ca_platform` BCs  
**API:** `/api/v1/secrets/ca*` · **Law:** Authoritative trust hierarchy; Root CA offline + HSM

---

## Mission

Create an enterprise Certificate Authority platform capable of establishing cryptographic trust, managing enterprise trust chains, issuing trusted certificates, protecting CA private keys, governing CA operations, supporting global environments, and enabling automated certificate lifecycle.

## Vision

A self-governing Enterprise Trust Chain where every certificate originates from a verified trust authority, every trust relationship is traceable, every CA operation is governed, every certificate chain is continuously validated, every trust failure is detected automatically, and every cryptographic asset has ownership and history.

## Hierarchy

Enterprise Root Trust Anchor → Offline Root CA → Policy Intermediate CAs → Regional/Business Intermediate CAs → Issuing CAs → Registration Authorities → Certificate Subscribers

## Hard laws

- Never Root CA is online without protection
- Never CA private keys lack HSM protection
- Never trust chains cannot be validated
- Never certificate revocation is unavailable
- Never certificate ownership is unknown
- Never CA governance is undefined
- Never audit trail is incomplete
- Never invent sibling CA/PKI BC (`pki_platform`, `ca_platform`)

## Distinct from P209-D

| P209-D `/pki*` | P209-E `/ca*` |
|---|---|
| Full PKI platform (lifecycle, ACME, types) | Authoritative CA hierarchy & trust chain governance |
| Certificate subscriber focus | Root/Intermediate/Issuing CA + ceremony + trust distribution |

## Definition of Done (P209-E)

CA/trust-chain foundation ENTERPRISE_GRADE: hierarchy, ceremony, governance, revocation, trust distribution, `/ca*` API live — verdict **ENTERPRISE_GRADE**.
