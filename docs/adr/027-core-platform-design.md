# ADR-027: Core Platform Design — 29 Enterprise Capabilities

## Status

Accepted

## Context

Marpich must serve unlimited industries through one composable platform. Every business module (hospital, banking, municipality, POS, …) depends on the same reusable enterprise services. Product leadership defined a comprehensive Core Platform scope and a hard rule: **Core Platform must never contain business logic** — only reusable enterprise services.

ADR-009 established 19 logical services. This ADR expands and formalizes the full platform design with 29 capabilities across six planes, including scheduling, workers, secrets, logging, monitoring, caching, gateway, and health.

## Decision

### 1. Core Platform law

- Every business module **depends on** Core Platform.
- Core Platform **never depends on** business modules.
- Core owns **how** (auth, audit, workflow, search); modules own **what** (patients, loans, permits).

### 2. Six platform planes

| Plane | Capabilities |
|-------|--------------|
| **Edge** | API Gateway, Health Monitoring |
| **Identity & Access** | Authentication, Authorization, Identity, User Management, Role Management, Permission Engine |
| **Control** | Tenant Management, Organization Management, Configuration Service, Localization, Secrets Management |
| **Content & Intelligence** | Document Engine, Media Library, File Storage, Search Engine, AI Platform, Analytics Platform |
| **Operations** | Notification Engine, Workflow Engine, Audit Engine, Integration Platform, Scheduling Platform, Background Workers, Report Engine |
| **Infrastructure** | Logging Platform, Monitoring Platform, Caching Platform, Event Bus / Outbox |

### 3. Bounded context mapping

Each capability maps to a bounded context (or shared infrastructure module) with its own schema and independent evolution. Identity plane capabilities share `identity` context in modular monolith but remain logical service boundaries.

New planned contexts: `secrets`, `scheduler`, `workers`, `file_storage`, `reporting`.

### 4. Module integration

Modules integrate via REST + versioned integration events only. Module activation triggers Core registration (permissions, settings, search indices, workflow definitions).

### 5. Canonical documentation

Master design: `docs/architecture/CORE_PLATFORM_DESIGN.md`  
Per-service API specs: `docs/architecture/CORE_PLATFORM.md`

## Consequences

### Positive

- Clear separation: platform vs industry
- All modules reuse one auth, audit, notification, and search stack
- Deployment flexibility (monolith → microservices) without contract change
- AI agents and engineers have explicit "no business logic in Core" test

### Negative

- More platform contexts to implement (`secrets`, `scheduler`, `workers`)
- Identity plane split requires discipline when co-located in one repo folder
- Event fan-out to audit/search/analytics must be monitored at scale

## Compliance

- Cursor rule: `.cursor/rules/marpich-core-platform.mdc`
- Platform charter updated to reference CORE_PLATFORM_DESIGN.md
