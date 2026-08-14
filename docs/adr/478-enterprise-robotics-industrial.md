# ADR 478 — Enterprise Robotics Industrial Automation & Smart Factory (P216-F)

## Status

Accepted

## Context

P216-E established Physical AI. P216-F extends robotics into industrial manufacturing: smart factory, autonomous production, OT automation, quality, predictive maintenance, factory digital twin, and industrial intelligence — preparing for P216-G logistics/warehouse automation.

## Decision

1. SoR remains `robotics` / `CAP-PLT-RB-001`.
2. Fabric: `meos_industrial_intelligence_fabric`.
3. API: `/api/v1/robotics/industrial*`.
4. Core domain: Industrial Manufacturing Intelligence; aggregate IndustrialManufacturingAggregate.
5. Eight bounded contexts (factory through industrial intelligence).
6. OT protocols (OPC UA, MQTT, Modbus, etc.) via Integration Platform connectors — never direct vendor embeds in domain/application.
7. Align ISA-95/88, IEC 62443, Industry 4.0/5.0; AI inference via P214-Z ACL.
8. Never replace Core, AI, Quantum, or P216 foundation through Physical AI fabrics.

## Consequences

Positive: unified cyber-physical manufacturing under MEOS robotics SoR.  
Negative: MES/SCADA ownership remains peer systems; robotics stores plant IDs and projections only.

## Alternatives rejected

- Separate `smart_factory` sibling BC outside SoR robotics.
- Embedding PLC SDKs in robotics domain.
- Module-local industrial metrics/alerting stores.

## Related

Law: `ENTERPRISE_ROBOTICS_INDUSTRIAL.md`  
Roadmap: `robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml`
