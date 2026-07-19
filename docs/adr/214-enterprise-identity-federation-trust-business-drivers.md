# ADR-214: Enterprise Identity Federation & Trust Platform — Business Drivers (P200-B1.1-C)

## Status

Accepted — Business Drivers foundation (V03-C03)

## Context

P200-B1.1-A/B defined Mission and Vision. P200-B1.1-C captures the **immutable business drivers** that justify and constrain EIFTP and all downstream identity/authn/authz/trust design in MEOS.

**Note:** Earlier Vision prompt foreshadowed “DDD Strategic Design” as C; the Blueprint Master Prompt for C is **Business Drivers**. DDD Strategic Design will follow later in the series. Strategic Goals are **P200-B1.1-D**.

## Decision

1. Business Drivers law: `docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_TRUST_BUSINESS_DRIVERS.md`
2. Catalogs under `docs/architecture/identity/eiftp/BUSINESS_*` and related matrices
3. Drivers are **architectural inputs** — implementations that create multiple identity authorities, break tenant isolation, or couple identity into business modules **fail quality gates**
4. SoR remains `identity_federation` + Identity plane companions; AuthZ stays ADR-204

## Consequences

- P200-B1.1-D Strategic Goals must trace to these drivers
- Capability and compliance matrices map drivers → outcomes → owners

## References

- ADR-212 Mission · ADR-213 Vision · ADR-202× Federation · ADR-204 AuthZ
