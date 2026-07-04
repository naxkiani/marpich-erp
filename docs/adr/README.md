# Architecture Decision Records

| ADR | Title | Status |
|-----|-------|--------|
| [001](001-monorepo-turborepo.md) | Monorepo with Turborepo + pnpm | Accepted |
| [002](002-nestjs-microservices.md) | NestJS for backend services | Accepted |
| [003](003-postgresql-multi-tenant.md) | PostgreSQL with hybrid multi-tenancy | Accepted |
| [004](004-kafka-event-bus.md) | Kafka for event-driven integration | Accepted |
| [005](005-module-composition.md) | Module composition over separate systems | Accepted |
| [008](008-bounded-context-isolation.md) | Strict bounded context isolation via events | Accepted |
| [009](009-core-platform-services.md) | Core Platform — 19 reusable services (REST + events) | Accepted |
| [010](010-event-fabric.md) | Event fabric — outbox, idempotency, dispatcher | Accepted |
| [011](011-contract-tests.md) | Contract-first integration events | Accepted |
| [012](012-search-and-gateway.md) | Search service and platform gateway | Accepted |
| [013](013-opentelemetry.md) | OpenTelemetry observability | Accepted |
| [014](014-platform-charter.md) | Platform Charter — one platform, never duplicate Core | Accepted |
| [015](015-engineering-quality-standard.md) | Engineering Quality Standard — mandatory feature checklist | Accepted |
| [016](016-development-protocol.md) | Development Protocol — analyze and reuse before code | Accepted |
| [017](017-module-structure-standard.md) | Module Structure Standard — layers and integrations | Accepted |
| [018](018-ui-page-standard.md) | UI Page Standard — shell and page checklist | Accepted |
| [019](019-ai-platform-standard.md) | AI Platform Standard — 14 surfaces per module | Accepted |
| [020](020-performance-standard.md) | Performance Standard — always optimize | Accepted |
| [021](021-security-standard.md) | Security Standard — mandatory authn/authz/audit | Accepted |
| [022](022-industry-catalog.md) | Industry Catalog — unlimited industries, one Core | Accepted |
| [023](023-long-horizon-architecture.md) | Long-Horizon Architecture — decade-scale mindset | Accepted |
| [024](024-chief-architect-mandate.md) | Chief Enterprise Architect — design before code | Accepted |
| [025](025-ddd-domain-architecture.md) | DDD Domain Architecture — isolation & ownership | Accepted |
| [026](026-bounded-contexts-registry.md) | Bounded Contexts Registry — 44 independent domains | Accepted |
| [027](027-core-platform-design.md) | Core Platform Design — 29 capabilities, no business logic | Accepted |
| [028](028-business-capabilities-registry.md) | Business Capabilities Registry — identify before modules | Accepted |
| [029](029-strict-service-boundaries.md) | Strict Service Boundaries — nine ownership dimensions | Accepted |
| [030](030-shared-kernel.md) | Shared Kernel — reusable primitives, no business logic | Accepted |
| [031](031-module-architecture-consistency.md) | Module Architecture — identical folder tree per module | Accepted |
| [032](032-dependency-graph.md) | Dependency Graph — layer law + automatic violation detection | Accepted |
| [033](033-architecture-validation-gate.md) | Architecture Validation — pre-code Enterprise Grade gate | Accepted |
| [034](034-communication-architecture.md) | Communication architecture — five channels, eight requirements | Accepted |
| [035](035-api-gateway.md) | Enterprise API Gateway — single entry point | Accepted |
| [036](036-integration-platform.md) | Integration Platform — sole external bridge | Accepted |
| [037](037-enterprise-event-bus.md) | Enterprise Event Bus — immutable envelopes, retry | Accepted |
| [038](038-enterprise-workflow-engine.md) | Enterprise Workflow Engine — visual designer + runtime | Accepted |
| [039](039-notification-platform.md) | Enterprise Notification Platform — omnichannel queue | Accepted |
| [040](040-search-engine.md) | Enterprise Search Engine — security-first discovery | Accepted |
| [041](041-document-exchange.md) | Enterprise Document Exchange — lifecycle + exchange | Accepted |
| [042](042-audit-platform.md) | Enterprise Audit Platform — immutable audit every operation | Accepted |
| [043](043-observability-platform.md) | Enterprise Observability Platform — unified telemetry | Accepted |
| [044](044-policy-engine.md) | Enterprise Policy Engine — configurable business rules | Accepted |
| [045](045-compliance-framework.md) | Enterprise Compliance Framework — violations, reports, alerts | Accepted |
| [046](046-feature-flag-system.md) | Enterprise Feature Flag System — multi-scope rollout, A/B, kill switch | Accepted |
| [047](047-plugin-platform.md) | Enterprise Plugin Platform — marketplace, SDK, sandbox runtime | Accepted |
| [048](048-pre-implementation-validation-dimensions.md) | Pre-implementation validation — 15 dimensions realignment | Accepted |
| [049](049-financial-kernel.md) | Enterprise Financial Kernel — platform financial foundation | Accepted |
| [050](050-enterprise-general-ledger.md) | Enterprise General Ledger — immutable, reversal-only | Accepted |
| [006](006-cqrs-read-models.md) | CQRS with async read model projections | Accepted |
| [007](007-ai-as-modules.md) | AI capabilities as first-class modules | Accepted |

## Format

Each ADR follows: Context → Decision → Consequences → Alternatives Considered
