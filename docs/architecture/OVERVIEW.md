# Marpich ERP — Architecture Overview

> **Canonical product law:** [PLATFORM_CHARTER.md](PLATFORM_CHARTER.md)  
> **Before coding:** [DEVELOPMENT_PROTOCOL.md](DEVELOPMENT_PROTOCOL.md)  
> **Mandatory code standard:** [ENGINEERING_QUALITY_STANDARD.md](ENGINEERING_QUALITY_STANDARD.md)

## Vision

Marpich ERP is an **Enterprise Operating System (EOS)** — a single composable platform that serves multiple industries through configuration, not duplication.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Presentation Layer                                │
│  Admin Portal │ Industry Portals │ Mobile │ POS │ Kiosk │ API Clients  │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   │
┌──────────────────────────────────▼──────────────────────────────────────┐
│                         API Gateway (BFF)                               │
│  Tenant Resolution │ Auth │ Rate Limit │ Routing │ GraphQL Federation   │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
┌───────▼───────┐        ┌────────▼────────┐       ┌────────▼────────┐
│   Platform    │        │  Domain Modules │       │    AI Layer     │
│   Services    │        │  (Composable)   │       │                 │
│ Identity      │        │ Finance │ HR    │       │ Insights        │
│ Tenant        │        │ Healthcare    │       │ Fraud Detection │
│ Module Reg    │        │ Education     │       │ Clinical Assist │
│ Workflow      │        │ Logistics     │       │ Document Intel  │
│ Documents     │        │ Retail │ ...  │       │ Credit Scoring  │
└───────┬───────┘        └────────┬────────┘       └────────┬────────┘
        │                          │                          │
        └──────────────────────────┼──────────────────────────┘
                                   │
