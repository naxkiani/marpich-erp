## ADR-327: Enterprise Identity Intelligence CQRS, Events, APIs & Microservices Platform

### Status
Accepted

### Context
`identity_intelligence` is the deployable system of record for the P207 series. P207-A through P207-K established strategy, mission scope, domain boundaries, autonomous operations, AI agents, digital twins, predictive risk, behavioral analytics, self-healing, governance optimization, and knowledge graph reasoning. The platform now requires a distributed runtime blueprint that defines how those capabilities operate through CQRS, events, secure APIs, and cloud-native service contracts without fragmenting the SoR.

### Decision
1. Keep `identity_intelligence` as the current deployable SoR while modeling the runtime as **logical microservices** under `/api/v1/identity-intelligence/fabric*`.
2. Define command, query, event, API, mesh, and deployment contracts as immutable catalogs owned by `identity_intelligence`.
3. Enforce **no shared databases**, **no undefined events**, **no insecure APIs**, **no unclear CQRS boundaries**, **no incomplete audit history**, and **no disconnected AI integration**.
4. Use platform dependencies only:
   - AI inference via AI Platform
   - authorization via Authorization PDP
   - audit history via Audit Platform
   - graph projection via `directory`
   - twin simulation via `identity_digital_twin`
   - metrics/traces via Observability Platform
5. Treat the named microservices in the prompt as **logical service boundaries** that can evolve into independently deployable units later, while `identity_intelligence` remains the present deployable unit.

### Consequences
- P207 capabilities gain a unified distributed runtime model with event-driven, API-first, and Zero Trust semantics.
- The system is prepared for later physical decomposition without inventing sibling bounded contexts.
- Production readiness becomes measurable through service boundary, CQRS, event, API, security, and Kubernetes readiness contracts.
