# Marpich Performance Standard

**Status:** Canonical — **always optimize**; mandatory for all code  
**Audience:** Engineering, AI agents, reviewers  
**Companions:** [ENGINEERING_QUALITY_STANDARD.md](ENGINEERING_QUALITY_STANDARD.md) · [DEVELOPMENT_PROTOCOL.md](DEVELOPMENT_PROTOCOL.md) · [ENTERPRISE_OBSERVABILITY_PLATFORM.md](ENTERPRISE_OBSERVABILITY_PLATFORM.md)

**Rule: Always optimize. Never load unnecessary data.**

---

## Platform Law

Performance is not a post-launch task. Every API, query, page, and event handler must apply the rules below **by default**.

| # | Rule | Backend | Frontend |
|---|------|---------|----------|
| 1 | **Always optimize** | Measure before merge; set budgets (p95 latency, query count) | Lighthouse / bundle size checks |
| 2 | **Avoid N+1 queries** | `selectinload` / `joinedload`; batch fetches; no ORM in loops | Batch API calls; no per-row fetch in tables |
| 3 | **Use pagination** | `limit` + `cursor` or `offset`; max page size enforced | `DataTable` server-side paging |
| 4 | **Use lazy loading** | Load relations on demand; split heavy endpoints | `dynamic()` / route-level code split |
| 5 | **Use caching** | TTL caches; ETag; HTTP `Cache-Control` on reads | SWR/React Query; stale-while-revalidate |
| 6 | **Use Redis** | Sessions, hot reads, rate limits, distributed locks | — (server-side) |
| 7 | **Use async APIs** | `async def` handlers; `asyncpg`; non-blocking I/O | Async fetch; debounced search |
| 8 | **Use background workers** | Outbox dispatcher; async jobs for heavy work | Optimistic UI + job status polling |
| 9 | **Optimize database indexes** | Index `(tenant_id, …)`; composite for filters; review EXPLAIN | — |
| 10 | **Optimize images** | Media service variants; WebP/AVIF; CDN URLs | `next/image`; responsive `srcset` |
| 11 | **Compress responses** | gzip/brotli at gateway; minimize JSON payloads | Tree-shaking; minify bundles |
| 12 | **Use streaming where appropriate** | SSE / chunked for large exports, AI tokens | Stream download; incremental render |
| 13 | **Never load unnecessary data** | DTO projection; no `SELECT *`; field masks on API | Fetch only visible columns; virtualize long lists |

---

## Backend Patterns (FastAPI / PostgreSQL)

### Pagination (required on all list endpoints)

```python
# Query params: ?limit=50&cursor=...  (max limit=100)
async def list_items(tenant_id: str, limit: int = 50, cursor: str | None = None): ...
```

### Avoid N+1

```python
# ✅ eager load in repository
stmt = select(Row).options(selectinload(Row.related)).where(Row.tenant_id == tenant_id)

# ❌ forbidden — query inside loop
for row in rows:
    related = await session.get(RelatedRow, row.related_id)
```

### Async + background

| Work type | Pattern |
|-----------|---------|
| HTTP request | `async def` route → application service |
| Event publish | Outbox in same transaction → `OutboxDispatcher` |
| Heavy job (export, AI, report) | `POST` returns job id → worker processes |
| Retry | Idempotent consumers + outbox redelivery |

### Redis (`settings` + infrastructure)

| Use case | Key pattern |
|----------|-------------|
| Cache | `cache:{tenant_id}:{resource}:{id}` |
| Rate limit | `ratelimit:{tenant_id}:{user_id}` |
| Session | Platform identity service |

### Database indexes (every new table)

```sql
-- Required minimum
CREATE INDEX idx_{table}_tenant ON {schema}.{table} (tenant_id);

-- Add composite indexes for filter/sort columns used in list APIs
CREATE INDEX idx_{table}_tenant_created ON {schema}.{table} (tenant_id, created_at DESC);
```

Document indexes in migration file comments. Run `EXPLAIN ANALYZE` for hot queries in PR notes.

### Response size

- Return summary DTOs on lists; detail DTOs on `GET /{id}`
- Omit null fields when `?fields=` sparse fieldsets used
- Enable compression at reverse proxy / uvicorn gzip

### Streaming

- Large CSV/PDF exports → job + download URL or chunked stream
- AI inference tokens → SSE from `/api/v1/ai` when supported

---

## Frontend Patterns (Next.js / React)

| Rule | Implementation |
|------|----------------|
| Lazy loading | `next/dynamic` for heavy charts, editors, AI panels |
| Pagination | Server-driven `DataTable`; never fetch 10k rows |
| Caching | React Query / SWR with `tenantId` in query keys |
| Images | `next/image` with width/height; lazy below fold |
| Virtualization | Long lists → virtual scroll (when > ~100 rows) |
| Bundle | Import shared components from `@marpich/shared`; analyze bundle on PR |

---

## PR Performance Checklist

```markdown
## Performance (required)

- [ ] Always optimize — budgets noted (p95 / query count / bundle)
- [ ] No N+1 queries (ORM or API)
- [ ] Pagination on list endpoints / tables
- [ ] Lazy loading for heavy UI / relations
- [ ] Caching strategy documented (Redis / HTTP / client)
- [ ] Redis used for hot paths where applicable
- [ ] Async APIs / non-blocking I/O
- [ ] Background workers for heavy work
- [ ] DB indexes on tenant_id + filter columns
- [ ] Images optimized (variants / next/image)
- [ ] Responses compressed / payload minimized
- [ ] Streaming used if large or AI output
- [ ] No unnecessary fields loaded
```

---

## Anti-Patterns (forbidden)

- Unbounded `GET /items` without pagination
- Loading full aggregates for list views
- Synchronous blocking calls in `async def` routes
- Missing `tenant_id` index on new tables
- Fetching all notifications/messages on every page load
- Embedding multi-MB JSON blobs in list responses

---

## Enforcement

| Mechanism | Location |
|-----------|----------|
| Cursor rule | `.cursor/rules/marpich-performance.mdc` |
| Engineering quality | [ENGINEERING_QUALITY_STANDARD.md](ENGINEERING_QUALITY_STANDARD.md) |
| Outbox / workers | `shared/infrastructure/messaging/` |
| Observability | `shared/infrastructure/observability/telemetry.py` |

**Review rejection:** PRs with unbounded queries, obvious N+1, or missing pagination on new list APIs are incomplete.