┌──────────────────────────────────▼──────────────────────────────────────┐
│                      Event Bus (Kafka)                                  │
│  Domain Events │ Integration Events │ Saga Orchestration │ Outbox        │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   │
┌──────────────────────────────────▼──────────────────────────────────────┐
│                      Data Layer                                         │
│  PostgreSQL (tenant-scoped) │ Redis (cache/sessions) │ S3 (documents)   │
└─────────────────────────────────────────────────────────────────────────┘
```

## Bounded Contexts

Each bounded context is a deployable service with its own database schema (per tenant or shared with row-level security).

### Platform Layer (always active)

| Context | Aggregate Roots | Key Events |
|---------|----------------|------------|
| Identity | User, Role, Permission, Session | UserCreated, RoleAssigned |
| Tenant | Tenant, Subscription, IndustryPack | TenantProvisioned, ModuleActivated |
| Module Registry | Module, ModuleVersion, Activation | ModuleRegistered, ModuleEnabled |
| Workflow | ProcessDefinition, ProcessInstance | ProcessStarted, TaskCompleted |
| Documents | Document, Folder, Version | DocumentUploaded, DocumentSigned |

### Domain Layer (activated per industry pack)

| Context | Industries | Shared With |
|---------|-----------|-------------|
| Finance | All | Accounting, Banking, Tax, Retail |
| HR | All | Universities, Government, Construction |
| Healthcare | Hospital, Clinic, Lab, Pharmacy | Patient, Clinical, Billing |
| Education | University, School | Student, Academics, Grading |
| Logistics | Logistics, Warehouse, Manufacturing | Inventory, Fleet, WMS |
| Retail | Retail, POS, Pharmacy, Restaurant | Catalog, POS, Payments |
| Real Estate | Real Estate, Property Mgmt | Listings, Leases, Maintenance |
| Construction | Construction, Engineering | Projects, BOQ, Subcontractors |
| Government | Government, NGO | Citizen Services, Procurement, Grants |

## Clean Architecture Layers (per service)

```
service/
├── domain/           # Entities, aggregates, value objects, domain events
├── application/      # Use cases, commands, queries, handlers (CQRS)
├── infrastructure/   # Repositories, ORM, message brokers, external APIs
└── presentation/     # Controllers, GraphQL resolvers, DTOs
```

**Dependency rule:** Domain has zero external dependencies. Application depends on domain. Infrastructure implements ports defined in application. Presentation depends on application.

## CQRS Pattern

- **Commands** mutate state, emit domain events, use write repositories
- **Queries** read from optimized read models (projections)
- **Event handlers** update read models asynchronously
- **Sagas** coordinate cross-context workflows via integration events

## Multi-Tenancy Strategy

| Strategy | Use Case | Implementation |
|----------|----------|----------------|
| Schema-per-tenant | Enterprise clients, regulatory isolation | PostgreSQL schema `tenant_{id}` |
| Row-level (shared schema) | SMB, high tenant count | `tenant_id` column + RLS policies |
| Hybrid | Mixed deployment | Configurable per tenant tier |

Tenant resolution: subdomain → header (`X-Tenant-ID`) → JWT claim.

## Security Model

- **Authentication:** JWT (access + refresh), MFA, SSO (SAML/OIDC)
- **Authorization:** RBAC + ABAC (attribute-based for industry compliance)
- **Audit:** Immutable audit log per tenant, correlation IDs on all events
- **Encryption:** TLS in transit, AES-256 at rest, field-level encryption for PII/PHI

## Event-Driven Integration

All cross-service communication uses integration events via Kafka:

```typescript
// Example: Tenant provisioned → activate modules → seed data
TenantProvisioned → ModuleActivationRequested → IndustryPackActivated
```

Outbox pattern ensures at-least-once delivery with idempotent consumers.

## AI Layer

AI capabilities are modules, not bolt-ons:

| Capability | Module | Domains |
|------------|--------|---------|
| Business Insights | ai.insights | All |
| Fraud Detection | ai.fraud-detection | Banking, FX, Retail |
| Clinical Assist | ai.clinical-assist | Healthcare |
| Document Intelligence | ai.document-intelligence | Tax, Accounting, Government |
| Credit Scoring | ai.credit-scoring | Microfinance, Banking |
| Route Optimization | ai.route-optimization | Logistics |
| Predictive Maintenance | ai.predictive-maintenance | Manufacturing |

## Deployment Topology

```
                    ┌─────────────┐
                    │   Ingress   │
                    └──────┬──────┘
                           │
              ┌────────────▼────────────┐
              │      API Gateway        │
              └────────────┬────────────┘
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────▼────┐      ┌─────▼─────┐     ┌─────▼─────┐
    │Identity │      │  Tenant   │     │  Domain   │
    │ Service │      │  Service  │     │ Services  │
    └────┬────┘      └─────┬─────┘     └─────┬─────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           │
              ┌────────────▼────────────┐
              │   Kafka Event Bus       │
              └────────────┬────────────┘
         ┌─────────────────┼─────────────────┐
    ┌────▼────┐      ┌─────▼─────┐     ┌─────▼─────┐
    │PostgreSQL│      │   Redis   │     │    S3     │
    └─────────┘      └───────────┘     └───────────┘
```

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Runtime | Node.js 22 LTS |
| Language | TypeScript 5.7 (strict) |
| Framework | NestJS 11 (DI, modules, guards) |
| Monorepo | pnpm workspaces + Turborepo |
| Database | PostgreSQL 16 |
| Cache | Redis 7 |
| Events | Apache Kafka |
| API | REST + GraphQL (Apollo Federation) |
| Frontend | Next.js 15 (App Router) |
| Containers | Docker + Kubernetes |
| IaC | Terraform |
| Observability | OpenTelemetry, Prometheus, Grafana |

## Competitive Positioning

| Capability | SAP | Oracle | Dynamics | Marpich |
|------------|-----|--------|----------|---------|
| Multi-industry | Modules (expensive) | Cloud modules | Industry clouds | Industry packs (config) |
| AI native | SAP Joule (add-on) | Oracle AI | Copilot | AI-first modules |
| Deployment | On-prem + cloud | Cloud | Cloud | Cloud-native + hybrid |
| Customization | ABAP (complex) | Low-code | Power Platform | Module composition |
| Time-to-value | Months-years | Months | Months | Days-weeks |
