# ADR-352: Secrets — Enterprise Secrets Management & Vault (P209-G)

## Status

Accepted — P209-G Enterprise Secrets Management & Vault Platform

## Context

ADR-345–351 delivered cryptographic trust fabric, strategy, domain, PKI, CA, and KMS. P209-G deepens the **authoritative Vault / secrets store**: secret domain model, dynamic credentials, rotation, Kubernetes injection, DevSecOps scanning, and discovery — still under SoR `secrets`, never a sibling `vault` BC.

**Hard laws:** SoR remains `secrets`. Surfaces under `/secrets/vault*`. Never plaintext secret storage. Never hardcoded credentials. Never incomplete secret lifecycle. Never rotation manual-only. Never unknown secret ownership. Never unaudited secret access. Never unsupported dynamic credentials.

## Decision

1. SoR remains `secrets`
2. Surfaces under `/api/v1/secrets/vault*`
3. Law: `ENTERPRISE_SECRETS_VAULT.md`
4. Catalogs: `SECRETS_VAULT_*.v1.yaml`
5. Runtime: `secrets_platform_vault.py`; aggregates; ACL; foundation
6. Quality gates enforce ciphertext-only storage, no hardcoding, complete lifecycle, auto rotation, ownership, audit, dynamic credentials
7. PAM (`privileged_access`) orchestrates privileged **refs only** — ciphertext stays in `secrets`
8. Cloud vault backends via Integration Platform — never embed vendor SDKs in domain

## Consequences

- Secrets encrypted at rest; dynamic/JIT leases; AuthZ for access; Workflow for approvals
- Distinct from P209-F `/kms*` (keys) vs `/vault*` (secret material / credentials)
- Forbidden sibling path `backend/contexts/vault`

## References

ADR-345–351 · HashiCorp Vault pattern · External Secrets Operator · Zero Trust
