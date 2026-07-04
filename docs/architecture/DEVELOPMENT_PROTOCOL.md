# Marpich Development Protocol

**Status:** Canonical — mandatory **before** writing any code  
**Audience:** Engineering, AI agents, reviewers  
**Role:** [Chief Enterprise Architect](CHIEF_ARCHITECT_MANDATE.md) — design systems before code  
**Companions:** [PLATFORM_CHARTER.md](PLATFORM_CHARTER.md) · [ENGINEERING_QUALITY_STANDARD.md](ENGINEERING_QUALITY_STANDARD.md) · [LONG_HORIZON_ARCHITECTURE.md](LONG_HORIZON_ARCHITECTURE.md)

**No code until this protocol is complete. Think ten years — not just today's ticket.**

---

## Step 0 — Before Writing Code

**Architecture validation gate:** [ARCHITECTURE_VALIDATION.md](ARCHITECTURE_VALIDATION.md) — validate **fifteen dimensions** (Architecture, DDD, Security, Scalability, Performance, Testing, AI Integration, Documentation, Accessibility, Localization, Observability, Workflow, Audit, Policy Compliance, Plugin Compatibility). **If any validation fails — STOP. Recommend architectural improvements. Only then generate production code.**

```bash
python3 scripts/validate-architecture.py
python3 scripts/check-dependency-graph.py
```

| Order | Action | Required output |
|-------|--------|-----------------|
| 0 | **Validate architecture** | Hard gates PASS + scorecard ≥ Enterprise Grade ([ARCHITECTURE_VALIDATION.md](ARCHITECTURE_VALIDATION.md)) |
| 1 | **Architect the capability** | Architecture brief — capability, domain, events ([CHIEF_ARCHITECT_MANDATE.md](CHIEF_ARCHITECT_MANDATE.md)) |
| 2 | **Analyze the entire system** | Brief note: which bounded contexts, events, and APIs are involved |
| 3 | **Find existing services** | List services/contexts that already solve part of the problem |
| 4 | **Decide reuse vs extend** | Explicit reuse plan — or ADR if extending Core |
| 5 | **Assess architecture strength** | If existing pattern is weak, **improve it first** — do not layer hacks on top |
| 6 | **Explain architectural decisions** | Document *why* before implementing *what* |
| 7 | **Long-horizon check** | 1M users, 10K orgs, AI evolution, extensibility — see [LONG_HORIZON_ARCHITECTURE.md](LONG_HORIZON_ARCHITECTURE.md) |

---

## Discovery Map — Where to Look First

### Backend services (bounded contexts)

```
backend/contexts/{context}/
├── domain/           # Aggregates, domain events — reuse models here
├── application/      # Use cases — reuse service patterns
├── infrastructure/   # Postgres/memory stores — reuse persistence adapters
├── presentation/     # FastAPI routers — reuse API prefixes
├── container.py      # DI wiring — follow existing container pattern
└── tests/            # Flow tests — mirror for new features
```

**Registry of all contexts:** `backend/contexts/registry.py`  
**Mounted routers:** `backend/core/presentation/api/main.py`  
**Industry modules catalog:** `backend/shared/contracts/industry_packs.json`

### Platform / shared infrastructure (reuse, never duplicate)

| Concern | Location |
|---------|----------|
| Settings / env | `backend/shared/infrastructure/settings.py` |
| Database ORM rows | `backend/shared/infrastructure/database/orm.py` |
| Event bus / outbox | `backend/shared/infrastructure/messaging/` |
| OpenTelemetry | `backend/shared/infrastructure/observability/telemetry.py` |
| Gateway middleware | `backend/core/presentation/middleware/platform_gateway.py` |
| Gateway route registry | `backend/core/gateway/route_registry.yaml` |
| Gateway architecture | [API_GATEWAY_ARCHITECTURE.md](API_GATEWAY_ARCHITECTURE.md) |
| Integration Platform | [INTEGRATION_PLATFORM.md](INTEGRATION_PLATFORM.md) |
| Workflow architecture | [ENTERPRISE_WORKFLOW_ENGINE.md](ENTERPRISE_WORKFLOW_ENGINE.md) |
| Notification Platform | [ENTERPRISE_NOTIFICATION_PLATFORM.md](ENTERPRISE_NOTIFICATION_PLATFORM.md) |
| Search Engine | [ENTERPRISE_SEARCH_ENGINE.md](ENTERPRISE_SEARCH_ENGINE.md) |
| Document Exchange | [ENTERPRISE_DOCUMENT_EXCHANGE.md](ENTERPRISE_DOCUMENT_EXCHANGE.md) |
| Audit Platform | [ENTERPRISE_AUDIT_PLATFORM.md](ENTERPRISE_AUDIT_PLATFORM.md) |
| Observability Platform | [ENTERPRISE_OBSERVABILITY_PLATFORM.md](ENTERPRISE_OBSERVABILITY_PLATFORM.md) |
| Policy Engine | [ENTERPRISE_POLICY_ENGINE.md](ENTERPRISE_POLICY_ENGINE.md) |
| Compliance Framework | [ENTERPRISE_COMPLIANCE_FRAMEWORK.md](ENTERPRISE_COMPLIANCE_FRAMEWORK.md) |
| Feature Flag System | [ENTERPRISE_FEATURE_FLAG_SYSTEM.md](ENTERPRISE_FEATURE_FLAG_SYSTEM.md) |
| Plugin Platform | [ENTERPRISE_PLUGIN_PLATFORM.md](ENTERPRISE_PLUGIN_PLATFORM.md) |
| Financial Kernel | [ENTERPRISE_FINANCIAL_KERNEL.md](ENTERPRISE_FINANCIAL_KERNEL.md) |
| Integration event base | `backend/shared/domain/events/` |
| Event JSON schemas | `docs/architecture/events/` |
| Contract validation | `backend/shared/contracts/` |

