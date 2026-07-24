# ADR-354: Secrets — Enterprise Cryptography Services & Encryption (P209-I)

## Status

Accepted — P209-I Enterprise Cryptography Services & Encryption Platform

## Context

ADR-345–353 delivered cryptographic trust through workload identity. P209-I deepens **governed cryptographic operations**: encryption/decryption, signing/verification, hashing, key exchange, EaaS APIs, algorithm policy — still under SoR `secrets`, never a sibling `crypto_platform` / `encryption_platform` BC.

**Hard laws:** SoR remains `secrets`. Surfaces under `/secrets/crypto*`. Never unmanaged application cryptography. Never encryption bypassing governance. Never exposed keys. Never uncontrolled algorithms. Never unverifiable signatures. Never unaudited crypto operations.

## Decision

1. SoR remains `secrets`
2. Surfaces under `/api/v1/secrets/crypto*`
3. Law: `ENTERPRISE_SECRETS_CRYPTO.md`
4. Catalogs: `SECRETS_CRYPTO_*.v1.yaml`
5. Runtime: `secrets_platform_crypto.py`; aggregates; ACL; foundation
6. Keys via KMS refs only; never return plaintext key material
7. Algorithms via Policy Engine; HSM acceleration via Integration/HSM adapters
8. HSM depth deferred to subsequent roadmap phase

## Consequences

- Applications consume EaaS — never embed unmanaged crypto
- Distinct from `/kms*` (key lifecycle) vs `/crypto*` (crypto operations)
- Shallow `/crypto-services` remains foundation catalog

## References

ADR-345–353 · NIST SP 800-57 · FIPS 140-3 · TLS 1.3 · PQC readiness
