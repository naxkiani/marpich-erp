# ADR-213: Enterprise Identity Federation & Trust Platform — Vision (P200-B1.1-B)

## Status

Accepted — Vision foundation (V03-C03)

## Context

P200-B1.1-A (ADR-212) established EIFTP Mission. P200-B1.1-B defines the **long-term vision**: Global Enterprise Trust Fabric, identity-as-continuously-verified-asset, AI as first-class identity citizen, and future-state architecture — still **without** a sibling BC.

## Decision

1. Vision law: `docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_TRUST_VISION.md`
2. Catalogs under `docs/architecture/identity/eiftp/` (`VISION_*`, capability matrix, trust fabric edges, AI identity vision, checklists)
3. Future-state maps capabilities to **existing Identity plane owners** (federation, authentication, adaptive auth, AuthZ, IGA, directory, twin, policy) — vision does not invent parallel SoRs
4. Scale targets (1M users / 10K orgs / unlimited tenants) inherit LONG_HORIZON_ARCHITECTURE — tenant isolation never weakened
5. Next: **P200-B1.1-C** DDD Strategic Design & Enterprise Scope builds on Mission + Vision

## Non-goals

- Replacing Authorization PDP
- Embedding OpenAI/IdP SDKs in business modules
- Creating `contexts/eiftp/`

## References

- ADR-212 (Mission) · ADR-202× (Federation) · ADR-195 (EITAP) · ADR-204 (AuthZ)
- Vision catalogs: `docs/architecture/identity/eiftp/VISION_*.yaml`
