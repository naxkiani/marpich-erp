# ADR-379: Data Security — Discovery & Data Inventory (P211-D)

## Status

Accepted — P211-D Enterprise Data Discovery & Data Inventory Platform

## Context

ADR-376–378 established SoR `data_security` through domain architecture. P211-D delivers the **visibility foundation**: discovery connectors, metadata intelligence, profiling, shadow data detection, AI-assisted discovery, inventory repository, KG/twin bindings — as a logical surface under `data_security`, not a sibling discovery BC.

**Hard laws:** SoR remains `data_security`. Surfaces under `/data-security/discovery*`. Never undiscoverable assets. Never incomplete inventory. Never unavailable metadata. Never undeterminable ownership. Never invisible shadow data. Never missing AI discovery. Never unanalyzable relationships. Connectors via Integration Platform. Classification inference via Enterprise AI. Crypto via P209. Access context via P208. Threat signals via P210.

## Decision

1. SoR remains `data_security`
2. Surfaces under `/api/v1/data-security/discovery*`
3. Law: `ENTERPRISE_DATA_SECURITY_DISCOVERY.md`
4. Catalogs: `DATA_SECURITY_DISCOVERY_*.v1.yaml`
5. Runtime: `ds_platform_discovery.py`; aggregates; ACL; foundation
6. Quality gates enforce discoverability, complete inventory, metadata, ownership, shadow visibility, AI discovery, analyzable relationships

## Consequences

- Foundation for P211-E classification, DSPM, DLP, privacy, AI data security
- Forbidden siblings: `data_discovery`, `data_inventory`, `metadata_platform`, `shadow_data`

## References

ADR-376–378 · INTEGRATION_PLATFORM.md · AI_PLATFORM_STANDARD.md · ENTERPRISE_SEARCH_ENGINE.md
