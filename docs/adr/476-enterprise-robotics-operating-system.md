# ADR 476 — Enterprise Robotics Operating System (P216-D)

## Status

Accepted

## Context

P216-C established DDD bounded contexts and aggregates. P216-D defines EROS — the robotics operating fabric: HAL, robot runtime, Physical AI runtime (via P214-Z), robot services, fleet control plane, and MEOS intelligence integration — plus device/edge/mission/security/observability/self-healing models for P216-E Physical AI Engine.

## Decision

1. SoR remains `robotics` / `CAP-PLT-RB-001`.
2. Fabric: `meos_robotics_operating_fabric`.
3. API: `/api/v1/robotics/runtime*`.
4. Six-layer OS stack (HAL → Runtime → Physical AI Runtime → Services → Fleet Control → MEOS Intelligence).
5. Fleet control plane orchestrates; Policy Engine / Workflow / Audit remain Core — never duplicated.
6. Observability facets publish to platform Observability/Analytics — no module-local metrics stores.
7. Physical AI runtime invokes P214-Z ACL only; never embed LLM SDKs.
8. Never replace Core, AI, Quantum, or P216 foundation/mission/strategy/domain fabrics.

## Consequences

Positive: standardized execution layer for autonomous fleets.  
Negative: hardware drivers remain vendor adapters via Integration/HAL ports — not domain logic.

## Alternatives rejected

- Per-vendor ROS forks as enterprise SoR.
- Fleet control mutating peer BC aggregates in-process.
- Module-local Prometheus/alerting stacks.

## Related

Law: `ENTERPRISE_ROBOTICS_RUNTIME.md`  
Roadmap: `robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml`
