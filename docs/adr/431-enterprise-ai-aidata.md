# ADR 431 — Enterprise AI Data Intelligence, Feature Engineering & AI Data Platform (P214-K)

## Status

Accepted

## Context

MEOS AI (P214-A–J) requires a trusted data intelligence foundation: datasets, features, training assets, synthetic data, quality, lineage, and marketplace — without sibling BCs (`feature_store`, `ai_data`, etc.). Feature serving integrates P214-D MLOps; synthetic data is governed by P214-H; lineage integrates P212-K metadata.

## Decision

1. SoR remains **`ai`** (`CAP-PLT-AI-001`).
2. Fabric: **`meos_enterprise_ai_data_intelligence_fabric`**.
3. API surface: **`/api/v1/ai/aidata*`**.
4. Eight logical bounded contexts (BC-01–BC-08) as partitions of SoR `ai`.
5. Offline/online feature store, pipelines, quality score, lineage chain, and marketplace are catalog + ACL contracts — modules never embed local feature stores.
6. Principle: transform enterprise data into **governed, intelligent and reusable AI assets**.

## Consequences

- P214-L (Model Intelligence / Lifecycle / Model Governance) consumes feature/dataset contracts from this fabric.
- Peer IDs only via ACL to P211–P214-J.
