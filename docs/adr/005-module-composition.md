# ADR-005: Module Composition Over Separate Systems

## Status

Accepted

## Context

Marpich must serve 25+ industries (universities, hospitals, banks, retail, etc.) while competing with platforms that offer industry-specific solutions (SAP for manufacturing, Epic for healthcare, etc.).

Building separate codebases per industry would:
- Duplicate finance, HR, CRM, inventory logic
- Fragment security patches and compliance updates
- Prevent cross-industry customers (e.g., a hospital that also runs a pharmacy)
- Increase maintenance cost exponentially

## Decision

All industry capabilities are **composable modules** registered via `IModuleManifest`. Industries are activated through **Industry Packs** that declare required and optional module sets.

```
Industry Pack "hospital" → activates healthcare.* + platform.finance + platform.hr
Industry Pack "retail"   → activates retail.* + platform.finance + platform.inventory
```

Shared domain logic (finance, HR, CRM) exists once. Industry-specific logic extends via module dependencies, not duplication.

## Consequences

### Positive
- Single deployment pipeline for all industries
- Shared security, audit, and compliance infrastructure
- Customers can activate multiple industry packs on one tenant
- New industries = new module pack, not new system

### Negative
- Module dependency graph must be carefully managed
- Configuration complexity increases (mitigated by industry pack defaults)
- Performance tuning requires tenant-scoped benchmarking

## Alternatives Considered

1. **Separate repos per industry** — Rejected: unmaintainable at scale
2. **Fork-per-customer** — Rejected: violates DRY, blocks upgrades
3. **Plugin marketplace only (like Odoo)** — Partially adopted: modules are internal-first, external plugins planned for Phase 2
