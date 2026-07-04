# ADR-056: Enterprise Cost Centers

## Status

Accepted

## Context

Financial Kernel (ADR-049) defines cost centers and profit centers as engine capabilities but only provides basic seeding and listing. Business modules across hospital, construction, university, retail, and enterprise need rich center types (department, project, branch, faculty, hospital ward, construction site, warehouse, business unit), profit center linkage, budget/expense/revenue allocation, and profitability analysis.

## Decision

Adopt **`docs/architecture/ENTERPRISE_COST_CENTERS.md`** as canonical cost center law within `financial_kernel` context.

Cost Centers Engine:
- `EnterpriseCostCenter` with 8 center types and hierarchy
- `EnterpriseProfitCenter` linked to business units
- `CenterAllocation` for budget, expense, and revenue allocation
- Weighted split allocation across centers
- Profitability analysis from posted GL journals
- API prefix: `/api/v1/financial-kernel/cost-centers/*`

Integration events: `cost_center.created`, `profit_center.created`, `allocation.created`

## Consequences

- All modules create and allocate to cost centers via kernel API
- Profitability computed from posted journals with cost_center dimensions
- Legacy `/financial-kernel/cost-centers` list endpoint retained for seeded centers
- Enterprise platform is canonical for create, allocate, and analyze

## Alternatives considered

- Cost centers in each module — rejected (ADR-049 single kernel)
- Separate analytics context — deferred (kernel owns dimension semantics)
