# Marpich Platform Charter

**Status:** Canonical — non-negotiable product and architecture law  
**Audience:** Product, engineering, AI agents, integrators  
**Architect role:** [Chief Enterprise Architect Mandate](CHIEF_ARCHITECT_MANDATE.md)

---

## Vision

**Marpich is one platform — not many systems.**

Everything is a **module**. Everything is **configurable**, **reusable**, and **replaceable**. Each customer enables only the modules they need. All industries share one **Core Platform**.

| Customer | Modules they enable |
|----------|---------------------|
| Universities | Education modules |
| Hospitals | Healthcare modules |
| Banks | Banking modules |
| Currency exchanges | Exchange modules |
| Government | Government modules |
| Construction companies | Construction modules |
| Real estate companies | Property modules |
| Manufacturing companies | Manufacturing modules |
| Hotels | Hospitality modules |
| Restaurants | Restaurant modules |
| Retail | POS modules |
| Accounting firms | Accounting modules |
| Tax companies | Tax modules |

**All of them use the same Core Platform.**

**Marpich supports unlimited industries.** Current domains: [Industry Catalog](INDUSTRY_CATALOG.md) · packs: `backend/shared/contracts/industry_packs.json`

See also: [BUSINESS_CAPABILITIES_REGISTRY.md](BUSINESS_CAPABILITIES_REGISTRY.md), [CORE_PLATFORM_DESIGN.md](CORE_PLATFORM_DESIGN.md), [INDUSTRY_CATALOG.md](INDUSTRY_CATALOG.md), [MODULE_SYSTEM.md](MODULE_SYSTEM.md), [MODULE_ARCHITECTURE.md](MODULE_ARCHITECTURE.md), [MODULE_STRUCTURE_STANDARD.md](MODULE_STRUCTURE_STANDARD.md), [DDD_DOMAIN_ARCHITECTURE.md](DDD_DOMAIN_ARCHITECTURE.md), [COMMUNICATION_ARCHITECTURE.md](COMMUNICATION_ARCHITECTURE.md), [API_GATEWAY_ARCHITECTURE.md](API_GATEWAY_ARCHITECTURE.md), [INTEGRATION_PLATFORM.md](INTEGRATION_PLATFORM.md), [ENTERPRISE_EVENT_BUS.md](ENTERPRISE_EVENT_BUS.md), [ENTERPRISE_WORKFLOW_ENGINE.md](ENTERPRISE_WORKFLOW_ENGINE.md), [ENTERPRISE_NOTIFICATION_PLATFORM.md](ENTERPRISE_NOTIFICATION_PLATFORM.md), [ENTERPRISE_SEARCH_ENGINE.md](ENTERPRISE_SEARCH_ENGINE.md), [ENTERPRISE_DOCUMENT_EXCHANGE.md](ENTERPRISE_DOCUMENT_EXCHANGE.md), [ENTERPRISE_AUDIT_PLATFORM.md](ENTERPRISE_AUDIT_PLATFORM.md), [ENTERPRISE_OBSERVABILITY_PLATFORM.md](ENTERPRISE_OBSERVABILITY_PLATFORM.md), [ENTERPRISE_POLICY_ENGINE.md](ENTERPRISE_POLICY_ENGINE.md), [ENTERPRISE_COMPLIANCE_FRAMEWORK.md](ENTERPRISE_COMPLIANCE_FRAMEWORK.md), [AI_PLATFORM_STANDARD.md](AI_PLATFORM_STANDARD.md), [SECURITY_STANDARD.md](SECURITY_STANDARD.md), [CORE_PLATFORM.md](CORE_PLATFORM.md), [DDD_ARCHITECTURE.md](DDD_ARCHITECTURE.md).

---

## Core vs Module

```
┌─────────────────────────────────────────────────────────────┐
│                      CORE PLATFORM                           │
│  Identity · Tenant · Permissions · Audit · Notifications   │
│  Workflow · Documents · Settings · Search · Localization     │
│  AI · Analytics · Integration · Scheduling · Secrets · …   │
│  (29 enterprise services — NO business logic)                │
└────────────────────────────┬────────────────────────────────┘
                             │ extends (never replaces)
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
   healthcare.*        education.*          banking.*
   (domain only)       (domain only)        (domain only)
```

