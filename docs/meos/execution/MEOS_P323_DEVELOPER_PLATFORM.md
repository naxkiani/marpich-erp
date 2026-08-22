# MEOS P323 — Enterprise Developer Platform

**Date:** 2026-08-18T11:30:00Z  
**Decision:** Developer experience is **the existing Plugin SDK + OpenAPI + event schemas + pytest/CI + local compose**, hardened so stubs cannot look like success. **Not** a new SDK ecosystem, API platform, CI/CD, plugin engine, or MEOS rebuild.  
**Maturity:** `DOCUMENTED` → `DEVELOPABLE` (manifest/init) → `TESTABLE` (contracts + plugin API tests) — **not** CERTIFIABLE / PUBLISHABLE / OPERABLE as a live partner program.  
**P324:** opened as release-engineering governance. **Not** RELEASE_CANDIDATE.

## 1. Actual P322 status (precondition)

| Signal | Actual |
|--------|--------|
| P322 | Extension governance **IMPLEMENTED** (install ≠ activate). **0 CERTIFIED. 0 production ACTIVE.** |
| P321 | Integration fabric **IMPLEMENTED**. **0 ACTIVE** integrations |
| P320 | UX **FUNCTIONAL**; G20/G21 not certified |
| P319 | **`BLOCK_AUTOMATION`** |
| `EXTENSION_STATE` | 2 DEMO seeds; marketplace not CERTIFIED |
| `PLUGIN_STATE` | SoR `contexts/plugins` |
| `API_STATE` | `/api/v1` + OpenAPI |
| `EVENT_STATE` | Outbox + versioned schemas (plugin events registered in P323) |
| `AI_STATE` | Assist **stub** (G18) |
| `CI_CD_STATE` | GitHub Actions smoke/contract workflows — **not** a plugin certification factory |
| `SECURITY_STATE` | **TRUST_CRITICAL** · production **false** (G26) |

## 2. Developer platform inventory (actual)

| Asset | Path | Status |
|-------|------|--------|
| Plugin SDK | `packages/plugin-sdk` | Types + validate + init |
| Plugin CLI | `marpich-plugin` (`src/cli.ts`) | validate/init **real**; pack/sign/publish **fail closed** |
| Module scaffold | `backend/contexts/_template/` | FIRST_PARTY module tree — not marketplace SKU |
| Manifest schema | `docs/architecture/plugins/PLUGIN_MANIFEST.v1.json` | Canonical |
| Connector type schemas | `docs/architecture/integration/connectors/*.json` | DESIGNED types |
| Event schemas | `docs/architecture/events/*.json` | Including `plugin.*` (P323) |
| OpenAPI | `/api/openapi.json` · `/api/docs` | Generated from routers |
| Contract tests | `backend/tests/contracts/` | pytest |
| Plugin API tests | `contexts/plugins/tests/test_plugin_flow.py` | 7 passed (P322) |
| Local stack | `infrastructure/docker/compose/docker-compose.dev.yml` + `scripts/dev-up.sh` | LOCAL |
| CI | `.github/workflows/meos-*.yml` | Existing; not a second CI product |
| Examples | `packages/plugin-sdk/examples/com.marpich.demo-*` | Seed-aligned |
| EIS “developer portal” | Integration Studio UI | **Fragmented** — not SoR |
| Federation `protocol_plugin_sdk.py` | identity_federation | INTERNAL IdP adapters — **not** Plugin SDK |
| Python plugin-sdk package | README previously claimed | **NOT_IMPLEMENTED** |
| Partner developer registry | — | **NOT_IMPLEMENTED** (use Identity) |

## 3. Developer registry

No new identity system. Publishers use existing JWT + `plugins.publish` / `plugins.install` / `plugins.admin`.  
Developer / team / org / certification status table: **NOT_IMPLEMENTED**. Do not invent partner tenants.

## 4–7. SDK, CLI, templates

See [MEOS_EXTENSION_SDK.md](./MEOS_EXTENSION_SDK.md).  
Templates: **widget** and **report** only (seed evidence). No AI/workflow/connector marketplace templates invented.

## 8–9. API and event DX

