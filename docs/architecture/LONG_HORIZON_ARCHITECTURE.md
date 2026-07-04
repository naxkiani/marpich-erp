# Marpich Long-Horizon Architecture

**Status:** Canonical — mindset for **every** code generation decision  
**Audience:** Engineering, AI agents, architects, reviewers  
**Companions:** [DEVELOPMENT_PROTOCOL.md](DEVELOPMENT_PROTOCOL.md) · [PLATFORM_CHARTER.md](PLATFORM_CHARTER.md)

**Rule: Never think about today's request only. Never sacrifice architecture for speed.**

---

## The Ten-Year Mindset

When generating or reviewing code, optimize for **2036**, not just the current ticket.

| Think about | Design implication |
|-------------|------------------|
| **Next ten years** | Versioned contracts, ADRs, reversible decisions; no dead-end shortcuts |
| **One million users** | Horizontal scale, stateless services, pagination, caching, async |
| **Ten thousand organizations** | Multi-tenant isolation (`tenant_id` everywhere), pack-based activation, no hardcoded tenant logic |
| **AI evolution** | AI as platform service; module hooks — not embedded models ([AI_PLATFORM_STANDARD.md](AI_PLATFORM_STANDARD.md)) |
| **Cloud scalability** | 12-factor, containers, workers, event-driven ([PERFORMANCE_STANDARD.md](PERFORMANCE_STANDARD.md)) |
| **Maintainability** | DDD layers, bounded contexts, tests, docs, small modules |
| **Extensibility** | Plugins, industry packs, integration events — extend Core, never fork |

---

## Platform Laws (long horizon)

```
┌────────────────────────────────────────────────────────────┐
│  Today's feature must survive:                              │
│  · 10 years of schema/API evolution (versioning)            │
│  · 1M users (scale-out, not scale-up hacks)                 │
│  · 10K tenants (isolation, config, packs)                   │
│  · AI paradigm shifts (platform abstraction)                │
│  · Cloud-native ops (observability, zero-downtime deploy)   │
└────────────────────────────────────────────────────────────┘
```

| Law | Meaning |
|-----|---------|
| **Always leave architecture better than before** | Refactor weak patterns when you touch them; Boy Scout rule |
| **Never sacrifice architecture for speed** | Shortcuts require ADR + explicit debt ticket — default is no |
| **Never today's request only** | Ask: does this block unlimited industries? duplicate Core? cap scale? |

---

## Decision Checklist (before every PR)

```markdown
## Long-horizon review

- [ ] Survives 10 years — versioned API/events, migration path documented
- [ ] Scales to 1M users — no unbounded queries, async, cache, indexes
- [ ] Scales to 10K orgs — tenant_id, RLS, pack config, no tenant hardcoding
- [ ] AI-ready — platform hooks, not embedded LLM
- [ ] Cloud-native — stateless, env config, observable, worker-ready
- [ ] Maintainable — tests, docs, clear boundaries
- [ ] Extensible — modules/events, not monolith growth
- [ ] Architecture improved or unchanged — not worse than before
- [ ] No speed-at-cost-of-architecture without ADR
```

---

## What "better architecture" means in Marpich

| If you touch… | Leave it better by… |
|---------------|---------------------|
| Weak coupling | Replace cross-import with integration event |
| Missing contract | Add JSON schema + contract test |
| Monolithic context | Split plan or extract module boundary |
| Untested path | Add integration test |
| Duplicate Core logic | Move to platform service |
| Hardcoded industry | Industry pack + settings schema |

---

## Speed vs architecture

| Allowed fast path | Not allowed |
|-------------------|-------------|
| Minimal diff that **follows** existing patterns | Copy-paste to ship today |
| Feature flag for incomplete module | Disabled auth "temporarily" |
| ADR-documented spike behind flag | Permanent hack without ticket |
| Improve one layer while adding feature | Layer hack on broken foundation |

**Default:** Correct architecture first. Speed comes from reuse, not shortcuts.

---

## Links to operational standards

| Concern | Standard |
|---------|----------|
| Reuse before code | [DEVELOPMENT_PROTOCOL.md](DEVELOPMENT_PROTOCOL.md) |
| One platform | [PLATFORM_CHARTER.md](PLATFORM_CHARTER.md) |
| Scale & perf | [PERFORMANCE_STANDARD.md](PERFORMANCE_STANDARD.md) |
| Security at scale | [SECURITY_STANDARD.md](SECURITY_STANDARD.md) |
| Modules & industries | [MODULE_STRUCTURE_STANDARD.md](MODULE_STRUCTURE_STANDARD.md), [INDUSTRY_CATALOG.md](INDUSTRY_CATALOG.md) |

---

## Enforcement

| Mechanism | Location |
|-----------|----------|
| Cursor rule | `.cursor/rules/marpich-long-horizon.mdc` |
| Development protocol | [DEVELOPMENT_PROTOCOL.md](DEVELOPMENT_PROTOCOL.md) |

**Review rejection:** Changes that worsen coupling, skip tenant isolation, or add unbounded scale debt without ADR.