| Rule | Meaning |
|------|---------|
| **Every module extends the Core** | Industry code adds domain aggregates, rules, and events — it consumes platform services |
| **No module replaces the Core** | A hospital module never ships its own auth, audit, or notification stack |

---

## Forbidden — Never Duplicate

These are **hard prohibitions**. If implementation feels like copying, the capability belongs in Core or as a plugin.

| Never duplicate | Use instead |
|-----------------|-------------|
| Business logic | Core service or shared domain submodule + events |
| APIs | One REST prefix per platform capability (`/audit`, `/notifications`, …) |
| Database tables | Platform schemas + module `{context}_*` tables with `tenant_id` |
| Permissions | Global catalog `module.resource.action` registered at module activation |
| Reports | Report Engine — modules supply data hooks only |
| Notifications | Notification Service — modules emit events or call one API |

### Anti-patterns (forbidden)

- Copying finance for Islamic banking → extend with `finance.islamic-products`
- Separate database per industry → tenant-scoped schemas + RLS
- Hardcoded industry logic in platform core → industry packs + module config
- Direct HTTP between bounded contexts → integration events + outbox ([COMMUNICATION_ARCHITECTURE.md](COMMUNICATION_ARCHITECTURE.md))
- Cross-database access between modules → **rejected** — REST, events, or scheduled sync only
- Shared mutable state between services → [SERVICE_BOUNDARIES.md](SERVICE_BOUNDARIES.md)
- Shared mutable state between modules → events + read models

---

## Required — Every Feature Must Support

No feature ships unless it satisfies **all** dimensions below.

| Dimension | Platform owner | Module responsibility |
|-----------|----------------|---------------------|
| **Configurable** | Settings Service | Declare JSON Schema config; no hardcoded tenant behavior |
| **Plugins** | Extension registry | Register workflow hooks, custom fields, webhooks, UI widgets |
| **AI** | AI Service — **platform service, not optional** | All 14 surfaces per [AI_PLATFORM_STANDARD.md](AI_PLATFORM_STANDARD.md) |
| **Audit logs** | Audit Service | Publish auditable integration events; call audit API when sync required |
| **Permissions** | Permission + Authorization | Register permissions at activation; guard every mutating API |
| **Localization** | Localization Service | Externalize strings; honor `Accept-Language` |
| **Multi-currency** | Finance / platform | Currency on monetary values; tenant default in settings |
| **Multi-language** | Localization Service | UI + document templates per locale |
| **Multi-tenant** | Core Platform | `tenant_id` on every table, API command, and event envelope |

---

## Module Implementation Contract

When adding or changing a module:

1. **Register permissions** at `platform.module.activated` — no local RBAC silos.
2. **Publish/subscribe integration events** — Enterprise Event Bus; see [ENTERPRISE_EVENT_BUS.md](ENTERPRISE_EVENT_BUS.md).
3. **Emit audit-relevant facts** — Audit Service consumes events or receives sync writes.
4. **Route notifications** through Notification Service — [ENTERPRISE_NOTIFICATION_PLATFORM.md](ENTERPRISE_NOTIFICATION_PLATFORM.md); no SMTP/push logic in domain code.
5. **Expose tenant config** via Settings — validated against module JSON Schema.
6. **Declare plugin extension points** — workflows ([ENTERPRISE_WORKFLOW_ENGINE.md](ENTERPRISE_WORKFLOW_ENGINE.md)), reports, custom fields.
7. **Wire all AI surfaces** — mandatory platform service; see [AI_PLATFORM_STANDARD.md](AI_PLATFORM_STANDARD.md).
8. **Scope every operation** by `tenant_id`, locale, and currency.

### Module anatomy (reference)

