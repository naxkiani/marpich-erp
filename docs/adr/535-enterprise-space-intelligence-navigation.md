# ADR 535 — Enterprise Space Intelligence Space Navigation (P218-I)

## Status

Accepted

## Context

P218-H established the space communications backbone. P218-I defines GNSS intelligence, autonomous navigation, trajectory optimisation, GNC, navigation AI and navigation digital twin — before Mission Intelligence (P218-J).

## Decision

1. SoR remains `space` / `CAP-PLT-SP-001`.
2. Fabric: `meos_space_navigation_intelligence_fabric`.
3. API: `/api/v1/space/navigation*`.
4. Five navigation layers; GNSS + autonomous nav + trajectory + GNC + navigation-AI catalogs.
5. All navigation AI via P214-Z / P218-E ACL only — `no_module_local_llm`.
6. GNSS/sensor receivers via Integration Platform — `no_module_local_gnss_receiver_stack`.
7. Guidance commands require Workflow + Policy — never ungated guidance command; human override always available.
8. Spoofing detection required — never skip GNSS spoofing detection.
9. Never replace Core, AI, Quantum, Robotics, Biotechnology, prior P218 fabrics (including P218-H).
10. Foundation for P218-J.

## Consequences

Positive: navigation foundation for mission planning/execution domains.  
Negative: GNC must stay aligned with Communications (P218-H), Orbital (P218-G), Satellite (P218-F) and Quantum (P215-Z) contracts.

## Alternatives rejected

- Sibling `navigation` BC outside SoR space.
- Module-local GNSS/IMU stacks.
- Fully autonomous guidance without human override gates.

## Related

Law: `ENTERPRISE_SPACE_INTELLIGENCE_NAVIGATION.md` · Prior: ADR 526–534 · Next: P218-J
