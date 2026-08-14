# Enterprise AI Data Intelligence, Feature Engineering & AI Data Platform (P214-K)

**SoR:** `ai` · **ADR:** 431 · **API:** `/api/v1/ai/aidata*` · **Capability:** `CAP-PLT-AI-001`

## Principle

**Enterprise AI Data Platform SHALL transform enterprise data into governed, intelligent and reusable AI assets for machine learning, generative AI and autonomous intelligence.**

## Fabric

MEOS Enterprise AI Data Intelligence Fabric — Enterprise Data + Data Governance + Data Mesh + Feature Engineering + Machine Learning + Generative AI + AI Agents → Trusted AI Data Foundation → Feature Intelligence → Model Intelligence → AI Decisions → Autonomous Enterprise Intelligence.

## Core domain

Enterprise AI Data Intelligence Management — `EnterpriseAIDataIntelligenceAggregate`

## Supporting domains (logical — same SoR)

Dataset Management · Feature Engineering · Feature Store · Training Data · Data Pipeline · Synthetic Data · Data Quality · Data Lineage · Data Governance

## Logical bounded contexts (same SoR — not sibling BCs)

| ID | Context |
|---|---|
| BC-01 | AI Dataset Management |
| BC-02 | Feature Engineering |
| BC-03 | Feature Store |
| BC-04 | Training Data |
| BC-05 | AI Data Pipeline |
| BC-06 | Synthetic Data |
| BC-07 | AI Data Quality |
| BC-08 | AI Data Governance |

## Hard laws (quality gates)

- Never Enterprise AI Data Platform is missing
- Never AI Dataset Management is missing
- Never Feature Engineering Platform is missing
- Never Feature Store Platform is missing
- Never Training Data Platform is missing
- Never Synthetic Data Platform is missing
- Never Data Quality Intelligence is missing
- Never AI Data Lineage is missing
- Never AI Data Marketplace is missing
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
| AI data catalog / features | `ai` |
| Feature consumption at train/serve | P214-D MLOps via ACL |
| Synthetic RAI / privacy review | P214-H via ACL |
| Metadata / lineage graph | P212-K via ACL |
| Asset encryption / privacy | P211 via ACL |
| Pipeline health | P214-J AIOps via ACL |

## Forbidden

- Sibling BC `feature_store`, `ai_data`, `ai_data_platform`, etc.
- Module-local feature store bypassing Enterprise AI
- Training without quality and lineage
- Synthetic data without P214-H privacy review
- Cross-schema AI data joins
- Unversioned datasets or features in production
