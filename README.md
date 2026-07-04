# Marpich ERP

**Enterprise Operating System** — one modular platform for every industry.

Marpich is not a simple ERP. It is a next-generation AI-powered Enterprise Digital Platform designed to compete with SAP S/4HANA, Oracle ERP Cloud, Microsoft Dynamics 365, Salesforce, ServiceNow, Odoo Enterprise, and Zoho Enterprise.

## Architecture Principles

| Principle | Implementation |
|-----------|----------------|
| Enterprise First | Multi-tenant, audit trails, compliance frameworks |
| AI First | Dedicated AI layer with domain-specific models |
| Cloud Native | Containerized services, horizontal scaling |
| API First | REST + GraphQL, OpenAPI contracts |
| Security First | Zero-trust, RBAC/ABAC, encryption at rest/transit |
| Event Driven | Kafka event bus, outbox pattern, CQRS |
| Domain Driven Design | Bounded contexts, aggregates, ubiquitous language |
| Clean Architecture | Domain → Application → Infrastructure → Presentation |
| Hexagonal Architecture | Ports & adapters for all external integrations |

## Repository Structure

```
Marpich ERP/
├── backend/                 # FastAPI + Python (Clean Architecture)
│   ├── core/                # Platform kernel
│   ├── shared/              # Cross-cutting primitives
│   └── modules/             # 62 bounded-context modules
├── frontend/                # Next.js + React + TypeScript
│   ├── core/
│   ├── shared/
│   ├── modules/             # Mirrors backend modules
│   └── apps/                # admin_portal, industry_portal, pos, mobile_shell
├── infrastructure/          # Docker, Terraform, Kubernetes
├── docs/                    # Architecture, ADRs, FOLDER_STRUCTURE.md
├── services/                # Legacy TypeScript services (migration path)
└── packages/                # Legacy shared packages (migration path)
```

Full tree: [docs/FOLDER_STRUCTURE.md](docs/FOLDER_STRUCTURE.md)

## Industry Packs

**Unlimited industries — one Core Platform.** Full catalog: [docs/architecture/INDUSTRY_CATALOG.md](docs/architecture/INDUSTRY_CATALOG.md)

Current domains include Education, University, School, Healthcare, Hospital, Clinic, Laboratory, Pharmacy, Banking, Islamic Banking, Currency Exchange, Accounting, Tax Management, Government, Municipality, NGO, Construction, Engineering, Real Estate, Property Management, Manufacturing, Warehouse, Inventory, Logistics, Transportation, Retail, POS, Hotel, Restaurant, Professional Services — and more via new packs.

Machine-readable: `backend/shared/contracts/industry_packs.json` · legacy TS: `packages/shared-kernel/src/contracts/industry-packs.ts`

## Quick Start

```bash
# Prerequisites: Node 22+, pnpm 9+, Docker
cp .env.example .env
pnpm install
pnpm docker:up          # PostgreSQL, Redis, Kafka
pnpm build
pnpm dev
```

## Services

| Service | Port | Responsibility |
|---------|------|----------------|
| API Gateway | 4000 | Routing, auth, rate limiting, tenant resolution |
| Identity Service | 4001 | Users, roles, permissions, JWT, MFA |
| Tenant Service | 4002 | Tenant provisioning, industry pack activation |
| Module Registry | 4003 | Module discovery, activation, dependency resolution |

## Documentation

- **[Bounded Contexts Registry](docs/architecture/BOUNDED_CONTEXTS_REGISTRY.md)** — 44 independent domains
- **[DDD Domain Architecture](docs/architecture/DDD_DOMAIN_ARCHITECTURE.md)** — Core / Supporting / Generic; full DDD isolation
- **[Chief Architect Mandate](docs/architecture/CHIEF_ARCHITECT_MANDATE.md)** — design systems before code; capabilities not CRUD
- **[Platform Charter](docs/architecture/PLATFORM_CHARTER.md)** — canonical product law (one platform, never duplicate Core)
- **[Long-Horizon Architecture](docs/architecture/LONG_HORIZON_ARCHITECTURE.md)** — think 10 years, 1M users; never sacrifice architecture for speed
- **[Industry Catalog](docs/architecture/INDUSTRY_CATALOG.md)** — unlimited industries, current domains, one Core
- **[Security Standard](docs/architecture/SECURITY_STANDARD.md)** — authn, authz, audit, encryption; never optional
- **[Performance Standard](docs/architecture/PERFORMANCE_STANDARD.md)** — always optimize; pagination, caching, async, indexes
- **[AI Platform Standard](docs/architecture/AI_PLATFORM_STANDARD.md)** — AI is Core; every module exposes 14 surfaces
- **[UI Page Standard](docs/architecture/UI_PAGE_STANDARD.md)** — every page: shell widgets + content patterns (23 items)
- **[Module Architecture](docs/architecture/MODULE_ARCHITECTURE.md)** — identical folder tree in every module (never violate consistency)
- **[Architecture Validation](docs/architecture/ARCHITECTURE_VALIDATION.md)** — pre-code Enterprise Grade gate (15 dimensions; stop if below threshold)
- **[Dependency Graph](docs/architecture/DEPENDENCY_GRAPH.md)** — layer DAG, Core vs business imports, automatic detection
- **[Module Structure Standard](docs/architecture/MODULE_STRUCTURE_STANDARD.md)** — one capability per module, required layers & integrations
- **[Development Protocol](docs/architecture/DEVELOPMENT_PROTOCOL.md)** — analyze & reuse before writing code
- **[Engineering Quality Standard](docs/architecture/ENGINEERING_QUALITY_STANDARD.md)** — mandatory code qualities + feature checklist
- [Shared Kernel](docs/architecture/SHARED_KERNEL.md) — reusable primitives; no business logic in `shared/`
- [Strict Service Boundaries](docs/architecture/SERVICE_BOUNDARIES.md) — nine ownership dimensions; no shared state
- [Business Capabilities Registry](docs/architecture/BUSINESS_CAPABILITIES_REGISTRY.md) — 73 capabilities; identify before modules
- [Core Platform Design](docs/architecture/CORE_PLATFORM_DESIGN.md) — 29 enterprise capabilities, no business logic
- [Core Platform Architecture](docs/architecture/CORE_PLATFORM.md) — per-service REST APIs and events
- [Core Platform Events](docs/architecture/CORE_PLATFORM_EVENTS.md)
- [DDD Architecture](docs/architecture/DDD_ARCHITECTURE.md)
- [Bounded Contexts (37)](docs/architecture/BOUNDED_CONTEXTS.md)
- [Context Map](docs/architecture/CONTEXT_MAP.md)
- [Domain Events Catalog](docs/architecture/DOMAIN_EVENTS_CATALOG.md)
- [Architecture Overview](docs/architecture/OVERVIEW.md)
- [Folder Structure](docs/FOLDER_STRUCTURE.md)
- [ADR Index](docs/adr/README.md)

## License

Proprietary — Marpich ERP Platform
