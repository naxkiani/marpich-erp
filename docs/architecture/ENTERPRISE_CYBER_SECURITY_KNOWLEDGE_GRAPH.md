# Enterprise Cyber Security — Knowledge Graph & Digital Twin (P210-K)

**SoR:** `cyber_security` · **ADR:** 371 · **API:** `/api/v1/cyber-security/graph*`

## Mission

Understand enterprise security relationships, map complete attack paths, predict cyber risks, simulate cyber attacks, support AI security reasoning, enable autonomous security operations, and provide a real-time security digital reality.

## Vision

Cyber Intelligence Fabric: every asset has context, every identity has relationships, every threat has intelligence, every vulnerability has impact, every attack path is visible, every security decision is explainable, every cyber scenario can be simulated.

## Architecture layers

Data Sources → Graph Ingestion → Entity Resolution → Semantic Modeling → Knowledge Graph Database → Reasoning Engine → AI Intelligence → Security Applications → SOC / SIEM / SOAR / XDR

## Hard laws (quality gates)

- Never security entities lack semantic relationships
- Never attack paths cannot be calculated
- Never digital twins are static
- Never AI reasoning is unavailable
- Never graph governance is missing
- Never entity resolution is inaccurate
- Never simulation capability is absent

## Boundaries

| Concern | Owner |
|---|---|
| Cyber KG ontology / attack graph / cyber twins / simulation | `cyber_security` (this surface) |
| AI inference | Enterprise AI Platform |
| Source entity SoR | owning contexts (identity, ASM, SIEM, …) — peer IDs only |
| Graph storage plumbing | infrastructure adapters (not peer DB joins) |

## Forbidden

- Sibling BC `cyber_graph`, `security_digital_twin`, `attack_graph`
- Orphan entities without semantic edges
- Attack path analysis that cannot compute paths
- Static / non-synchronized twins
- Reasoning without AI Platform ACL
- Ungoverned graph access
- Low-confidence / inaccurate entity resolution as default
- Missing simulation engine

## Compliance

ISO 27001 · NIST CSF · NIST AI RMF · MITRE ATT&CK · SOC 2
