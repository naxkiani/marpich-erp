# ADR 432 — Enterprise AI Model Intelligence, Lifecycle & Model Governance (P214-L)

## Status

Accepted

## Context

MEOS AI (P214-A–K) needs a model control plane for registry, lifecycle, evaluation, approval, monitoring, drift, risk, knowledge graph, and digital twin — without sibling BCs (`model_lifecycle_platform`, `model_registry`, etc.). Approval integrates P214-H + Workflow; training/deploy with P214-D; data/features with P214-K; graph with P214-G.

## Decision

1. SoR remains **`ai`** (`CAP-PLT-AI-001`).
2. Fabric: **`meos_enterprise_ai_model_intelligence_fabric`**.
3. API surface: **`/api/v1/ai/modelintel*`**.
4. Seven logical bounded contexts (BC-01–BC-07) as partitions of SoR `ai`.
5. Models are enterprise assets with versioning, risk scores, and lifecycle state.
6. Principle: complete lifecycle visibility, governance and intelligence for every AI model in MEOS.

## Consequences

- P214-M (AI Integration / API Gateway / Service Mesh) consumes modelintel contracts.
- Peer IDs only via ACL to P211–P214-K.
