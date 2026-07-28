# AI Platform API

Prefix: `/api/v1/ai`

| Surface | Method | Permission |
|---|---|---|
| Assist | `POST /assist` | `ai.assist.infer` |
| Foundation | `GET /foundation*` | `ai.assist.read` |
| Mission / vision / scope | `GET /mission*` | `ai.assist.read` |
| Domain architecture (DDD) | `GET /domain*` | `ai.assist.read` |
| MLOps | `GET /mlops*` | `ai.assist.read` |

See ADR-421–424.
