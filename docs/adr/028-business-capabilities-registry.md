# ADR-028: Business Capabilities Registry

## Status

Accepted

## Context

Marpich architecture mandates design-before-code and capability-driven modules. Engineers and AI agents were at risk of creating modules, pages, or bounded contexts before naming the underlying business capability — leading to duplication (e.g. auth in every industry, merged hospital+clinic, FX inside treasury).

Product leadership requires: identify every business capability first; each capability eventually yields Application Service, Domain Service, Events, Reports, Permissions, UI Components, and API Contracts; never duplicate capabilities.

## Decision

1. Publish canonical **Business Capabilities Registry** at `docs/architecture/BUSINESS_CAPABILITIES_REGISTRY.md`.
2. Publish machine-readable catalog at `backend/shared/contracts/business_capabilities.json`.
3. Separate three tiers:
   - **Platform** (29 capabilities) — `CORE_PLATFORM_DESIGN.md`, not business
   - **Enterprise** (38 cross-industry capabilities)
   - **Industry** (35 vertical lifecycle capabilities)
4. Enforce design order: Capability → bounded context → aggregates → events → services → API → module manifest.
5. One capability → one owning bounded context; anti-duplication matrix in registry.

## Consequences

### Positive

- Clear inventory before implementation
- Module IDs derive from capabilities, not the reverse
- Duplication visible in registry review

### Negative

- Registry must be maintained when adding industries
- Some industry pack module names (`platform.hr`) must map to capability IDs explicitly

## Compliance

- Cursor rule: `.cursor/rules/marpich-capabilities.mdc`
- Chief Architect brief must cite capability ID
