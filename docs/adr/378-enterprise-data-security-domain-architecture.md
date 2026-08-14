# ADR-378: Data Security — Domain Architecture / DDD (P211-C)

## Status

Accepted — P211-C Enterprise Data Security Domain Architecture (DDD)

## Context

ADR-376–377 established SoR `data_security` with strategy and MVS. P211-C catalogs the **DDD domain map**: core Enterprise Data Security Intelligence Domain plus supporting logical domains (discovery, classification, protection, privacy, access governance, risk, lineage, DLP, compliance, AI data security, knowledge graph, digital twin) — as logical subdomains inside `data_security`, not sibling BCs.

**Hard laws:** SoR remains `data_security`. Surfaces under `/data-security/domain*`. Never tightly coupled domains. Never unclear data ownership. Never privacy separated from security. Never missing events. Never undefined aggregates. Never unclear integration boundaries. Consent ledger remains `consent`; crypto `secrets`; PDP `authorization`; threat defense `cyber_security`.

## Decision

1. SoR remains `data_security`
2. Surfaces under `/api/v1/data-security/domain*`
3. Law: `ENTERPRISE_DATA_SECURITY_DOMAIN_ARCHITECTURE.md`
4. Catalogs: `DATA_SECURITY_DOMAIN_*.v1.yaml`
5. Runtime: `ds_platform_domain.py`; aggregates; ACL; foundation
6. Quality gates enforce loose coupling, clear ownership, privacy↔security integration, events, aggregates, clear integration boundaries

## Consequences

- P211-D+ deepen discovery/classification/protection on the same SoR
- Forbidden siblings unchanged (dspm, privacy_intelligence, …)

## References

ADR-376 · ADR-377 · DDD_DOMAIN_ARCHITECTURE.md · SERVICE_BOUNDARIES.md
