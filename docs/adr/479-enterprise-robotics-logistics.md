# ADR 479 — Enterprise Robotics Autonomous Logistics (P216-G)

## Status

Accepted

## Context

P216-F established smart factory / industrial automation. P216-G extends cyber-physical intelligence into warehousing, fulfilment, material flow, and transport coordination — preparing for P216-H autonomous mobility / drones / smart transportation.

## Decision

1. SoR remains `robotics` / `CAP-PLT-RB-001`.
2. Fabric: `meos_autonomous_logistics_fabric`.
3. API: `/api/v1/robotics/logistics*`.
4. Core domain: Enterprise Autonomous Logistics Intelligence; aggregate EnterpriseAutonomousLogisticsAggregate.
5. Eight bounded contexts (warehouse through digital twin).
6. Never duplicate WMS/TMS/ERP core logic — integrate via APIs/events; store peer IDs only.
7. Physical AI via P214-Z ACL; fleet/runtime via P216-D; industrial sync via P216-F.
8. Never replace Core, AI, Quantum, or prior P216 fabrics.

## Consequences

Positive: unified autonomous logistics under MEOS robotics SoR.  
Negative: commercial WMS/TMS remain systems of record for classic inventory documents where already owned.

## Alternatives rejected

- Sibling `warehouse` BC outside SoR robotics for robot-native logistics.
- Embedding WMS aggregates inside robotics domain.
- Module-local LLM for logistics optimisation.

## Related

Law: `ENTERPRISE_ROBOTICS_LOGISTICS.md`  
Roadmap: `robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml`
