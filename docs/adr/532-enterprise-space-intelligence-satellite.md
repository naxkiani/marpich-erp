# ADR 532 — Enterprise Space Intelligence Satellite Intelligence (P218-F)

## Status

Accepted

## Context

P218-E established the Space AI Intelligence Core. P218-F defines satellite intelligence, constellation management, orbital asset operations, payload intelligence, satellite AI, and satellite digital twin — before Orbital Traffic / SSA (P218-G).

## Decision

1. SoR remains `space` / `CAP-PLT-SP-001`.
2. Fabric: `meos_satellite_intelligence_fabric`.
3. API: `/api/v1/space/satellite*`.
4. Five satellite intelligence layers; ten lifecycle phases; constellation + payload + satellite-AI catalogs.
5. All satellite AI inference via P214-Z / P218-E ACL only — `no_module_local_llm`.
6. Telemetry / ground links via Integration Platform — `no_module_local_telemetry_stack`.
7. Secure command uplink requires Workflow + Policy — never ungated satellite command uplink.
8. Never replace Core, AI, Quantum, Robotics, Biotechnology, prior P218 fabrics (including P218-E).
9. Foundation for P218-G.

## Consequences

Positive: governed fleet-scale satellite platform for subsequent orbital-traffic domains.  
Negative: constellation optimisation must stay aligned with Quantum (P215-Z) and Space AI (P218-E) contracts.

## Alternatives rejected

- Sibling `satellite` BC outside SoR space.
- Module-local LLM or telemetry brokers.
- Ungated autonomous constellation reconfiguration without workflow approval.

## Related

Law: `ENTERPRISE_SPACE_INTELLIGENCE_SATELLITE.md` · Prior: ADR 526–531 · Next: P218-G
