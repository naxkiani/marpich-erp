# Enterprise Cyber Security — Domain Architecture (DDD) — P210-C

**Prompt:** P210-C · **ADR:** [363](../adr/363-enterprise-cyber-security-domain.md)  
**Builds on:** P210-A (ADR-361), P210-B (ADR-362)  
**SoR:** `cyber_security` · **Forbidden:** sibling SOC/SIEM/SOAR/XDR/threat_detection BCs  
**API:** `/api/v1/cyber-security/domain*`

---

## Mission

Create a scalable cyber security domain architecture that clearly separates security responsibilities, eliminates domain coupling, enables autonomous evolution, supports cloud-native microservices, enables AI-assisted security, supports Zero Trust, and integrates with every MEOS domain via contracts and events.

## Vision

Create a Cyber Security Domain Model where every security capability owns its logical domain, every domain owns its data within the SoR schema, every business rule belongs to one context, every interaction occurs through contracts, and every event becomes enterprise knowledge.

## Hard laws

- Never bounded contexts overlap
- Never aggregates violate consistency boundaries
- Never domain ownership is unclear
- Never business rules leak across contexts
- Never events are not domain-driven
- Never knowledge graph integration is missing
- Never anti-corruption layers are absent
- Never invent sibling deployable BCs for logical contexts
- Never duplicate IR lifecycle (SoR remains `security_incident`)

## Logical bounded contexts (same SoR)

Security Monitoring · Threat Detection · Threat Intelligence · Incident Response (handoff) · Case Management · Threat Hunting · Security Automation · Exposure Management · Security Governance · AI Security

## Distinct from peers

| Peer | Boundary |
|---|---|
| `security_incident` | IR lifecycle SoR — consumed via ACL/events |
| Observability | Telemetry plumbing |
| Secrets / AuthZ / PAM / II | Crypto / PDP / privileged / identity analytics |
| Knowledge Graph / Twin platforms | Peer SoRs — refs + ACL only |

## Definition of Done (P210-C)

Domain foundation ENTERPRISE_GRADE: non-overlapping logical BCs, clear ownership, domain events, KG + ACL, `/domain*` API live.
