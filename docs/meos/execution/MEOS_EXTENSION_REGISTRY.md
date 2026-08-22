# MEOS Extension Registry

**Date:** 2026-08-18T07:45:00Z  
**Machine:** [MEOS_EXTENSION_REGISTRY.v1.yaml](./MEOS_EXTENSION_REGISTRY.v1.yaml)  
**SoR (runtime plugins):** `backend/contexts/plugins` · `/api/v1/plugins`  
**SoR (connectors):** `backend/contexts/integration` · P321 [MEOS_INTEGRATION_REGISTRY.md](./MEOS_INTEGRATION_REGISTRY.md)  
**SoR (first-party apps):** [MEOS_APPLICATION_REGISTRY.md](./MEOS_APPLICATION_REGISTRY.md)  
**Overall:** `production_active_count: 0` · `certified_count: 0` · **`NOT_CERTIFIED`**

Law: never mark **CERTIFIED**, **AVAILABLE**, or **ACTIVE** without evidence. Catalog trust labels (`community` / `verified`) are **not** certification.

## Lifecycle vocabulary

`DESIGNED` → `IMPLEMENTED` → `TESTED` → `CERTIFIED` → `AVAILABLE` → `INSTALLED` → `CONFIGURED` → `ACTIVE` → `SUSPENDED` → `DEPRECATED` → `REMOVED`

Honesty labels: `IMPLEMENTED_UNVERIFIED` · `NOT_IMPLEMENTED` · `BLOCKED`.

## Classification

| Class | Meaning in this registry |
|-------|--------------------------|
| **BUILT_IN** | First-party MEOS module / platform capability (not a marketplace SKU) |
| **FIRST_PARTY** | Marpich-owned demo or SDK artifact |
| **THIRD_PARTY** | External publisher listing — **none evidenced** |
| **INTERNAL_EXTENSION** | In-repo descriptor or studio UI that is not Plugin Platform SoR |
| **EXPERIMENTAL** | Seed / demo only |
| **DEPRECATED** | **none evidenced** |

## Inventory (actual)

### First-party applications (BUILT_IN)

Not marketplace products. Status lives in the Application Registry. **No app ACTIVE.** Wave 02 desks are TESTED on workstation Postgres; production cluster **BLOCKED** (G26).

### Plugin marketplace listings (FIRST_PARTY · EXPERIMENTAL)

| EXTENSION_ID | NAME | VERSION | TYPE | OWNER | CAPABILITIES | PERMISSIONS | TRUST (catalog) | SECURITY | LIFECYCLE |
|--------------|------|---------|------|-------|--------------|-------------|-----------------|----------|-----------|
| `com.marpich.demo-sales-widget` | Demo Sales KPI Widget | 1.0.0 | widget | `com.marpich` | `ui.dashboard.widget` | `analytics.read`, `sales.orders.read` | community | **NOT_CERTIFIED** | IMPLEMENTED_UNVERIFIED |
| `com.marpich.demo-report-pack` | Demo Financial Reports | 2.1.0 | report | `com.marpich` | `analytics.report.template` | `finance.reports.read` | verified | **NOT_CERTIFIED** | IMPLEMENTED_UNVERIFIED |

Dependencies: **none declared** beyond Plugin Platform + granted permissions.  
Tenant scope: installation row keyed by `tenant_id`.  
Data access: declared permissions only — **not** unrestricted DB/secrets/admin.  
Compatibility: semver on the listing; **no** min/max MEOS version field in the aggregate.  
Production INSTALLED / ACTIVE: **none evidenced**.

### Plugin types supported (catalog) with **zero** listings

`module` · `dashboard` · `theme` · `ai_skill` · `integration` · `workflow_extension` — types in `PLUGIN_CATALOG.yaml`. **Do not invent listings.**

### Connectors (P321)

Catalog **types** in `docs/architecture/integration/CONNECTOR_CATALOG.yaml` (bank_api, payment_gateway, messaging providers, LMS JSON stubs, LiveKit). Live production connectors: **0**. See Integration Registry.

### Automation packs (P319)

[MEOS_AUTOMATION_REGISTRY.md](./MEOS_AUTOMATION_REGISTRY.md) — **`BLOCK_AUTOMATION`**. Zero ACTIVE automations. Not marketplace SKUs.

### Internal / fragmented (not a second marketplace)

| ID | What it is | Classification | Status |
|----|------------|----------------|--------|
| `packages/plugin-sdk` | `marpich-plugin` pack/CLI | FIRST_PARTY tooling | IMPLEMENTED |
| `identity_federation` `BUILTIN_PROVIDER_PLUGINS` | IdP **protocol descriptors** (oidc/saml/ldap + vendor names) | INTERNAL_EXTENSION | IMPLEMENTED_UNVERIFIED — external IdP production **NOT_AVAILABLE** |
| EIS “Connector marketplace” UI | Studio seed table | INTERNAL_EXTENSION | IMPLEMENTED — **not** Plugin Platform SoR |

Vendor names in federation descriptors (Okta, Auth0, …) are **not** third-party marketplace products and **not** certified partner apps.

### Not found as marketplace products

Third-party plugins · partner listings · knowledge extensions · certified AI tools · workflow template packs · deprecated extensions.

## Required fields (governance)

Each extension **should** have: EXTENSION_ID, NAME, VERSION, TYPE, OWNER, DESCRIPTION, CAPABILITIES, DEPENDENCIES, PERMISSIONS, TENANT_SCOPE, DATA_ACCESS, COMPATIBILITY, SECURITY_STATUS, LIFECYCLE_STATUS.

**Gap:** Plugin aggregate stores id, type, name, description, publisher, version, permissions, extension points, sandbox, trust, signature fingerprints. It does **not** store CERTIFIED, min/max MEOS version, data-retention class, or supply-chain attestation. Those remain documentation / future Policy Engine fields — **not invented as populated.**
