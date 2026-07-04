# Marpich Engineering Quality Standard

**Status:** Canonical — mandatory for all generated and merged code  
**Audience:** Engineering, AI agents, reviewers  
**Companion:** [PLATFORM_CHARTER.md](PLATFORM_CHARTER.md)  
**Prerequisite:** [DEVELOPMENT_PROTOCOL.md](DEVELOPMENT_PROTOCOL.md) — analyze and reuse **before** writing code  
**Pre-code gate:** [ARCHITECTURE_VALIDATION.md](ARCHITECTURE_VALIDATION.md) — validate fifteen dimensions (Architecture, DDD, Security, Scalability, Performance, Testing, AI Integration, Documentation, Accessibility, Localization, Observability, Workflow, Audit, Policy Compliance, Plugin Compatibility); **stop if any fails**

**Rule: Never skip any item below.**

---

## Part A — Every Generated Code Must Be

| Quality | Definition | Marpich implementation |
|---------|------------|------------------------|
| **Enterprise Grade** | Production-safe defaults, compliance-ready, no demo shortcuts | Multi-tenant isolation, audit, permissions, contract-first APIs |
| **Cloud Native** | Stateless services, 12-factor config, horizontal scale | Env-based settings, container-ready, `0.0.0.0:$PORT`, ephemeral FS → DB/S3 |
| **AI Ready** | Extension points for models, prompts, embeddings | AI Service hooks; module manifests declare `ai.*` capabilities |
| **RESTful** | Resource-oriented HTTP, consistent verbs and status codes | `/api/v1/{context}/…`, OpenAPI, platform error envelope |
| **Scalable** | Async I/O, pagination, no unbounded queries | `async` handlers, cursor/limit pagination, DB indexes on `tenant_id` |
| **Reusable** | Shared primitives; no one-off copies | Core Platform services; extend via events and plugins |
| **Secure** | AuthN/Z on every route, input validation, no secrets in code | JWT + permissions; Pydantic schemas; env secrets only — see [SECURITY_STANDARD.md](SECURITY_STANDARD.md) |
| **Well Documented** | Code + API + architecture docs | OpenAPI tags, context `docs/`, ADRs for decisions |
| **Testable** | Pure domain, injectable ports, deterministic tests | Memory stores for unit tests; contract tests for events/APIs |
| **Maintainable** | DDD layers, bounded contexts, small modules | `domain/` → `application/` → `infrastructure/` → `presentation/` |
| **Observable** | Logs, metrics, traces exportable to ops stack | [ENTERPRISE_OBSERVABILITY_PLATFORM.md](ENTERPRISE_OBSERVABILITY_PLATFORM.md) · OTel · structured logging |

---

## Part B — Every Feature Must Include

No feature is complete until **all** rows are addressed in the PR or task notes.

| Requirement | Backend | Frontend |
|-------------|---------|----------|
| **Logging** | Structured `logging` with `request_id`, `tenant_id`, context name | Client error boundary + console/logger service |
| **Monitoring** | `/api/v1/health`, readiness hooks, System Health Dashboard | Error reporting integration point |
| **Metrics** | OTel meters (`http.server.duration`, domain counters) | Web vitals / client metrics hook |
| **Tracing** | OTel FastAPI instrumentation + span attributes | Propagate `X-Request-ID` / trace headers |
| **Error Handling** | Typed exceptions → HTTP problem envelope; no bare `except` in domain | User-facing error states, toast/alerts |
| **Retry** | Outbox redelivery, idempotent consumers, transient DB retry policy | Exponential backoff on API client |
| **Caching** | Redis or in-memory TTL for hot reads; cache keys include `tenant_id` | SWR/React Query with tenant-scoped keys |
| **Background Processing** | Outbox dispatcher, async event handlers, job queue hooks | Optimistic UI + polling/WebSocket where needed |
| **Audit Trail** | Publish integration events; Audit Service consumption | Display audit history via platform API |
| **Documentation** | OpenAPI operation descriptions, `contexts/{ctx}/docs/` glossary | Component Storybook or inline JSDoc + README |
| **Unit Tests** | `contexts/{context}/tests/` — domain + application logic | Component/unit tests co-located |
| **Integration Tests** | `tests/integration/` — API + event flows | E2E or integration against API mocks |
| **Performance Optimization** | Indexes, `select` limits, N+1 avoidance, async batch | Code split, lazy load, memoization — see [PERFORMANCE_STANDARD.md](PERFORMANCE_STANDARD.md) |
| **Accessibility** | N/A (API: semantic error messages) | WCAG 2.1 AA — labels, focus, keyboard, ARIA |
| **Dark Mode** | N/A | Theme tokens; `prefers-color-scheme` + toggle |
| **RTL** | Locale-aware formatting in API responses | `dir="rtl"`, logical CSS, i18n |
| **LTR** | Default locale paths | `dir="ltr"` default; locale switcher |