- API: FastAPI OpenAPI; contract path `/api/v1/plugins/marketplace/listings` added to `test_openapi_contract.py`. Auth: JWT + permissions. Tenant: `X-Tenant-ID`.  
- Events: plugin lifecycle schemas registered (`plugin.registered` … `plugin.sandbox.violation`) with envelope `allOf`; `contexts.plugins` added to `event_samples.INTEGRATION_EVENT_MODULES`. **TESTED** (27 plugin-filtered contract tests). Some older event files (e.g. hospital/accounting) are **payload-only** schemas — pre-existing mismatch vs envelope validator, not changed in P323.

## 10–14. Plugin / connector / workflow / automation / AI development

| Track | Developer path | Certification |
|-------|----------------|---------------|
| Plugin | init → validate → Platform install/enable APIs | CERTIFY **not available** |
| Connector | Integration Platform + catalog JSON | P321 **0 ACTIVE** |
| Workflow | Workflow Engine + Task Center | No `workflow_extension` listings |
| Automation | P319 registry | **BLOCK_AUTOMATION** |
| AI tool | `ai_skill` type only | Assist stub; **0 listings** |

Pack/sign/publish CLI **must not** be used as a production install path (exits 2).

## 15–21. Tenancy, security, tests, contracts

- Tenant isolation: **TESTED** on plugin installs (P322). Cross-tenant search/events: **not** a dedicated SDK suite.  
- Security testing: permission denial + auth on plugin routes (**TESTED**). Privilege-escalation matrix / secret scanning in CLI: **NOT_AVAILABLE**.  
- Contract tests: OpenAPI + event schemas + plugin manifest examples (P323).  
- Quality gates in CI: existing pytest/smoke. Lint/typecheck of plugin-sdk: **PARTIAL** (no published `tsc` build evidenced in CI).

## 22–26. CI/CD, artifacts, versioning, compatibility

Reuse GitHub Actions. **Do not create a second CI platform.**  
Artifacts: git tree + demo checksums. npm publish of `@marpich/plugin-sdk`: **NOT_EVIDENCED**.  
SDK version `0.1.0`. API **v1**. Breaking CLI stubs now fail closed — intentional honesty, not a certified-extension break (none certified).

## 27–30. Portal, search, examples, sandbox

See [MEOS_DEVELOPER_PORTAL.md](./MEOS_DEVELOPER_PORTAL.md).  
Global Search remains Enterprise Search — no second search.  
LOCAL compose ≠ partner sandbox ≠ production. Production credentials **must not** be required for `validate`/`init`.

## 31–39. Publish, observability, audit, partners, fabrics

Publishing: Plugin Platform `plugins.publish` + P322 lifecycle. End-to-end CERTIFY→PUBLISH in production: **NOT_AVAILABLE**.  
Observability: existing OTel/plugin dashboard counters; `sandbox_violations_24h` hardcoded 0.  
Audit: plugin integration events.  
Partners: **none**.  
P321/P319/P320 reused, not duplicated.

## Architecture validation scorecard

| Dimension | Score | Pass? |
|-----------|-------|-------|
| Architecture | 4 | Yes — reuse SDK + contracts + CI |
| DDD | 4 | Yes — no new bounded context |
| Security | 4 | Fail-closed stubs; JWT/permissions unchanged |
| Scalability | 3 | Local/dev only |
| Performance | 3 | No DX perf evidence |
| Testing | 4 | Manifest + plugin event contracts |
| AI Integration | 3 | No AI SDK surface beyond catalog type |
| Documentation | 4 | Honest CLI/README |
| Accessibility | 3 | No new portal UI (G21 still FAIL) |
| Localization | 3 | SDK CLI English |
| Observability | 3 | Reuse platform |
| Workflow | 3 | Engine exists; no extension listings |
| Audit | 4 | plugin.* schemas |
| Policy Compliance | 3 | Certification gates remain documentary |
| Plugin Compatibility | 4 | Manifest aligned to catalog |

**Verdict:** ENTERPRISE_GRADE as **developer-tooling honesty/governance**. Partner **PUBLISHABLE** path: **No**.

## Reuse analysis

Reused Plugin SDK, Plugin Platform, OpenAPI, event validator, pytest contracts, docker-compose.dev, GitHub workflows, Identity permissions, P322 marketplace, P321 connectors, P319 automation block.  
Rejected: new microservice framework, new CI, invented portal product, fake pack/sign success.

## Required next action

Production cluster (G26) remains the operational blocker. Then: real signing, schema-backed CERTIFY, npm/CI packaging of the SDK — still on Plugin Platform, not a new engine.
