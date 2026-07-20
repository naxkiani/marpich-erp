# ADR-346: Secrets / PKI / KMS — Strategy Foundation (P209-A)

## Status

Accepted — P209-A Enterprise Cryptographic Trust Strategy Foundation

## Context

ADR-345 materialized Core BC `secrets`. P209-A catalogs the **enterprise strategy**, **root of trust**, **capability map**, and **governance principles** for Secrets, PKI, KMS, Vault (logical), HSM, and Cryptographic Trust — without inventing sibling BCs or allowing ungoverned crypto material.

**Hard laws:** SoR remains `secrets`. Surfaces under `/secrets/strategy*`. Never secrets stored outside governed stores. Never keys exportable without policy. Never manually managed certificates. Never inadequate Root CA security. Never absent HSM. Never incomplete cryptographic lifecycle. Never unaudited crypto operations. PAM orchestrates privileged refs only.

## Decision

1. SoR remains `secrets`
2. Surfaces under `/api/v1/secrets/strategy*`
3. Law: `ENTERPRISE_SECRETS_STRATEGY.md`
4. Catalogs: `SECRETS_STRATEGY_*.v1.yaml`
5. Runtime: `secrets_platform_strategy.py`; aggregates; ACL; `secrets_strategy_foundation.py`
6. Quality gates enforce governed stores, key export policy, auto certs, Root CA, HSM, lifecycle, audit

## Consequences

- Complements ADR-345 platform foundation with strategy/capability contracts
- Future P209-B+ phases deepen mission, PKI, KMS, vault, etc. under same SoR

## References

ADR-345 · ADR-276 · CORE_PLATFORM.md §21 · NIST SP 800-57 · FIPS 140-3 · RFC 5280
