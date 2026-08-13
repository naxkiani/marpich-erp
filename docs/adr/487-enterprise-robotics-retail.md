# ADR 487 — Enterprise Robotics Autonomous Commerce / Retail (P216-O)

## Status

Accepted

## Context

P216-L established public safety / civil protection. P216-J (agriculture), P216-M (space), and P216-N (environmental) remain planned. P216-O extends MEOS Robotics into retail robotics, customer experience automation, autonomous commerce, and intelligent retail operations — preparing for P216-P hospitality robotics.

## Decision

1. SoR remains `robotics` / `CAP-PLT-RB-001`.
2. Fabric: `meos_autonomous_commerce_fabric`.
3. API: `/api/v1/robotics/retail*`.
4. Core domain: Enterprise Commerce Intelligence; aggregate RetailIntelligenceAggregate.
5. Eight bounded contexts (customer experience through retail governance).
6. Payment/POS/CRM/e-commerce via Integration Platform and peer APIs — never direct vendor embeds in domain.
7. Physical AI via P214-Z / P216-E ACL; never module-local LLM.
8. Never duplicate POS/sales/CRM core logic; store peer IDs only.
9. Privacy by design and responsible AI; ungated physical autonomy forbidden.
10. Never replace Core, AI, Quantum, or prior delivered P216 fabrics (through P216-L).
11. ADR 485 reserved for P216-M space; ADR 486 reserved for P216-N environmental; ADR 482 remains reserved for P216-J agriculture.

## Consequences

Positive: unified retail cyber-physical commerce intelligence under robotics SoR.  
Negative: POS/CRM/e-commerce/WMS remain external SoRs; robotics projects via ACL and events.

## Alternatives rejected

- Sibling `retail_robotics` BC outside SoR robotics.
- Embedding payment SDKs or POS engines in robotics domain.
- Fully autonomous customer robots without privacy and safety envelopes.

## Related

Law: `ENTERPRISE_ROBOTICS_RETAIL.md`  
Roadmap: `robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml`
