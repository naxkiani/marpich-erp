# ADR-032: Dependency Graph — Layer and Module Import Law

## Status

Accepted

## Context

Marpich modules follow identical internal layers (Presentation → Application → Domain; Infrastructure implements Domain contracts). Without enforced import rules, layers collapse (application services importing ORM adapters, presentation calling repositories) and business modules couple directly to each other.

Product leadership mandated:
- Presentation depends on Application
- Application depends on Domain
- Infrastructure depends on Application and implements Domain contracts
- Domain depends on nothing (except Shared Kernel)
- Core depends on nothing (business)
- Business modules depend only on Core, Shared Kernel, and Public Contracts
- Never allow circular dependency
- Automatically detect violations

## Decision

1. Adopt **`docs/architecture/DEPENDENCY_GRAPH.md`** as canonical dependency law.

2. Implement static AST analyzer in **`backend/shared/kernel/dependency_graph.py`**.

3. Enforce in CI via:
   - `scripts/check-dependency-graph.py`
   - `backend/tests/architecture/test_dependency_graph.py`
   - Baseline file `dependency_baseline.json` for known legacy layer debt (21 entries at adoption)

4. **Zero tolerance** (no baseline) for: circular module imports, Shared Kernel → contexts, business → business, core → business.

5. **Legacy allowance:** application → infrastructure in existing `service.py` files until migrated to ports + `container.py` wiring.

## Consequences

- New layer or cross-module violations fail CI immediately
- Fixing legacy debt shrinks baseline via `--update-baseline`
- Module authors use integration events instead of cross-context imports

## Alternatives considered

- Import-linter third-party only — insufficient for Core vs business rules
- Fail on all 21 legacy violations now — blocks delivery; baseline tracks debt down
- Runtime dependency injection checks — static AST is faster and runs in every PR
