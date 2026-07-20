# ADR-324: Identity Intelligence — Self-Healing Identity Fabric (P207-I)

## Status

Accepted — P207-I Self-Healing Identity Fabric Platform

## Context

P207-A–H established strategy through behavioral analytics on SoR `identity_intelligence`. P207-D delivered autonomous ops including basic remediation. P207-I deepens the **Self-Healing Identity Fabric**: health monitoring, failure detection, AI root-cause analysis, leveled remediation, twin simulation before repair, validation, and continuous learning — without fully manual recovery, ungoverned remediation, missing RCA, unaudited actions, absent twin simulation, or undefined security validation.

**Hard laws:** SoR remains `identity_intelligence`. Surfaces under `/healing*` (distinct from `/autonomous*`). Governed remediation required. HITL for Level 2+. Twin simulation before remediation. Graph RCA via directory. AI via AI Platform. Never invent sibling healing BC. Never embed LLM SDK. Never bypass AuthZ PDP.

## Decision

1. SoR remains `identity_intelligence`
2. Surfaces under `/api/v1/identity-intelligence/healing*`
3. Law: `ENTERPRISE_IDENTITY_INTELLIGENCE_SELF_HEALING_FABRIC.md`
4. Catalogs: `II_HEALING_*.v1.yaml`
5. Runtime: `ii_platform_healing.py`; aggregates: `ii_healing_aggregates.py`; ACL: `ii_healing_acl.py`; validator: `ii_healing_foundation.py`
6. Quality gates reject manual-only recovery, ungoverned remediation, missing RCA, unaudited actions, absent twin simulation, undefined security validation

## Consequences

- P207-D remains autonomous orchestration surface; P207-I is reliability/healing depth
- Authoritative twin storage remains `identity_digital_twin`

## References

ADR-316–323 · Workflow · AI Platform · directory · identity_digital_twin · Zero Trust · Platform Charter
