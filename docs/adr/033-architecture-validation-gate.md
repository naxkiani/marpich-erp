# ADR-033: Architecture Validation Gate — Pre-Code Enterprise Grade

## Status

Accepted

## Context

Marpich has extensive architecture docs (DDD, dependency graph, module tree, security, performance, AI). Agents and developers can still skip design and generate code that violates layer rules, omits tests, or duplicates Core.

Product leadership mandated: **before generating any code**, validate architecture across fifteen dimensions. If the score is below **Enterprise Grade**, **stop**, improve architecture, then code. **Never sacrifice architecture quality.**

## Decision

1. Adopt **`docs/architecture/ARCHITECTURE_VALIDATION.md`** as the pre-code validation law.

2. **Enterprise Grade threshold:**
   - All automated hard gates PASS
   - Every dimension scored ≥ 3 (1–5 scale)
   - Average ≥ 4.0
   - Critical dimensions (Modularity, DDD Compliance, Clean Architecture, Security) ≥ 4

3. **Automated hard gates:** `scripts/validate-architecture.py` + `scripts/check-dependency-graph.py`

4. **Manual scorecard:** Required in architecture brief / PR before implementation.

5. Enforce via **`.cursor/rules/marpich-architecture-validation.mdc`** (`alwaysApply: true`).

6. Integrate as **Step 0** in [DEVELOPMENT_PROTOCOL.md](../architecture/DEVELOPMENT_PROTOCOL.md).

## Consequences

- Agents must output scorecard and pass hard gates before writing code
- Below-threshold designs require architecture improvement, not feature hacks
- CI can add `validate-architecture.py` to pipeline (hard gates only)

## Alternatives considered

- Rely on ENGINEERING_QUALITY_STANDARD only — post-hoc; does not block bad design before code
- Fully automated scoring — many dimensions (DX, DDD nuance) need human/agent judgment
- Single boolean checklist — insufficient; scoring exposes weak dimensions
