# Marpich Plugin SDK

Official **manifest types and validator** for third-party Marpich plugins.

**Canonical docs:** [ENTERPRISE_PLUGIN_PLATFORM.md](../../docs/architecture/ENTERPRISE_PLUGIN_PLATFORM.md)  
**Manifest schema:** [PLUGIN_MANIFEST.v1.json](../../docs/architecture/plugins/PLUGIN_MANIFEST.v1.json)  
**P323:** [MEOS_EXTENSION_SDK.md](../../docs/meos/execution/MEOS_EXTENSION_SDK.md)

SDK version: **0.1.0** (`package.json`). Not a certified runtime.

---

## What is real

| Capability | Status |
|------------|--------|
| Types + `validateManifest` | **IMPLEMENTED** |
| `marpich-plugin validate [path]` | **IMPLEMENTED** (manifest JSON only) |
| `marpich-plugin init <id> [widget\|report]` | **IMPLEMENTED** (writes `marpich.plugin.json`) |
| Examples matching P322 seeds | `examples/com.marpich.demo-*` |
| `pack` / `sign` / `publish` / `test` / `deploy` | **NOT_IMPLEMENTED** (CLI **exits 2**) |
| Python package `packages/plugin-sdk/python/` | **NOT_IMPLEMENTED** |
| Cryptographic signing / CVE scan | **NOT_AVAILABLE** |
| CERTIFIED / marketplace publish | **No** — P322 `certified_count: 0` |

Do not treat a valid manifest as a signed package or a certified listing.

---

## Plugin types

| Type | Extension point | `init` scaffold? |
|------|-----------------|------------------|
| `widget` | `ui.dashboard.widget` | Yes (seed evidence) |
| `report` | `analytics.report.template` | Yes (seed evidence) |
| `module` `dashboard` `theme` `ai_skill` `integration` `workflow_extension` | catalog | **No** — type exists, no seed listing |

---

## Quick start

```bash
# Validate this repo's seed example (plain Node — no tsc)
node packages/plugin-sdk/src/cli.js validate \
  packages/plugin-sdk/examples/com.marpich.demo-sales-widget/marpich.plugin.json

# From a new directory — writes DEMO scaffold (not CERTIFIED)
node /path/to/packages/plugin-sdk/src/cli.js init com.marpich.example-widget widget
```

`npx @marpich/plugin-sdk` requires a published npm package — **not evidenced** as published. Use the in-repo CLI.

---

## Manifest example

See `examples/com.marpich.demo-sales-widget/marpich.plugin.json` (matches Plugin Platform seed). Checksum fields are **demo fingerprints**, not production signatures.

---

## Runtime integration

Host applications invoke plugins via `IPluginRuntime` (`backend` Plugin Platform). Invoke requires tenant install **and** enable (P322). Listings are not production ACTIVE.

---

## Forbidden

- Direct imports of platform internals
- Treating CLI stubs as successful pack/sign/publish
- Unsigned packages in production
- Requesting undeclared permissions at runtime
