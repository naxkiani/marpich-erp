# ADR-P3: Router Package Contract Gate

## Status

Accepted — Completeness audit P3

## Context

`ROUTER_SPECS` / service warmup lists historically referenced packages and modules that do not exist. P0 gated deferred contexts at runtime; P2 froze empty scaffolds and blueprint fabrics. Without a CI contract, new ghost specs can still land and inflate OpenAPI omission noise.

## Decision

1. Freeze current missing module paths in `backend/tests/architecture/missing_router_packages_baseline.json`.
2. Contract tests in `backend/tests/contracts/test_router_package_contracts.py`:
   - Fail when the missing set **grows** (new ghost ROUTER/SERVICE specs).
   - Fail when baseline entries **now resolve** but were not removed (force baseline shrink).
   - Fail when a missing context package directory is not in `DEFERRED_CONTEXT_IDS`.
3. CI workflow `.github/workflows/meos-p3-router-contracts.yml` runs the contracts + `scripts/check-missing-router-packages.py`.

## How to land a new module

1. Implement the package under `backend/contexts/{id}/`.
2. Add ROUTER_SPEC / service spec.
3. Remove the module path from the baseline JSON in the same PR.
4. Do **not** expand the baseline to hide unfinished work — prefer deferring the spec or implementing the package.

## References

- Completeness audit canvas P3
- `startup_registry.py` (`DEFERRED_CONTEXT_IDS`, `EMPTY_INDUSTRY_SCAFFOLD_IDS`)
- ADR-P2 blueprint/scaffold honesty