```typescript
interface IModuleManifest {
  moduleId: string;           // e.g. "healthcare.patient-management"
  moduleVersion: string;
  displayName: string;
  category: ModuleCategory;
  industryPacks: string[];
  dependencies: string[];
  permissions: ModulePermission[];
  entities: ModuleEntity[];
  apiRoutes: ModuleApiRoute[];
  eventSubscriptions: string[];
  eventPublications: string[];
  configSchema: object;       // JSON Schema — required
  pluginHooks: string[];      // extension point IDs — required
  aiSurfaces: AiSurfaceManifest; // all 14 surfaces — required
}
```

`AiSurfaceManifest` — see [AI_PLATFORM_STANDARD.md](AI_PLATFORM_STANDARD.md).

```typescript
// Legacy reference — use aiSurfaces instead of aiHooks alone
interface IModuleManifestLegacyAi {
  aiHooks: string[];
}
```

Industry pack catalog: `backend/shared/contracts/industry_packs.json`.

---

## Activation Flow (one platform, many shapes)

```
1. Tenant created with industryPack = "hospital"
2. Core Platform resolves required + optional modules from pack
3. Module Registry validates dependency DAG
4. For each module:
   a. Run migration (tenant-scoped schema)
   b. Seed default configuration (Settings)
   c. Register permissions (Permission Service)
   d. Register API routes (Gateway)
   e. Subscribe to integration events
5. Emit platform.tenant.provisioned / platform.module.activated
6. AI layer loads domain models for activated modules
```

---

## Enforcement

