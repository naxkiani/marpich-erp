# ADR 481 — Enterprise Robotics Healthcare Robotics (P216-I)

## Status

Accepted

## Context

P216-H established autonomous mobility. P216-I extends MEOS Robotics into healthcare robotics, medical AI, surgical robotics, and digital healthcare automation — preparing for P216-J agricultural robotics.

## Decision

1. SoR remains `robotics` / `CAP-PLT-RB-001`.
2. Fabric: `meos_healthcare_robotics_fabric`.
3. API: `/api/v1/robotics/healthcare*`.
4. Core domain: Enterprise Healthcare Intelligence; aggregate HealthcareRoboticsAggregate.
5. Eight bounded contexts (patient care through clinical governance).
6. FHIR/HL7/DICOM/EHR/HIS via Integration Platform — never direct vendor embeds in domain.
7. Medical AI and Physical AI via P214-Z / P216-E ACL; never module-local LLM.
8. Never duplicate hospital/clinic core logic; store peer IDs only.
9. Human-in-the-loop required for clinical autonomy; ungated physical autonomy forbidden.
10. Never replace Core, AI, Quantum, or prior P216 fabrics.

## Consequences

Positive: unified healthcare cyber-physical intelligence under robotics SoR.  
Negative: hospital/clinic/LIS/pharmacy remain external SoRs; robotics projects via ACL and events.

## Alternatives rejected

- Sibling `healthcare_robotics` BC outside SoR robotics.
- Embedding FHIR/HL7 stacks in robotics domain.
- Autonomous surgery without human-in-the-loop and safety envelopes.

## Related

Law: `ENTERPRISE_ROBOTICS_HEALTHCARE.md`  
Roadmap: `robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml`
