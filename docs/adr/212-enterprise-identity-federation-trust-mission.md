# ADR-212: Enterprise Identity Federation & Trust Platform — Mission (P200-B1.1-A)

## Status

Accepted — Mission foundation (V03-C03)

## Context

Volume 03 Chapter 03 introduces **EIFTP** (Enterprise Identity Federation & Trust Platform) as the MEOS **Enterprise Trust Backbone**. P198 already delivered the `identity_federation` bounded context (ADR-202 … 202f) as Federation & SSO fabric.

Blueprint Prompt **P200-B1.1-A** asks for Mission documentation, identity taxonomy, trust domains, Zero Trust mission model, and architecture compliance — **not** a second federation codebase.

**Naming collision note:** Marpich ADR-204 / Prompt 200 already denotes *Authorization PDP*. Blueprint **P200-B** is Volume 03 Chapter 03 Federation & Trust series. This ADR binds P200-B1.1-A to EIFTP Mission and keeps Authorization under ADR-204/211.

## Decision

1. **Single SoR for federation protocols, trust relationships, and mesh** remains `backend/contexts/identity_federation/` (reuse P198).
2. **EIFTP Mission law** lives in `docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_TRUST_PLATFORM.md` and catalogs under `docs/architecture/identity/eiftp/`.
3. **No module** may implement independent IdP / SSO / trust vault outside Identity plane (Platform Charter).
4. **AuthZ (ADR-204)** stays the access PDP; EIFTP establishes and governs *trust* — AuthZ consumes trust signals as facts, never duplicates trust SoR.
5. Subsequent prompts: **P200-B1.1-B Vision** → architecture → protocols → ops — each extends catalogs, never forks the BC.

## Trust philosophy

Trust by Verification · continuous · context-aware · Zero Trust (never trust by default).

## Consequences

- Mission validation tests assert taxonomy / domain / ZT catalogs exist and are consistent with `identity_federation` ownership.
- P200-B code changes extend adapters/engines inside `identity_federation` + Identity companions; do not create `eiftp` sibling context.

## References

- ADR-202 … 202f (Federation)
- ADR-195 (EITAP umbrella)
- ADR-204 / 211 (Authorization — separate)
- Catalogs: `docs/architecture/identity/eiftp/`
