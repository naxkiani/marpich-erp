# ADR-035: Enterprise API Gateway — Single Entry Point

## Status

Accepted

## Context

Marpich exposes 29+ Core Platform services and 40+ business modules via REST and WebSocket. Clients must not call module backends directly. ADR-012 introduced `PlatformGatewayMiddleware` for request ID and access logging, but enterprise requirements demand a unified gateway owning authentication, authorization, OIDC/OAuth2, rate limiting, versioning, load balancing, caching, compression, validation, transformation, observability, tenant resolution, localization, documentation, and feature flags — with **invalid requests rejected before modules**.

Product and security leadership mandated a canonical **Enterprise API Gateway** design before expanding edge middleware implementation.

## Decision

Adopt **`docs/architecture/API_GATEWAY_ARCHITECTURE.md`** as the single entry point law.

### Single entry point

All external HTTP/WebSocket traffic enters through the API Gateway. Modules are internal upstreams.

### Ordered filter chain (fail fast)

TLS → request ID/trace → method/size/CORS → rate limit → API version → authentication → tenant resolution → authorization → feature flags → request validation → cache → route/LB → upstream → response transform → compression → log/metrics/trace.

Termination at any stage returns `4xx`/`5xx` without invoking module handlers.

### Twenty responsibilities

Authentication, Authorization, JWT Validation, OpenID Connect, OAuth2, Rate Limiting, API Versioning, Load Balancing, Caching, Compression, Request Validation, Response Transformation, Logging, Monitoring, Metrics, Distributed Tracing, WebSocket Routing, Tenant Resolution, Localization, API Documentation, Feature Flags.

### Routing

Declarative `route_registry.yaml` driven by `contexts/registry.py` and `context.yaml`. Prefix-based match with auth/tenant/module/permission metadata.

### Deployment tiers

| Tier | Implementation |
|------|----------------|
| Dev/SMB | `PlatformGatewayMiddleware` + FastAPI composition root |
| Growth | Edge proxy + service groups |
| Enterprise | `services/api-gateway/` (+ optional Kong/Envoy) |

Contracts (paths, headers, envelopes) are identical across tiers.

## Consequences

- Gateway filter chain implementation is incremental; modules keep `require_permissions` as defense-in-depth
- `route_registry.yaml` becomes required for new public routes
- OIDC/OAuth2 gateway termination follows SECURITY_STANDARD contracts
- NestJS gateway extended to match Python registry over time

## Alternatives considered

- Per-module auth only — fails zero-trust; rejected
- Service mesh without edge gateway — insufficient for B2B docs, rate limits, and public OpenAPI
- Direct module ports in production — rejected
