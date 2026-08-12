# MEOS Test Status

**Date:** 2026-08-12

## Backend

| Metric | Value |
|--------|-------|
| `test_*.py` files | ~750+ |
| Historical pytest nodeids | ~1900 |
| Known lastfailed (cache) | ~27 (federation, banking, treasury, analytics, dependency graph, …) |
| Full monorepo CI | **Missing** (only federation / digital-twin niche workflows) |

## Frontend

| Metric | Value |
|--------|-------|
| Unit/integration tests | Empty `.gitkeep` only |
| Typecheck | Available via package scripts |

## Wave 01 CI target

Added: [`.github/workflows/meos-wave01-smoke.yml`](../../../.github/workflows/meos-wave01-smoke.yml)

- Focused pytest: identity + search + notifications + workflow smoke  
- Typecheck for `@marpich/shared` (and core best-effort)

Do not claim green platform until Wave 01 smoke is green on CI runners.
