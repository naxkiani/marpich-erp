# Enterprise Machine Learning Operations (MLOps) Platform (P214-D)

**SoR:** `ai` · **ADR:** 424 · **API:** `/api/v1/ai/mlops*` · **Capability:** `CAP-PLT-AI-001`

## Principle

**Enterprise MLOps SHALL transform machine learning from isolated experiments into governed, scalable, secure and continuously improving enterprise capabilities.**

## Fabric

MEOS Enterprise Machine Learning Intelligence Fabric — data → experiment → train → validate → register → deploy → monitor → improve → retrain.

## Core domain

Enterprise Machine Learning Lifecycle Management — `MLLifecycleAggregate`

## Supporting domains (logical — same SoR)

Experiment · Feature · Training · Registry · Deployment · Monitoring · Governance · Infrastructure · Security

## Logical bounded contexts (same SoR — not sibling BCs)

| ID | Context |
|---|---|
| BC-01 | ML Experiment |
| BC-02 | Feature Engineering |
| BC-03 | Training Pipeline |
| BC-04 | Model Registry |
| BC-05 | Model Deployment |
| BC-06 | Model Monitoring |
| BC-07 | ML Governance |

## Hard laws (quality gates)

- Never Enterprise MLOps platform is missing
- Never ML lifecycle management is missing
- Never Experiment platform is missing
- Never Feature store is missing
- Never Training platform is missing
- Never Model registry is missing
- Never Validation platform is missing
- Never Deployment platform is missing
- Never Monitoring platform is missing
- Never Continuous training is missing
- Never ML governance is missing
- Never CQRS architecture is missing
- Never Event architecture is missing
- Never Microservices architecture is missing
- Never API first architecture is missing
- Never Zero trust security is missing
- Never Cloud native deployment is missing
- Never Sibling AI BC

## Boundaries

| Concern | Owner |
|---|---|
| MLOps catalog | `ai` |
| Feature / training data governance | P212 via ACL |
| Predictive analytics consumption | P213-J via ACL |
| GPU / GitOps deploy | P213-O via ACL |
| Domain model | P214-C |
| Identity / AuthZ / Trust / Cyber / Data security | P207–P211 |
| Inference runtime | Enterprise AI SoR only |

## Forbidden

- Sibling BC (`ml_platform`, `model_lifecycle_platform`, …)
- Unsigned model artifacts in production
- Feature store without P212 alignment
- Module-local training/inference SDKs bypassing Enterprise AI
