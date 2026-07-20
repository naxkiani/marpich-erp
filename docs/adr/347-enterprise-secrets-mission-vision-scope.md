# ADR-347: Secrets / PKI / KMS — Mission, Vision & Enterprise Scope (P209-B)

## Status

Accepted — P209-B Mission, Vision & Enterprise Scope

## Context

ADR-345–346 established the `secrets` Cryptographic Trust Fabric and strategy foundation. P209-B catalogs **mission**, **vision**, **strategic objectives**, **enterprise scope**, **boundaries**, **capability ownership**, **stakeholders**, **use cases**, **principles**, **MEOS integrations**, **evolution roadmap**, and **KPIs** — without inventing sibling BCs or claiming peer SoRs (authorization, identity, PAM orchestration).

**Hard laws:** SoR remains `secrets`. Surfaces under `/secrets/mission*`. Never mission/vision absent. Never enterprise scope undefined. Never unclear boundaries (must not own business AuthZ, user profiles, app logic, data classification, network routing). Never absent capability ownership, integration responsibilities, governance principles, or evolution roadmap. Never replace peer SoRs.

## Decision

1. SoR remains `secrets`
2. Surfaces under `/api/v1/secrets/mission*`
3. Law: `ENTERPRISE_SECRETS_MISSION_VISION_SCOPE.md`
4. Catalogs: `SECRETS_MVS_*.v1.yaml`
5. Runtime: `secrets_platform_mission_scope.py`; aggregates; ACL; foundation
6. Quality gates enforce MVS completeness and boundary discipline

## Consequences

- Complements P209-A strategy with strategic charter and scope contracts
- PAM continues to orchestrate privileged refs only; Secrets owns material + PKI + KMS

## References

ADR-345 · ADR-346 · ADR-276 · CORE_PLATFORM.md §21