| Mechanism | Location |
|-----------|----------|
| Cursor agent rule | `.cursor/rules/marpich-platform-charter.mdc` |
| Chief architect rule | `.cursor/rules/marpich-chief-architect.mdc` |
| Chief architect mandate | [CHIEF_ARCHITECT_MANDATE.md](CHIEF_ARCHITECT_MANDATE.md) |
| DDD domain rule | `.cursor/rules/marpich-ddd-domains.mdc` |
| DDD domain architecture | [DDD_DOMAIN_ARCHITECTURE.md](DDD_DOMAIN_ARCHITECTURE.md) |
| Engineering quality rule | `.cursor/rules/marpich-engineering-quality.mdc` |
| AI platform rule | `.cursor/rules/marpich-ai-platform.mdc` |
| Development protocol rule | `.cursor/rules/marpich-development-protocol.mdc` |
| Development protocol | [DEVELOPMENT_PROTOCOL.md](DEVELOPMENT_PROTOCOL.md) |
| Module structure | [MODULE_STRUCTURE_STANDARD.md](MODULE_STRUCTURE_STANDARD.md) |
| Module architecture (identical tree) | [MODULE_ARCHITECTURE.md](MODULE_ARCHITECTURE.md) |
| Dependency graph | [DEPENDENCY_GRAPH.md](DEPENDENCY_GRAPH.md) |
| Communication architecture | [COMMUNICATION_ARCHITECTURE.md](COMMUNICATION_ARCHITECTURE.md) |
| Communication rule | `.cursor/rules/marpich-communication-architecture.mdc` |
| API Gateway architecture | [API_GATEWAY_ARCHITECTURE.md](API_GATEWAY_ARCHITECTURE.md) |
| API Gateway rule | `.cursor/rules/marpich-api-gateway.mdc` |
| Integration Platform | [INTEGRATION_PLATFORM.md](INTEGRATION_PLATFORM.md) |
| Integration rule | `.cursor/rules/marpich-integration-platform.mdc` |
| Enterprise Event Bus | [ENTERPRISE_EVENT_BUS.md](ENTERPRISE_EVENT_BUS.md) |
| Event Bus rule | `.cursor/rules/marpich-event-bus.mdc` |
| Enterprise Workflow Engine | [ENTERPRISE_WORKFLOW_ENGINE.md](ENTERPRISE_WORKFLOW_ENGINE.md) |
| Workflow rule | `.cursor/rules/marpich-workflow-engine.mdc` |
| Enterprise Notification Platform | [ENTERPRISE_NOTIFICATION_PLATFORM.md](ENTERPRISE_NOTIFICATION_PLATFORM.md) |
| Notification rule | `.cursor/rules/marpich-notification-platform.mdc` |
| Enterprise Search Engine | [ENTERPRISE_SEARCH_ENGINE.md](ENTERPRISE_SEARCH_ENGINE.md) |
| Search rule | `.cursor/rules/marpich-search-engine.mdc` |
| Enterprise Document Exchange | [ENTERPRISE_DOCUMENT_EXCHANGE.md](ENTERPRISE_DOCUMENT_EXCHANGE.md) |
| Document Exchange rule | `.cursor/rules/marpich-document-exchange.mdc` |
| Enterprise Audit Platform | [ENTERPRISE_AUDIT_PLATFORM.md](ENTERPRISE_AUDIT_PLATFORM.md) |
| Audit Platform rule | `.cursor/rules/marpich-audit-platform.mdc` |
| Audit event catalog | `docs/architecture/audit/AUDIT_CATALOG.yaml` |
| Enterprise Observability Platform | [ENTERPRISE_OBSERVABILITY_PLATFORM.md](ENTERPRISE_OBSERVABILITY_PLATFORM.md) |
| Observability rule | `.cursor/rules/marpich-observability-platform.mdc` |
| Metrics catalog | `docs/architecture/observability/METRICS_CATALOG.yaml` |
| Health dashboard | `docs/architecture/observability/HEALTH_DASHBOARD.v1.yaml` |
| Enterprise Policy Engine | [ENTERPRISE_POLICY_ENGINE.md](ENTERPRISE_POLICY_ENGINE.md) |
| Policy Engine rule | `.cursor/rules/marpich-policy-engine.mdc` |
| Policy domain catalog | `docs/architecture/policy/POLICY_DOMAIN_CATALOG.yaml` |
| Policy definition schema | `docs/architecture/policy/POLICY_DEFINITION_SCHEMA.v1.yaml` |
| Enterprise Compliance Framework | [ENTERPRISE_COMPLIANCE_FRAMEWORK.md](ENTERPRISE_COMPLIANCE_FRAMEWORK.md) |
| Compliance rule | `.cursor/rules/marpich-compliance-framework.mdc` |
| Compliance domain catalog | `docs/architecture/compliance/COMPLIANCE_DOMAIN_CATALOG.yaml` |
| Compliance dashboard | `docs/architecture/compliance/COMPLIANCE_DASHBOARD.v1.yaml` |
| Enterprise Feature Flag System | [ENTERPRISE_FEATURE_FLAG_SYSTEM.md](ENTERPRISE_FEATURE_FLAG_SYSTEM.md) |
| Feature Flag rule | `.cursor/rules/marpich-feature-flags.mdc` |
| Flag catalog | `docs/architecture/feature_flags/FLAG_CATALOG.yaml` |
| Feature dashboard | `docs/architecture/feature_flags/FEATURE_DASHBOARD.v1.yaml` |
| Enterprise Plugin Platform | [ENTERPRISE_PLUGIN_PLATFORM.md](ENTERPRISE_PLUGIN_PLATFORM.md) |
| Plugin Platform rule | `.cursor/rules/marpich-plugin-platform.mdc` |
| Plugin catalog | `docs/architecture/plugins/PLUGIN_CATALOG.yaml` |
| Marketplace architecture | `docs/architecture/plugins/MARKETPLACE_ARCHITECTURE.md` |
| Plugin SDK | `packages/plugin-sdk/` |
| Enterprise Financial Kernel | [ENTERPRISE_FINANCIAL_KERNEL.md](ENTERPRISE_FINANCIAL_KERNEL.md) |
| Financial Kernel rule | `.cursor/rules/marpich-financial-kernel.mdc` |
| Financial engines catalog | `docs/architecture/financial_kernel/FINANCIAL_ENGINES.v1.yaml` |
| COA templates | `docs/architecture/financial_kernel/CHART_OF_ACCOUNTS.v1.yaml` |
| Industry financial packs | `docs/architecture/financial_kernel/INDUSTRY_FINANCIAL_PACKS.yaml` |
| Enterprise General Ledger | [ENTERPRISE_GENERAL_LEDGER.md](ENTERPRISE_GENERAL_LEDGER.md) |
| GL catalog | `docs/architecture/financial_kernel/GL_CATALOG.yaml` |
| Document types catalog | `docs/architecture/documents/DOCUMENT_TYPES.yaml` |
| Search modes catalog | `docs/architecture/search/SEARCH_MODES.yaml` |
| Notification channel catalog | `docs/architecture/notifications/CHANNEL_CATALOG.yaml` |
| Workflow definition schema | `docs/architecture/workflow/DEFINITION_SCHEMA.v1.yaml` |
| Connector catalog | `docs/architecture/integration/CONNECTOR_CATALOG.yaml` |
| Route registry | `backend/core/gateway/route_registry.yaml` |
| Architecture validation | [ARCHITECTURE_VALIDATION.md](ARCHITECTURE_VALIDATION.md) |
| AI platform | [AI_PLATFORM_STANDARD.md](AI_PLATFORM_STANDARD.md) |
| Performance rule | `.cursor/rules/marpich-performance.mdc` |
| Performance standard | [PERFORMANCE_STANDARD.md](PERFORMANCE_STANDARD.md) |
| Security rule | `.cursor/rules/marpich-security.mdc` |
| Security standard | [SECURITY_STANDARD.md](SECURITY_STANDARD.md) |
| Industry catalog | [INDUSTRY_CATALOG.md](INDUSTRY_CATALOG.md) |
| Industry catalog rule | `.cursor/rules/marpich-industry-catalog.mdc` |
| Long-horizon rule | `.cursor/rules/marpich-long-horizon.mdc` |
| Long-horizon architecture | [LONG_HORIZON_ARCHITECTURE.md](LONG_HORIZON_ARCHITECTURE.md) |
| Engineering standard | [ENGINEERING_QUALITY_STANDARD.md](ENGINEERING_QUALITY_STANDARD.md) |
| Contract tests | `backend/tests/contracts/` |
| Bounded context registry | `backend/contexts/registry.py` |
| ADR-005 Module composition | `docs/adr/005-module-composition.md` |
| ADR-009 Core Platform services | `docs/adr/009-core-platform-services.md` |
| ADR-034 Communication architecture | `docs/adr/034-communication-architecture.md` |
| ADR-035 API Gateway | `docs/adr/035-api-gateway.md` |
| ADR-036 Integration Platform | `docs/adr/036-integration-platform.md` |
| ADR-037 Enterprise Event Bus | `docs/adr/037-enterprise-event-bus.md` |
| ADR-038 Enterprise Workflow Engine | `docs/adr/038-enterprise-workflow-engine.md` |
| ADR-039 Notification Platform | `docs/adr/039-notification-platform.md` |
| ADR-040 Search Engine | `docs/adr/040-search-engine.md` |
| ADR-041 Document Exchange | `docs/adr/041-document-exchange.md` |
| ADR-042 Audit Platform | `docs/adr/042-audit-platform.md` |
| ADR-043 Observability Platform | `docs/adr/043-observability-platform.md` |
| ADR-044 Policy Engine | `docs/adr/044-policy-engine.md` |
| ADR-045 Compliance Framework | `docs/adr/045-compliance-framework.md` |
| ADR-046 Feature Flag System | `docs/adr/046-feature-flag-system.md` |
| ADR-047 Plugin Platform | `docs/adr/047-plugin-platform.md` |
| ADR-048 Pre-implementation validation | `docs/adr/048-pre-implementation-validation-dimensions.md` |
| ADR-049 Financial Kernel | `docs/adr/049-financial-kernel.md` |
| ADR-050 Enterprise General Ledger | `docs/adr/050-enterprise-general-ledger.md` |

**When in doubt:** extend Core, configure per tenant, integrate via events — never fork.

---

## Engineering Quality

All generated code must satisfy the **[Engineering Quality Standard](ENGINEERING_QUALITY_STANDARD.md)** — enterprise-grade qualities and the full feature checklist (logging, monitoring, metrics, tracing, tests, accessibility, RTL/LTR, dark mode, etc.). **Never skip any item.**
