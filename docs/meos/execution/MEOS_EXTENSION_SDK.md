# MEOS Extension SDK

**Date:** 2026-08-18T11:30:00Z  
**Package:** `@marpich/plugin-sdk` **0.1.0** · `packages/plugin-sdk/`  
**SoR runtime:** Plugin Platform (`contexts/plugins`) — the SDK does **not** replace it.

## Principles (enforced by platform, not by packing a zip)

DDD · events · API-first · plugin-first · tenant JWT · permission grants · Policy Engine for business rules.  
Extensions talk to MEOS through REST, events, and declared extension points — **not** peer database imports.

## Commands (actual)

| Command | Behavior |
|---------|----------|
| `validate [path]` | Load JSON · `validateManifest` · exit 0/1 |
| `init <pluginId> [widget\|report] [--force]` | Write `marpich.plugin.json` |
| `pack` `sign` `publish` `test` `deploy` | **NOT_IMPLEMENTED** · **exit 2** |

`init` types other than widget/report are **rejected** (catalog types without seed evidence).  
Runtime: **plain Node ESM** (`src/*.js`). `tsc` / `dist/` is **not** required.

## Contracts exposed

| Contract | Where |
|----------|--------|
| EXTENSION / PLUGIN | `PLUGIN_MANIFEST.v1.json` + SDK types |
| API | OpenAPI `/api/v1` |
| EVENT | `docs/architecture/events/` including `plugin.*` |
| WEBHOOK / CONNECTOR | Integration Platform + `CONNECTOR_CATALOG.yaml` — **not** this CLI |
| WORKFLOW / AI_TOOL | Catalog plugin types only; **no** init scaffold |

## Examples (executable as JSON)

- `examples/com.marpich.demo-sales-widget/marpich.plugin.json`
- `examples/com.marpich.demo-report-pack/marpich.plugin.json`

Validated against the JSON Schema in `backend/tests/contracts/test_plugin_manifest_contract.py`.  
These match P322 DEMO seeds. **Not CERTIFIED.**

## What the SDK must not claim

- OS sandbox enforcement
- Cryptographic Ed25519 sign
- Marketplace publish
- Partner certification
- Python twin package (path does not exist)
