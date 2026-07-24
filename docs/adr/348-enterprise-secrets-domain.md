# ADR-348: Secrets / PKI / KMS — Cryptographic Trust Domain Architecture (P209-C)

## Status

Accepted — P209-C Enterprise Cryptographic Trust Domain Architecture (DDD)

## Context

ADR-345–347 established foundation, strategy, and mission/scope for Core BC `secrets`. P209-C catalogs **strategic domain classification**, **logical bounded contexts** (Trust, PKI, KMS, Secrets, HSM, Workload Identity, Governance), **aggregates**, **domain services**, **events**, **CQRS**, and **microservice boundaries** — all deployable as one SoR `secrets` (logical contexts only; no sibling BCs).

**Hard laws:** SoR remains `secrets`. Surfaces under `/secrets/domain*`. Never unclear domain boundaries. Never mixed PKI and KMS responsibilities. Never unmanaged secrets. Never unmodeled trust relationships. Never absent domain events. Never aggregates violating ownership. Never incomplete cryptographic lifecycle.

## Decision

1. SoR remains `secrets` (logical BCs ≠ deployable BCs)
2. Surfaces under `/api/v1/secrets/domain*`
3. Law: `ENTERPRISE_SECRETS_DOMAIN.md`
4. Catalogs: `SECRETS_DOMAIN_*.v1.yaml`
5. Runtime: `secrets_platform_domain.py`; aggregates; ACL; foundation
6. Quality gates enforce boundary clarity, PKI/KMS separation, managed secrets, trust model, events, ownership, lifecycle

## Consequences

- Complements P209-A/B with tactical DDD contracts
- Microservices listed are logical; deployable unit today remains `secrets`

## References

ADR-345–347 · MODULE_ARCHITECTURE.md · DDD_DOMAIN_ARCHITECTURE.md
