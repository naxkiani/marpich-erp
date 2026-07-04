# ADR-046: Enterprise Feature Flag System

## Status

Accepted

## Context

Feature toggles today live as a flat `features` dict on `TenantSettings` — tenant-only, boolean, no rollout, A/B, canary, emergency kill, or multi-scope evaluation. Gateway and modules need tenant, organization, user, environment, country, and industry dimensions plus version control and a feature dashboard.

## Decision

Adopt **`docs/architecture/ENTERPRISE_FEATURE_FLAG_SYSTEM.md`** as canonical feature flag law.

New bounded context **`feature_flags`** owns registry, evaluation, rollout, A/B, emergency disable, version history, and dashboard.

Settings `features` remains for backward compatibility — delegates to Feature Flag System over time.

Evaluation via `IFeatureFlagEvaluator` port — modules and gateway call `POST /feature-flags/evaluate`.

## Consequences

- No hardcoded env gates in modules
- Emergency disable audited via integration events
- Gateway route flags call evaluate API
- Default flags seeded on tenant provision

## Alternatives considered

- Flags only in Settings JSON — rejected (no rollout/A/B/versioning)
- LaunchDarkly-only external — rejected as sole source (OTel + tenant model require platform service)
- Per-module flag files — rejected (fragmentation)
