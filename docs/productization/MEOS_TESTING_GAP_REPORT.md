# MEOS Testing Gap Report

**Date:** 2026-08-11

## Evidence

- ~754 backend `test_*.py` files; ~1.9k historical pytest nodeids
- Known failures in federation, banking, treasury, analytics, dependency graph, OpenAPI packs
- Frontend unit/integration folders are empty `.gitkeep`
- CI: niche federation/digital-twin workflows only — **no monorepo smoke gate**
- This environment may lack pytest installed

## Gaps

| Area | Gap | Priority |
|------|-----|----------|
| Platform smoke CI | Missing | P1 |
| Frontend shell tests | Missing | P1 |
| Auth + search + notifications e2e | Missing | P1 |
| Flaky/failing backend suite | 27 lastfailed | P1 |
| Domain scaffold tests | N/A until implemented | P2 |

## P1 test plan

1. Smoke: health + login + search query + notifications inbox + workflow list definitions
2. Frontend: shell search header injection unit test; nav registry render
3. Gate PR on smoke green before more productization docs
