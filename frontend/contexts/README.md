# Bounded Contexts (Frontend)

Mirrors `backend/contexts/` — one folder per domain.

Each context:
- `domain/` — view models, client types
- `application/` — state, API clients, use cases
- `infrastructure/` — fetch adapters
- `presentation/` — components, pages, hooks
- `tests/` / `docs/`

**Never import** another context's domain layer. Subscribe to backend events via WebSocket/SSE for live updates.
