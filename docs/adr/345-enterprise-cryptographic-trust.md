# ADR-345: Enterprise Secrets, Key Management, PKI & Cryptographic Trust Platform (P209)

## Status

Accepted — P209 Cryptographic Trust Fabric foundation

## Context

MEOS Core Platform capability #21 (`secrets` / `/api/v1/secrets`) was catalogued but unimplemented. Peers (PAM ADR-276, AuthZ, Identity) ACL-handoff to `"secrets"` while material SoR was absent. P209 materializes the **Core** `secrets` bounded context as the enterprise trust anchor for secrets, keys, certificates, HSM, workload identity crypto, and post-quantum readiness.

**Hard laws:** SoR is `secrets`. Never plaintext secrets. Never keys outside governed lifecycle. Never manually managed certificates. Never absent HSM integration. Never unsupported cryptographic agility. Never unverifiable workload identities. Never unauditable trust relationships. Never invent sibling `vault` / `pki_platform` / `kms_platform` BCs. PAM vault orchestrates privileged *references* only — ciphertext stays here. AI crypto recommendations via AI Platform (advisor only).

## Decision

1. Create Core BC `backend/contexts/secrets/` (platform type)
2. API `/api/v1/secrets*`
3. Law: `ENTERPRISE_CRYPTOGRAPHIC_TRUST.md`
4. Catalogs: `docs/architecture/secrets/SECRETS_*.v1.yaml`
5. Runtime: `secrets_platform.py`; aggregates; ACL; `secrets_foundation.py`
6. Register in `registry.py` + `startup_registry.py`
7. Quality gates enforce plaintext/lifecycle/manual-cert/HSM/agility/SPIFFE/audit rejects

## Consequences

- PAM (`privileged_access`) remains privileged orchestration SoR; Secrets is material + PKI + KMS SoR
- Modules store `secret_ref` / `certificate_ref` / `key_ref` only
- Enables Zero Trust mTLS, supply-chain signing, and PQC migration path

## References

ADR-027 · ADR-276 · CORE_PLATFORM.md §21 · NIST SP 800-57 · FIPS 140-3 · RFC 5280 · RFC 8555 · SPIFFE
