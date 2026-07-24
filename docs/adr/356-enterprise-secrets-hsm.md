# ADR-356: Secrets — AI Cryptography, HSM, Confidential Computing & PQC (P209-K)

## Status

Accepted — P209-K AI Cryptography, HSM, Confidential Computing & Post-Quantum Security Platform

## Context

ADR-345–355 delivered cryptographic trust through signing/supply-chain. P209-K deepens **hardware-backed, AI-governed, quantum-ready cryptography**: HSM management, confidential computing/TEE, PQC migration, crypto agility, AI crypto intelligence — still under SoR `secrets`, never a sibling `hsm_platform` / `pqc_platform` / `confidential_computing_platform` BC.

**Hard laws:** SoR remains `secrets`. Surfaces under `/secrets/hsm*`. Never algorithms that cannot evolve. Never absent HSM protection. Never unauditable AI crypto decisions. Never confidential workloads without attestation. Never undefined PQC migration. Never unvalidated hardware trust. Never unmeasurable crypto risks.

## Decision

1. SoR remains `secrets`
2. Surfaces under `/api/v1/secrets/hsm*`
3. Law: `ENTERPRISE_SECRETS_HSM.md`
4. Catalogs: `SECRETS_HSM_*.v1.yaml`
5. Runtime: `secrets_platform_hsm.py`; aggregates; ACL; foundation
6. AI via AI Platform (advisor); HSM via Integration connectors; AuthZ for dual control
7. Series may continue with closeout / ops phases as needed

## Consequences

- Distinct from shallow `/hsm` foundation catalog vs deep `/hsm*` platform
- Distinct from `/crypto*` (EaaS ops) vs `/hsm*` (hardware/PQC/AI crypto intelligence)

## References

ADR-345–355 · FIPS 140-3 · NIST PQC · SGX/SEV · TEE attestation
