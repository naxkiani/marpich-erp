# ADR-051: Enterprise Chart of Accounts — Configurable Account Trees

## Status

Accepted

## Context

Financial Kernel (ADR-049) and General Ledger (ADR-050) established journal posting and trial balance. The initial COA implementation was flat with hardcoded account numbers in Python (`industry_coa.py`). Enterprise requirements demand unlimited hierarchy, parent/child accounts, account groups, seven categories (including off-balance and statistical), tenant-specific accounts, industry and country templates, and fully configurable account codes with no hardcoded numbers in application logic.

## Decision

Adopt **`docs/architecture/ENTERPRISE_CHART_OF_ACCOUNTS.md`** as canonical COA law within `financial_kernel` context.

COA extensions:
- Hierarchical `ChartOfAccount` aggregate with `parent_account_id`, unlimited `level`, `tree_path`, `account_group`, `account_category`
- Semantic `account_key` for module integration; tenant-configurable `code`
- Industry templates (14 packs) and country templates (US GAAP, Iran IFRS, EU IFRS) in `ACCOUNT_TREE_TEMPLATES.v1.yaml`
- Template loader — no account numbers in Python application code
- COA API prefix: `/api/v1/financial-kernel/coa/*`
- GL posting validates `is_posting` and rejects off-balance/statistical GL lines

## Consequences

- Modules resolve accounts by `account_key` via COA API, not hardcoded codes
- Tenant provision seeds hierarchical industry template automatically
- Country overlays applied as merge templates
- Legacy flat `POST /ledger/accounts` remains with extended optional parent fields

## Alternatives considered

- Fixed numeric COA per industry — rejected (multi-country, tenant customization)
- Separate COA context — rejected (kernel owns COA per ADR-049)
- Hardcoded codes in Python constants — rejected (configuration-only in YAML)
