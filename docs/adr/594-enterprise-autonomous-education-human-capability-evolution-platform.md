# ADR 594 — Enterprise Autonomous Education & Human Capability Evolution Platform (P234)

## Status
Accepted

## Context
P233 established EAHIBEP (healthcare & bio-evolution intelligence). P234 opens the Enterprise Autonomous Education & Human Capability Evolution Platform (EAEHCEP) for lifelong learning, skill intelligence, personalized pathways, talent development and workforce transformation under MEOS 11.0. University, School and HR remain authoritative education/workforce SoRs — EAEHCEP is intelligence/personalization only and must never merge university≠school.

## Decision
1. SoR `education_intelligence`; fabric `meos_enterprise_autonomous_education_human_capability_evolution_platform_framework`; API `/api/v1/education-intelligence*`; capability `CAP-PLT-EAEHCEP-001`.
2. Ten logical BCs inside one SoR: Learning Management, Skill Intelligence, Capability Development, Talent, Knowledge Evolution, Career Intelligence, Learning Analytics, Education Governance, Workforce Transformation, Human Digital Twin bindings.
3. Federate with university, school, hr, P223, P228, P227, P230, P224, P219-J via ACL/events — never replace them.
4. Inference only via P214-Z; credential/employment mutations via owning SoRs + Workflow; privacy via P230; content via Documents; LMS via Integration Platform.
5. Never merge university≠school; never module-local LLM/search; never content blobs in module tables; never silent grade/transcript/employment mutation; never silent consent override.
6. Roadmap: P234 foundation → P234-A…D (skills/journeys → AI/twin → workforce/career → civilization-scale gated capability evolution).

## Consequences
Positive: governed lifelong learning and capability intelligence across federated education/HR SoRs.  
Negative: enrollments, grades, transcripts and employment records remain peer-owned — EAEHCEP stores profiles, journeys, assessments and plans with peer refs only.

## Links
Law: `ENTERPRISE_AUTONOMOUS_EDUCATION_HUMAN_CAPABILITY_EVOLUTION_PLATFORM.md` · Prior: ADR 593 · Next: P234-A · Peer: ADR 595 (P235 EAHRWIP)
