# Enterprise Data Security — Lineage, Metadata & Intelligence Graph (P211-K)

**SoR:** `data_security` · **ADR:** 386 · **API:** `/api/v1/data-security/intelligence*` · **Capability:** `CAP-PLT-DS-001`

## Mission

Create an enterprise intelligence platform capable of building complete data lineage, managing active metadata, creating enterprise knowledge graphs, understanding data relationships, performing impact analysis, supporting compliance evidence, enabling AI reasoning over enterprise data, and providing complete data transparency.

## Vision

Living Enterprise Data Intelligence Graph: every data asset is connected, every transformation is explainable, every dependency is visible, every policy relationship is understood, every risk can be traced, every AI decision can explain data origin.

## Architecture flow

Enterprise Data Sources → P211-D Discovery → Metadata Collection → Lineage Extraction → Semantic Intelligence → Enterprise Knowledge Graph → AI Reasoning → Governance & Security Intelligence

## Hard laws (quality gates)

- Never Data origin is unknown
- Never Data movement is invisible
- Never Metadata is incomplete
- Never Relationships cannot be queried
- Never Impact analysis is unavailable
- Never AI cannot reason over data context

## Boundaries

| Concern | Owner |
|---|---|
| Lineage / metadata / graph catalog | `data_security` |
| Inventory inputs | P211-D |
| Classification / protection / access context | P211-E / J / H |
| Global search index | Enterprise Search (events only) |
| External connectors | Integration Platform |
| Inference / agents | Enterprise AI |
| Identity / authz / crypto / cyber | P207–P210 |

## Forbidden

- Sibling BC `data_lineage_platform`, `metadata_platform`, `data_intelligence_graph`
- Module-local Elasticsearch / OpenSearch
- Cross-schema SQL for peer lineage
- Module-local LLM SDKs
