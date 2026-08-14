# ADR-424: Enterprise AI — MLOps Platform (P214-D)

## Status

Accepted — P214-D Enterprise Machine Learning Operations (MLOps) Platform

## Context

ADR-421–423 established SoR `ai` foundation, mission/scope, and DDD. P214-D catalogs the **MEOS Enterprise Machine Learning Intelligence Fabric**: lifecycle, experiments, feature store, training, registry, validation, deployment, monitoring, continuous training, and ML governance — as logical capabilities inside `ai`, not sibling BCs.

**Principle:** Enterprise MLOps SHALL transform machine learning from isolated experiments into governed, scalable, secure and continuously improving enterprise capabilities.

## Decision

1. SoR remains `ai` (CAP-PLT-AI-001)
2. Surfaces under `/api/v1/ai/mlops*`
3. Law: `ENTERPRISE_AI_MLOPS.md`
4. Catalogs: `AI_MLOPS_*.v1.yaml`
5. Runtime: `ai_platform_mlops.py`; aggregates; ACL; foundation
6. Aligns with P212 feature/data, P213-J/O, P214-A/C, P207–P211 via ACL
7. Quality gates enforce full MLOps stack, CQRS, events, microservices, zero trust, cloud-native

## Consequences

- P214-E deepens Generative AI / LLM on the same SoR
- Forbidden siblings unchanged

## References

ADR-421 · ADR-422 · ADR-423 · AI_PLATFORM_STANDARD.md · P212 · P213
