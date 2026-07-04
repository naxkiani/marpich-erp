# Marpich Backend (FastAPI / Python)

Modular Clean Architecture — **never monolithic**.

## Layout

```
backend/
├── core/                 # Platform kernel (composition root)
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── presentation/     # FastAPI app, middleware, router registry
├── shared/               # Cross-cutting primitives (tenant, events, audit)
│   ├── domain/
│   ├── application/
│   └── infrastructure/
├── modules/              # Bounded contexts (one folder per capability)
│   ├── platform/         # identity, tenant, gateway, …
│   ├── finance/
│   ├── healthcare/
│   └── …
└── tests/                # Backend-wide integration / e2e
```

## Module contract

Every module under `modules/{namespace}/{capability}/`:

| Layer | Responsibility |
|-------|----------------|
| `domain/` | Aggregates, entities, value objects, domain events |
| `application/` | Use cases, commands, queries, handlers (CQRS) |
| `infrastructure/` | Repositories, ORM, external adapters |
| `presentation/` | FastAPI routers, request/response schemas |
| `tests/` | Unit + integration tests for this module |
| `docs/` | Module API, permissions, events |

## Dependency rule

```
presentation → application → domain
infrastructure → application → domain
```

`core.presentation` composes module routers — modules never import each other directly.

## Run (after implementation)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn core.presentation.api.main:app --reload --port 8000
```
