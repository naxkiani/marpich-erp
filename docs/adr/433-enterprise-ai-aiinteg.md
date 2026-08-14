# ADR 433 — Enterprise AI Integration, AI API Gateway & Intelligent AI Service Mesh (P214-M)

## Status

Accepted

## Context

MEOS AI (P214-A–L) needs a communication fabric for AI APIs, service mesh semantics, model serving, agent messaging, events, and workflows — without sibling BCs or replacing the platform API Gateway / Event Fabric.

## Decision

1. SoR remains **`ai`** (`CAP-PLT-AI-001`).
2. Fabric: **`meos_intelligent_ai_integration_fabric`**.
3. API surface: **`/api/v1/ai/aiinteg*`**.
4. Seven logical bounded contexts (BC-01–BC-07) on SoR `ai`.
5. **Platform API Gateway owns the edge**; AI defines route/contract catalogs via ACL.
6. **Platform Event Fabric owns the bus**; AI publishes/consumes via ACL only.
7. Principle: secure, intelligent, autonomous communication fabric for all AI capabilities.

## Consequences

- P214-N (AI Infrastructure / Cloud / Compute) consumes aiinteg contracts.
- Modules never embed local AI gateways or mesh control planes.
