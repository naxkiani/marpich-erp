# ADR-349: Secrets — Enterprise PKI Platform (P209-D)

## Status

Accepted — P209-D Enterprise PKI Platform

## Context

ADR-345–348 established Cryptographic Trust Fabric through DDD. P209-D catalogs the **Enterprise PKI hierarchy**, **CA/RA**, **certificate lifecycle**, **validation (OCSP/CRL)**, **policies**, **ACME/automation**, and **workload PKI (SPIFFE)** — as logical surfaces under SoR `secrets`, never a sibling `pki_platform` BC. KMS material remains separated (P209-C).

**Hard laws:** SoR remains `secrets`. Surfaces under `/secrets/pki*`. Never unprotected Root CA keys. Never manually managed certificates. Never incomplete certificate lifecycle. Never absent revocation. Never unvalidatable trust chains. Never unknown certificate ownership. Never unavailable audit evidence.

## Decision

1. SoR remains `secrets`
2. Surfaces under `/api/v1/secrets/pki*`
3. Law: `ENTERPRISE_SECRETS_PKI.md`
4. Catalogs: `SECRETS_PKI_*.v1.yaml`
5. Runtime: `secrets_platform_pki.py`; aggregates; ACL; foundation
6. Quality gates enforce Root CA HSM protection, auto lifecycle, revocation, chain validation, ownership, audit

## Consequences

- Complements domain BC map with PKI operational contracts
- Root CA offline/HSM; issuing CAs automated; RA via Workflow for approvals
- AI PKI intelligence via AI Platform only

## References

ADR-345–348 · RFC 5280 · RFC 6960 · RFC 8555 · FIPS 140-3 · SPIFFE
