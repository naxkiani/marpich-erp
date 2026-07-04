# ADR-019: AI Platform Standard

## Status

Accepted

## Context

Platform Charter and Module Structure require "AI Extension" but did not define AI as a mandatory **platform service** with a fixed set of surfaces every module must expose. Teams could treat AI as optional or embed models inside modules.

Product leadership mandated: AI is Core; every module exposes insights, predictions, assistant, chat, anomaly detection, forecasting, and the full 14-surface catalog.

## Decision

Adopt **`docs/architecture/AI_PLATFORM_STANDARD.md`** as canonical AI law.

Enforce via **`.cursor/rules/marpich-ai-platform.mdc`** (`alwaysApply: true`).

Extend module manifest with required `ai:` block (all surfaces + prompt templates).

Link from Platform Charter, Module Structure Standard, README.

## Consequences

- Module PRs must complete 14-surface AI checklist
- AI inference only through `/api/v1/ai` (platform service)
- Dedicated `ai` bounded context implementation remains on platform roadmap; contract is fixed now

## Alternatives considered

- Per-industry optional AI — rejected; platform is AI-first
- Embed AI in each module — rejected; duplicates Core and violates charter
