# MEOS P355 — Productization

**Status:** `PRODUCTIZATION_LAYER_READY` — **not** `PRODUCT_READY` until clean tree + GHCR digest, and **not** `PRODUCTION_CERTIFIED`.  
**Tracks:** A productization (this) ∥ B infrastructure (G26/P313). Track A does not wait for Track B.

P355 is a productization layer over existing Identity, Organization, Settings, Feature Flags, Accounting, Plugin Platform, AppShell, P354 installer, and P353 packages. It is **not** a second ERP, billing engine, identity system, or marketplace.

## MEOS_PRODUCT

`python3 scripts/meos_product_engine.py`  
Dirty source (`*-dirty`, including `47258dfd-dirty`) is **FORBIDDEN** as a commercial release.

## Entitlement (server-side)

`POST /api/v1/feature-flags/entitlements/evaluate`  
Uses `contexts.feature_flags.application.product_entitlement`. Client flags are **not** trusted.

## Commands

```bash
python3 scripts/meos-product-readiness.py
python3 scripts/meos-onboard.py
python3 scripts/meos-demo.py health
python3 scripts/meos-release.py inspect
```

Onboarding is **PLAN_ONLY**. `--production` does not create a production tenant.

Payment execution: **READY_FOR_CREDENTIALS** (Accounting invoices exist; no fabricated transactions).

## Frozen

G26_READY = FALSE · P0 = 1 · P313 = NOT_CERTIFIED · GO_LIVE_AUTHORIZATION = NOT_APPROVED · ACTIVE_APPLICATIONS = 0 · PRODUCTION_TRAFFIC = NOT_ENABLED
