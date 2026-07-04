# ADR-047: Enterprise Plugin Platform

## Status

Accepted

## Context

ADR-005 planned external plugins for Phase 2. Extension points exist (workflows, reports, widgets, webhooks) but only as first-party module hooks. Third-party developers need a governed path to ship Modules, Widgets, Reports, Dashboards, Themes, AI Skills, Integrations, and Workflow Extensions — with sandboxing, signing, permission control, versioning, upgrades, SDK, and marketplace discovery.

## Decision

Adopt **`docs/architecture/ENTERPRISE_PLUGIN_PLATFORM.md`** as canonical plugin law.

New bounded context **`plugins`** owns registry, marketplace listings, sandbox runtime, signing verification, install/upgrade lifecycle, and marketplace dashboard.

**Plugin SDK** at `packages/plugin-sdk/` — manifest types, validator, pack/sign CLI stubs.

**Marketplace architecture** at `docs/architecture/plugins/MARKETPLACE_ARCHITECTURE.md`.

Runtime invocation via `IPluginRuntime` port — modules never import plugin code directly.

Integration-type plugins delegate connector execution to Integration Platform after registration.

## Consequences

- Third-party extensions are signed, sandboxed, and permission-gated
- Marketplace provides discovery separate from tenant runtime
- Internal modules remain in Module Registry; plugins are additive
- Audit events on install, upgrade, invoke, sandbox violation
- Gateway may gate routes on `required_plugin`

## Alternatives considered

- Odoo-style app store only (no sandbox) — rejected (enterprise security)
- npm registry direct install — rejected (no permission/signature model)
- Extend Module Registry for third-party — rejected (different trust/sandbox requirements)
- Monolithic marketplace microservice — rejected (same bounded-context pattern as other platforms)
