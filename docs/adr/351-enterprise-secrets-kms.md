# ADR-351: Secrets — Enterprise Key Management Service (P209-F)

## Status

Accepted — P209-F Enterprise Key Management Service (KMS)

## Context

ADR-345–350 delivered cryptographic trust fabric, strategy, domain, PKI, and CA/trust-chain. P209-F deepens the **authoritative KMS**: key domain model, lifecycle, HSM integration, envelope encryption, multi-cloud federation, and crypto policy — still under SoR `secrets`, never a sibling `kms_platform` BC.

**Hard laws:** SoR remains `secrets`. Surfaces under `/secrets/kms*`. Never keys stored without protection. Never HSM unavailable. Never incomplete key lifecycle. Never unknown key ownership. Never rotation manual-only. Never unaudited key operations. Never absent cryptographic policies.

## Decision

1. SoR remains `secrets`
2. Surfaces under `/api/v1/secrets/kms*`
3. Law: `ENTERPRISE_SECRETS_KMS.md`
4. Catalogs: `SECRETS_KMS_*.v1.yaml`
5. Runtime: `secrets_platform_kms.py`; aggregates; ACL; foundation
6. Quality gates enforce protected keys, HSM, complete lifecycle, ownership, auto rotation, audit, crypto policies
7. Cloud KMS (AWS/Azure/GCP/Vault) via Integration Platform connectors — never module-embedded SDKs

## Consequences

- KMS keys HSM-backed; DEK/KEK envelope encryption; AuthZ for key access; Audit for every op
- Distinct from P209-D `/pki*` and P209-E `/ca*` (certificate authority vs key management)
- PAM holds refs only — ciphertext stays in `secrets`

## References

ADR-345–350 · FIPS 140-3 · NIST SP 800-57 · envelope encryption
