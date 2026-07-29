# ADR-386: Data Security — Lineage, Metadata & Intelligence Graph (P211-K)

## Status

Accepted — P211-K Enterprise Data Lineage, Metadata & Intelligence Graph Platform

## Context

ADR-376–385 established SoR `data_security` through discovery, classification, DSPM, DLP, access, privacy, and protection. P211-K delivers the **data intelligence backbone**: active metadata, technical/business/AI lineage, semantic knowledge graph, impact analysis, observability signals, AI reasoning over data context, twin bindings — without inventing sibling `data_lineage_platform` / `metadata_platform` BCs and without module-local search engines (Enterprise Search remains Core).

**Hard laws:** SoR remains `data_security`. Surfaces under `/data-security/intelligence*`. Never unknown data origin. Never invisible data movement. Never incomplete metadata. Never unqueryable relationships. Never unavailable impact analysis. Never AI that cannot reason over data context. Inference via Enterprise AI. Connectors via Integration Platform where external. Approvals via Workflow. Policies via Policy Engine.

## Decision

1. SoR remains `data_security`
2. Surfaces under `/api/v1/data-security/intelligence*`
3. Law: `ENTERPRISE_DATA_SECURITY_INTELLIGENCE.md`
4. Catalogs: `DATA_SECURITY_INTELLIGENCE_*.v1.yaml`
5. Runtime: `ds_platform_intelligence.py`; aggregates; ACL; foundation
6. Quality gates enforce known origin, visible movement, complete metadata, queryable relationships, impact analysis, AI reasoning
7. Roadmap: P211-K = Intelligence Graph; AI Data Security deferred (`/ai-data*`); fulfills deferred J-INTEL

## Consequences

- Intelligence backbone connecting discovery → classification → DLP → access → protection → cyber → Enterprise AI
- Forbidden siblings: `data_lineage_platform`, `metadata_platform`, `data_intelligence_graph`

## References

ADR-376–385 · ENTERPRISE_SEARCH_ENGINE.md · INTEGRATION_PLATFORM.md · AI_PLATFORM_STANDARD.md · P207–P210