### Documentation (read before coding)

| Doc | Purpose |
|-----|---------|
| [BOUNDED_CONTEXTS.md](BOUNDED_CONTEXTS.md) | Context boundaries and responsibilities |
| [CONTEXT_MAP.md](CONTEXT_MAP.md) | Relationships between contexts |
| [DOMAIN_EVENTS_CATALOG.md](DOMAIN_EVENTS_CATALOG.md) | Published/subscribed events |
| [CORE_PLATFORM.md](CORE_PLATFORM.md) | Platform service APIs |
| [MODULE_SYSTEM.md](MODULE_SYSTEM.md) | Module manifests and activation |
| [MODULE_ARCHITECTURE.md](MODULE_ARCHITECTURE.md) | Identical layer tree — copy `backend/contexts/_template/` |
| [ARCHITECTURE_VALIDATION.md](ARCHITECTURE_VALIDATION.md) | Pre-code validation — Enterprise Grade gate |
| [docs/adr/](../adr/README.md) | Past architectural decisions |

### Frontend (when UI is involved)

```
frontend/
├── core/             # Shell, auth, layout — reuse
├── shared/           # Design system components — reuse
└── modules/          # Industry UI — extend, don't fork core widgets
```

---

## Reuse Checklist — Mandatory

Before creating anything new, confirm each row:

| Asset | Search first | Reuse via |
|-------|--------------|-----------|
| **Services** | `contexts/registry.py`, `grep` use cases | Call application service or subscribe to events |
| **APIs** | OpenAPI `/api/docs`, `presentation/router.py` | Extend existing router; same prefix conventions |
| **Components** | `frontend/shared/`, `frontend/core/` | Import existing; extend with props/slots |
| **Models** | `domain/aggregates/`, `orm.py` | Extend aggregate or add module-specific table |
| **Permissions** | Permission catalog, router decorators | Register `module.resource.action` at activation |
| **Events** | `DOMAIN_EVENTS_CATALOG.md`, `docs/architecture/events/` | Subscribe or publish existing envelope versions |
| **Logic** | Application layer in peer contexts | Extract to Core only if cross-industry |

**Never create duplicate logic.** If two places need the same behavior → one implementation in Core or one shared module.

---

## When Existing Architecture Is Weak

Do **not** generate feature code on a broken foundation.

| Weak signal | Improve first |
|-------------|---------------|
| Duplicate audit/notification/auth in a context | Refactor to Core services |
| Cross-context domain import | Replace with integration event + ACL |
| Missing contract schema for events | Add JSON schema + contract test |
| No `tenant_id` on tables/events | Fix data model before new features |
| Untested critical path | Add integration test before extending |
| Inconsistent API envelope | Align router with platform standard |

Improvement may be a small refactor PR or an ADR — but it precedes the feature.

---

## Architectural Decision Explanation (required)

Every non-trivial change must state:

```markdown
## Architectural decisions

### Context
What problem are we solving? Which existing services were considered?

### Reuse
- Services reused: …
- APIs reused: …
- Events reused: …
- Components/models reused: …

### Decisions
1. **Decision:** …  
   **Why:** …  
   **Alternatives rejected:** …

### Impact
- Bounded contexts touched: …
- New events/APIs (if any): …
- Permissions registered: …
```

For agents: include this in the response **before** or **with** the implementation — not after the fact.

---

## Agent / Developer Workflow (summary)

```
1. VALIDATE → hard gates + score 15 dimensions ([ARCHITECTURE_VALIDATION.md](ARCHITECTURE_VALIDATION.md)) — STOP if any fails
2. READ  → registry, context map, related routers, event catalog
3. SEARCH → grep for similar aggregates, handlers, permissions
4. REUSE  → extend existing service/API/event/component
5. FIX    → if pattern is weak, refactor or propose improvement first
6. EXPLAIN → document decisions (ADR for significant choices)
7. CODE   → only when ENTERPRISE_GRADE — satisfy Platform Charter + Engineering Quality Standard
8. TEST   → unit + integration + contract tests
9. REVIEW → long-horizon checklist — architecture better than before
```

**Mindset:** [LONG_HORIZON_ARCHITECTURE.md](LONG_HORIZON_ARCHITECTURE.md) — never sacrifice architecture for speed.

---

## Enforcement

| Mechanism | Location |
|-----------|----------|
| Cursor agent rule | `.cursor/rules/marpich-development-protocol.mdc` |
| Long-horizon rule | `.cursor/rules/marpich-long-horizon.mdc` |
| Long-horizon architecture | [LONG_HORIZON_ARCHITECTURE.md](LONG_HORIZON_ARCHITECTURE.md) |
| Platform charter | [PLATFORM_CHARTER.md](PLATFORM_CHARTER.md) |
| Engineering standard | [ENGINEERING_QUALITY_STANDARD.md](ENGINEERING_QUALITY_STANDARD.md) |

**Review rejection:** PRs that add new services/APIs/events without a reuse analysis and decision explanation are incomplete.
