# ADR-022: Industry Catalog — Unlimited Industries, One Core

## Status

Accepted

## Context

Platform Charter lists sample customers but did not document the full industry domain catalog or the "unlimited industries" extensibility model. Product leadership defined the current domain list and the rule that every industry extends the same Core Platform.

## Decision

Adopt **`docs/architecture/INDUSTRY_CATALOG.md`** as the human-readable industry reference.

Keep machine-readable packs in **`backend/shared/contracts/industry_packs.json`**.

Add missing packs: `municipality`, `transportation`.

Enforce via **`.cursor/rules/marpich-industry-catalog.mdc`** (`alwaysApply: true`).

## Consequences

- New verticals add packs + modules, not new products
- Sales and engineering share one vocabulary for domains
- `hr_company` pack documented as Professional Services vertical

## Alternatives considered

- Fixed industry list only — rejected; unlimited extensibility is core to Marpich positioning
- Separate doc per industry — rejected; one catalog + JSON packs
