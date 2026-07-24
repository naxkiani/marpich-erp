# ADR-355: Secrets — Digital Signature, Code Signing & Supply Chain Trust (P209-J)

## Status

Accepted — P209-J Digital Signature, Code Signing & Supply Chain Trust Platform

## Context

ADR-345–354 delivered cryptographic trust through crypto services. P209-J deepens **artifact/software trust**: digital signatures, code signing, SBOM, SLSA/in-toto attestation, CI/CD gates, AI model signing — still under SoR `secrets`, never a sibling `code_signing_platform` / `supply_chain_trust_platform` BC.

**Hard laws:** SoR remains `secrets`. Surfaces under `/secrets/signing*`. Never unsigned software artifacts. Never unmanaged signing keys. Never unavailable provenance. Never absent SBOM verification. Never unvalidatable deployment trust. Never unknown artifact ownership. Never unaudited signature operations.

## Decision

1. SoR remains `secrets`
2. Surfaces under `/api/v1/secrets/signing*`
3. Law: `ENTERPRISE_SECRETS_SIGNING.md`
4. Catalogs: `SECRETS_SIGNING_*.v1.yaml`
5. Runtime: `secrets_platform_signing.py`; aggregates; ACL; foundation
6. Signing keys via KMS/HSM refs; certificates via PKI; approvals via Workflow
7. HSM depth deferred to subsequent roadmap phase

## Consequences

- Distinct from `/crypto*` (general crypto ops) vs `/signing*` (code/artifact/supply-chain trust)
- CI/CD integration via Integration Platform — never embed vendor SDKs in domain

## References

ADR-345–354 · SLSA · in-toto · SPDX · CycloneDX · Sigstore patterns
