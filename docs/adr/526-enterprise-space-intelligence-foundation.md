# ADR 526 — Enterprise Space Intelligence Foundation (P218)

## Status
Accepted

## Context
After P215 Quantum, P216 Robotics, and P217 Biotechnology, MEOS expands into Space Intelligence: Space AI, orbital civilization systems, and autonomous space operations under a new SoR `space`.

## Decision
1. New SoR `space` (`CAP-PLT-SP-001`); fabric `meos_space_intelligence_fabric`.
2. API surface `/api/v1/space*` with foundation under `/space/foundation*`.
3. Inference only via P214-Z; robotics physical systems via P216-Z; quantum via P215-Z; bio life-support via P217 ACL.
4. External ground/space systems via Integration Platform only — no direct vendor SDKs in domain.
5. Mission-critical decisions require Workflow + explainability; never ungated autonomous mission release.
6. Zero-trust space infrastructure; space cybersecurity and satellite identity mandatory.
7. Never replace Core / AI / Quantum / Robotics / Biotechnology.
8. Foundation for P218-A capability framework.

## Consequences
Positive: clean SoR for planetary/orbital intelligence without merging into robotics or bio.  
Negative: new schema and permissions; must keep peer IDs only across domains.

## Links
Law: `ENTERPRISE_SPACE_INTELLIGENCE_FOUNDATION.md` · Prior: ADR 525 (P217-Z) · Next: P218-A
