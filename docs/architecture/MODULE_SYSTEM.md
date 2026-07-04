# Module System

## Core Principle

**Never build separate systems.** Every industry capability is a composable module that registers with the platform kernel.

**Every business capability must become a module.** See **[Module Structure Standard](MODULE_STRUCTURE_STANDARD.md)** for required layers, integrations, and anti-monolith rules.

## Module Anatomy

```typescript
interface IModuleManifest {
  moduleId: string;           // e.g. "healthcare.patient-management"
  moduleVersion: string;      // semver
  displayName: string;
  category: ModuleCategory;
  industryPacks: string[];    // which packs can use this
  dependencies: string[];     // required modules
  permissions: ModulePermission[];
  entities: ModuleEntity[];
  apiRoutes: ModuleApiRoute[];
  eventSubscriptions: string[];
  eventPublications: string[];
  settingsSchema: object;
  aiSurfaces: AiSurfaceManifest;  // required — see AI_PLATFORM_STANDARD.md
  workflowHooks: string[];
  reportTemplates: string[];
  searchEntities: string[];
  localizationNamespace: string;
}
```

### Required layers & integrations (canonical)

Every module must include: **Domain · Application · Infrastructure · Presentation · API · Permissions · Events · Tests · Documentation · Settings · [AI (14 surfaces)](AI_PLATFORM_STANDARD.md) · Analytics · Workflow · Reports · Notifications · Search · Localization**. Details: [MODULE_STRUCTURE_STANDARD.md](MODULE_STRUCTURE_STANDARD.md).

## Module ID Convention

```
{namespace}.{capability}

Namespaces:
  platform.*     — core platform services
  finance.*      — financial domain
  healthcare.*   — healthcare domain
  education.*    — education domain
  logistics.*    — supply chain
  retail.*       — retail & POS
  hospitality.*  — hotels & restaurants
  real-estate.*  — property
  construction.* — construction & engineering
  government.*   — public sector
  ngo.*          — non-profits
  manufacturing.*— production
  ai.*           — AI capabilities
```

## Activation Flow

```
1. Tenant created with industryPack = "hospital"
2. Tenant Service resolves required + optional modules from pack
3. Module Registry validates dependency graph (topological sort)
4. For each module:
   a. Run migration (schema-per-tenant or shared + RLS)
   b. Seed default configuration
   c. Register API routes in Gateway
   d. Subscribe to integration events
5. Emit IndustryPackActivated event
6. AI layer loads domain-specific models for activated modules
```

## Dependency Resolution

Modules form a directed acyclic graph (DAG). The registry rejects circular dependencies.

```
platform.core
  └── platform.identity
        └── platform.tenant
              └── [domain modules...]

healthcare.patient-management
  ├── platform.core
  ├── platform.identity
  └── platform.documents

healthcare.clinical
  ├── healthcare.patient-management
  └── platform.workflow
```

## Configuration

Each module exposes a JSON Schema configuration block stored per tenant:

```json
{
  "moduleId": "healthcare.billing",
  "tenantId": "acme-hospital",
  "config": {
    "billingCodes": "ICD-10",
    "insuranceIntegration": true,
    "defaultCurrency": "USD",
    "fiscalYearStart": "01-01"
  }
}
```

## Extension Points

| Extension | Mechanism |
|-----------|-----------|
| Custom fields | Entity metadata + JSONB columns |
| Workflows | Workflow engine hooks per module |
| Reports | Reporting module templates |
| UI layouts | Admin portal widget registry |
| API webhooks | Event bus outbound connectors |
| AI prompts | AI module prompt templates per tenant |

## Anti-Patterns (Forbidden)

- ❌ Copying finance module for Islamic banking → use `finance.islamic-products` extension
- ❌ Separate database per industry → use tenant-scoped schemas
- ❌ Hardcoded industry logic in platform core → use industry packs
- ❌ Direct service-to-service HTTP calls → use integration events
- ❌ Shared mutable state between modules → use events + read models
- ❌ Monolithic modules (multiple unrelated capabilities in one context) → split per [MODULE_STRUCTURE_STANDARD.md](MODULE_STRUCTURE_STANDARD.md)
