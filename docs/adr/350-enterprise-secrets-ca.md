# ADR-350: Secrets — Enterprise Certificate Authority & Trust Chain (P209-E)

## Status

Accepted — P209-E Enterprise Certificate Authority & Trust Chain Platform

## Context

ADR-349 delivered Enterprise PKI contracts. P209-E deepens the **authoritative CA hierarchy**, **Root CA key ceremony**, **Intermediate/Issuing CA governance**, **trust chain management**, **trust distribution**, and **CA audit** — still under SoR `secrets`, never a sibling `pki_platform` or `ca_platform` BC. Complements P209-D; does not replace KMS (future phase).

**Hard laws:** SoR remains `secrets`. Surfaces under `/secrets/ca*`. Never Root CA online without protection. Never CA private keys without HSM. Never unvalidatable trust chains. Never unavailable revocation. Never unknown certificate ownership. Never undefined CA governance. Never incomplete audit trail.

## Decision

1. SoR remains `secrets`
2. Surfaces under `/api/v1/secrets/ca*`
3. Law: `ENTERPRISE_SECRETS_CA.md`
4. Catalogs: `SECRETS_CA_*.v1.yaml`
5. Runtime: `secrets_platform_ca.py`; aggregates; ACL; foundation
6. Quality gates enforce offline/protected Root CA, HSM keys, chain validation, revocation, ownership, governance, audit

## Consequences

- Root CA remains offline + HSM; Issuing CAs automated; RA/approvals via Workflow
- Trust distribution contracts for OS/browser/K8s trust stores
- KMS phase deferred to subsequent roadmap entry

## References

ADR-345–349 · RFC 5280 · RFC 6960 · FIPS 140-3 · SPIFFE
