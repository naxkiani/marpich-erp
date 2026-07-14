# ADR-203: Enterprise Identity Digital Twin Platform

## Status
Accepted — extended by [ADR-203a](203a-digital-twin-type-catalog.md) for Prompt **V03-C02-P199-A** multi-kind catalog

## Context
Identity state is distributed across Identity, Federation, Lifecycle, and Risk. Consumers need a tenant-isolated, auditable projection for analysis without importing peer aggregates or querying peer schemas. Prompt 199-A further requires organization/device/session/AI-agent/industry twin kinds with trust/risk/compliance facets — still as projections, not SoR.

## Decision
Create `identity_digital_twin` as a Platform bounded context. It stores reference-only projections, consumes versioned integration events through ACL handlers, publishes immutable twin events via the Event Fabric, and delegates configurable controls to Policy Engine. Simulations are deterministic and non-mutating; authoritative state changes remain owned by their source contexts. AI hooks are declared for the AI Platform, with no embedded model client.

Twin **kinds** are catalog-driven (ADR-203a); one BC serves all kinds.

## Consequences
- The twin is eventually consistent and must surface source versions.
- No peer identity, federation, lifecycle, or risk aggregate may be imported.
- Drift alerts are evidence for operators; remediation requires a source-context command or workflow.
- Industry twins never duplicate hospital/bank/university tables — only projections from those contexts' events.

## References
- [ENTERPRISE_IDENTITY_DIGITAL_TWIN_PLATFORM.md](../architecture/ENTERPRISE_IDENTITY_DIGITAL_TWIN_PLATFORM.md)
- [ENTERPRISE_TWIN_SYNCHRONIZATION_EVENT_MESH.md](../architecture/ENTERPRISE_TWIN_SYNCHRONIZATION_EVENT_MESH.md)
- [ADR-203a](203a-digital-twin-type-catalog.md)
- [ADR-207](207-twin-synchronization-engine-event-mesh.md)