See **[UI Page Standard](UI_PAGE_STANDARD.md)** for the full per-page checklist (command palette, global search, tables, forms, export, etc.).

See **[Performance Standard](PERFORMANCE_STANDARD.md)** — always optimize; pagination, caching, async, no N+1.

See **[Security Standard](SECURITY_STANDARD.md)** — authn, authz, audit, encryption; never optional.

---

## Feature Delivery Checklist (copy into PR description)

```markdown
## Engineering quality (required — all must be checked)

### Code qualities
- [ ] Enterprise Grade
- [ ] Cloud Native
- [ ] AI Ready
- [ ] RESTful
- [ ] Scalable
- [ ] Reusable
- [ ] Secure
- [ ] Well Documented
- [ ] Testable
- [ ] Maintainable
- [ ] Observable

### Feature inclusions
- [ ] Logging
- [ ] Monitoring
- [ ] Metrics
- [ ] Tracing
- [ ] Error Handling
- [ ] Retry
- [ ] Caching
- [ ] Background Processing
- [ ] Audit Trail
- [ ] Documentation
- [ ] Unit Tests
- [ ] Integration Tests
- [ ] Performance Optimization
- [ ] Accessibility
- [ ] Dark Mode
- [ ] RTL
- [ ] LTR
```

---

## Implementation Patterns (reference)

### Backend error envelope

```python
# presentation layer maps domain errors → consistent HTTP response
# Never leak stack traces or internal IDs in production responses
```

### Structured log fields

```python
logger.info("event", extra={
    "request_id": request_id,
    "tenant_id": tenant_id,
    "context": "hospital",
    "action": "encounter.completed",
})
```

### OpenTelemetry

- Enable: `OTEL_ENABLED=true` — see `docs/adr/013-opentelemetry.md`
- Gateway records `http.server.duration` and span attributes

### Event + audit path

```
Command → aggregate → domain event → outbox → integration event → audit consumer
```

### Frontend i18n / RTL

- All user strings in locale files — never hardcoded in JSX
- Layout uses logical properties (`margin-inline-start`, not `margin-left`)
- Support `fa-IR`, `ar-SA` (RTL) and `en-US` (LTR) minimum

### Tests minimum per feature

| Layer | Minimum |
|-------|---------|
| Domain / application | 1+ unit test per use case |
| REST API | 1+ integration test per new route |
| Integration event | Contract sample in `docs/architecture/events/` + contract test |

---

## Enforcement

| Mechanism | Location |
|-----------|----------|
| Cursor agent rule | `.cursor/rules/marpich-engineering-quality.mdc` |
| Platform charter | [PLATFORM_CHARTER.md](PLATFORM_CHARTER.md) |
| OpenTelemetry ADR | [../adr/013-opentelemetry.md](../adr/013-opentelemetry.md) |
| Contract tests | `backend/tests/contracts/` |

**Review rejection:** Any PR missing checklist items or skipping observability, tests, audit, or accessibility (for UI) is incomplete.
