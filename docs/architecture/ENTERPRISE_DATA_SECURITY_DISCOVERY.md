# Enterprise Data Security — Discovery & Data Inventory (P211-D)

**SoR:** `data_security` · **ADR:** 379 · **API:** `/api/v1/data-security/discovery*` · **Capability:** `CAP-PLT-DS-001`

## Mission

Discover every enterprise data asset, create a unified inventory, understand ownership, map locations, collect metadata, identify sensitive information, detect unknown/shadow data, and provide the foundation for security, privacy and governance automation.

## Vision

Data Visibility Intelligence Fabric: every data asset known, every source mapped, every movement understood, every owner identified, every risk measurable, every dataset with security context, every relationship intelligent.

## Architecture flow

Enterprise Data Sources → Discovery Connectors → Data Collection Engine → Metadata Extraction → Data Profiling → AI Classification Engine → Data Inventory Repository → Knowledge Graph → Security Intelligence Layer

## Hard laws (quality gates)

- Never Data assets cannot be discovered
- Never Inventory is incomplete
- Never Metadata is unavailable
- Never Ownership cannot be determined
- Never Shadow data remains invisible
- Never AI discovery capability is missing
- Never Data relationships cannot be analyzed

## Boundaries

| Concern | Owner |
|---|---|
| Discovery / inventory / metadata / shadow catalog | `data_security` |
| Connector execution | Integration Platform |
| Classification inference | Enterprise AI |
| Crypto for connector secrets | `secrets` (P209) |
| Access context | `authorization` (P208) |
| Search indexing events | Enterprise Search |

## Forbidden

- Sibling BC `data_discovery`, `data_inventory`, `metadata_platform`, `shadow_data`
- Undiscovered production assets
- Incomplete inventory as production-ready
- Invisible shadow data
- Module-local LLM SDKs for discovery AI
- Direct cloud SDK embeds (use Integration connectors)
