# ADR-363: Cyber Security — Domain Architecture / DDD (P210-C)

## Status

Accepted — P210-C Enterprise Cyber Security Domain Architecture (DDD)

## Context

ADR-361–362 established SoR `cyber_security` strategy and MVS. P210-C catalogs the **canonical DDD model**: core/supporting domain map, logical bounded contexts, aggregates, entities, value objects, domain services, events, repositories, application services, context mapping, knowledge graph / digital twin intents, domain policies, and anti-corruption layers — without inventing sibling deployable BCs (`soc_platform`, `siem_platform`, `threat_detection`, etc.) and without absorbing peer SoRs.

**Hard laws:** SoR remains `cyber_security`. Surfaces under `/cyber-security/domain*`. Never overlapping bounded contexts. Never aggregates that violate consistency boundaries. Never unclear domain ownership. Never business rules leaking across contexts. Never non-domain-driven events. Never missing knowledge-graph integration. Never absent anti-corruption layers. Incident Response lifecycle remains `security_incident` (logical IR context = handoff contracts only). KG/Twin/Telemetry/Audit/Notifications remain platform peers.

## Decision

1. SoR remains `cyber_security` — logical BCs are modular surfaces inside one deployable unit
2. Surfaces under `/api/v1/cyber-security/domain*`
3. Law: `ENTERPRISE_CYBER_SECURITY_DOMAIN.md`
4. Catalogs: `CYBER_DOMAIN_*.v1.yaml`
5. Runtime: `cs_platform_domain.py`; aggregates; ACL; foundation
6. Quality gates enforce non-overlap, ownership clarity, event-driven contracts, KG + ACL presence

## Consequences

- P210-D–O deepen SOC/SIEM/SOAR/XDR/etc. as logical modules on the same SoR
- Peer integration via ACL + events only

## References

ADR-361 · ADR-362 · ADR-158 · DDD_DOMAIN_ARCHITECTURE.md · SERVICE_BOUNDARIES.md
