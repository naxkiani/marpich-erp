# MEOS Marketplace Governance

**Date:** 2026-08-18T07:45:00Z  
**SoR:** Plugin Platform (`/api/v1/plugins`) + Application Registry + Integration Fabric (P321)  
**UI:** `/enterprise/plugins` · `PluginMarketplacePage` (P320 AppShell)  
**Law:** This is **extension discovery and lifecycle**, not a generic e-commerce store and not a second plugin engine.

## What is discoverable today

| Category | Exposed? | Evidence |
|----------|----------|----------|
| PLUGINS | Yes | `GET /api/v1/plugins/marketplace/listings` — 2 DEMO seeds |
| APPLICATIONS | Yes (nav/registry) | First-party apps — **not** store SKUs |
| CONNECTORS / INTEGRATIONS | Types + P321 registry | **0 ACTIVE** live partners |
| REPORTING_PACKS | One seed | `com.marpich.demo-report-pack` |
| AUTOMATION_PACKS | Registry only | P319 `BLOCK_AUTOMATION` |
| DASHBOARDS / AI_TOOLS / WORKFLOW_TEMPLATES | Type exists | **No listings** |
| KNOWLEDGE_EXTENSIONS | No | **NOT_IMPLEMENTED** |

Do not publish empty categories as populated storefronts.

## Discovery (reuse P320)

- Marketplace page uses AppShell / PageLayout, design tokens, local listing filters (`q`, `type`, `trust`).  
- Global Search remains Enterprise Search (`/api/v1/search`). **No second search engine.**  
- EIS “Connector marketplace” is a **fragmented** studio table. Operators must treat Integration Platform + Plugin Platform as SoR.

Install / activate / configure / invoke require `plugins.install` / `plugins.invoke` and a tenant JWT. Unauthenticated browse of business listings is not a public storefront.

## Trust labels vs certification

| Label | Source | Meaning |
|-------|--------|---------|
| `community` / `verified` / `enterprise` | Plugin catalog enum | **Catalog metadata only** |
| FIRST_PARTY / THIRD_PARTY | This governance doc | Ownership class |
| CERTIFIED | [MEOS_PLUGIN_CERTIFICATION.md](./MEOS_PLUGIN_CERTIFICATION.md) | **No listing has passed** |

Never display seed `verified` as a security certification. UI copy: `plugins.notCertified`.

## Publishing

API: `POST /api/v1/plugins/marketplace/submissions` (`plugins.publish`) + register.  
Pipeline in architecture docs: author → submit → validate → review → publish.  
**Production publishing ops, publisher identity proofing, and CVE scanning: NOT_AVAILABLE.** Signature check is a **format** check (`sha256:` prefix + fingerprint present), not cryptographic certification.

## Internal vs external

| Class | Trust default |
|-------|----------------|
| BUILT_IN modules | Platform — still not CERTIFIED for production go-live (P313) |
| FIRST_PARTY demo listings | DEMO — must not auto-activate |
| Partner / THIRD_PARTY | **None listed** — would start UNVERIFIED |

## Commerce

Pricing, ratings, reviews, paid checkout: **architecture-mentioned, NOT_IMPLEMENTED** as a store. Do not invent products or partners.
