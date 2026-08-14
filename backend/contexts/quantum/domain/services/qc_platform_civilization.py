"""P215-W Enterprise Quantum Civilization Intelligence & Collective Network — immutable catalog."""
from __future__ import annotations
from typing import Any
PROMPT_ID = "P215-W"
ADR = 468
SOR = "quantum"
API_PREFIX = "/api/v1/quantum"
PRODUCT = "Enterprise Quantum Civilization Intelligence Layer, Collective Quantum Intelligence Network, Global Cognitive Ecosystem & MEOS Future Quantum Intelligence Civilization Platform"
CAPABILITY = "CAP-PLT-QC-001"
PRINCIPLE = "MEOS Quantum Civilization Intelligence Platform SHALL provide the collective cognitive infrastructure enabling shared knowledge, collaborative intelligence and continuous evolution across enterprise ecosystems."
FABRIC = "meos_quantum_civilization_intelligence_fabric"
QGI_GATE = "P215-V"
EVOLUTION_GATE = "P215-U"
OS_GATE = "P215-T"
TRUST_GATE = "P215-K"
CORE_DOMAIN = "enterprise_collective_quantum_intelligence_management"
SUPPORTING_DOMAINS = (
    {"id": "civilization_intelligence", "purpose": "Civilization-scale intelligence coordination."},
    {"id": "collective_knowledge", "purpose": "Shared knowledge assets and contributions."},
    {"id": "cognitive_network", "purpose": "Intelligence connectivity and collaboration."},
    {"id": "intelligence_exchange", "purpose": "Governed knowledge and insight exchange."},
    {"id": "multi_agent_society", "purpose": "Agent societies and cooperation."},
    {"id": "global_knowledge_governance", "purpose": "Knowledge civilization governance under P215-K."},
    {"id": "collective_decision", "purpose": "Consensus and multi-agent decisions via P213."},
    {"id": "future_intelligence_evolution", "purpose": "Civilization capability growth and milestones."},
    {"id": "quantum_collaboration", "purpose": "Human-AI-quantum collaborative networks."},
)
GENERIC_DOMAINS = ("identity", "security", "observability", "policy", "workflow", "audit", "search")
LOGICAL_BOUNDED_CONTEXTS = (
    {"id": "quantum_civilization_intelligence_core", "bc": "BC-01", "name": "Quantum Civilization Intelligence Core Context", "owns": "QuantumCivilizationIntelligenceAggregate", "purpose": "Civilization intelligence coordination, collective reasoning, synchronization."},
    {"id": "collective_intelligence_network", "bc": "BC-02", "name": "Collective Intelligence Network Context", "owns": "CollectiveNetworkAggregate", "purpose": "Intelligence connectivity, knowledge exchange, collaboration."},
    {"id": "global_cognitive_ecosystem", "bc": "BC-03", "name": "Global Cognitive Ecosystem Context", "owns": "CognitiveEcosystemAggregate", "purpose": "Cognitive ecosystem management, communities, agent collaboration."},
    {"id": "knowledge_civilization", "bc": "BC-04", "name": "Knowledge Civilization Context", "owns": "KnowledgeCivilizationAggregate", "purpose": "Knowledge preservation, evolution, distribution."},
    {"id": "collective_decision_intelligence", "bc": "BC-05", "name": "Collective Decision Intelligence Context", "owns": "CollectiveDecisionAggregate", "purpose": "Multi-intelligence decisions, consensus, strategic collaboration."},
    {"id": "future_intelligence_evolution", "bc": "BC-06", "name": "Future Intelligence Evolution Context", "owns": "FutureEvolutionAggregate", "purpose": "Civilization intelligence growth, capability discovery, evolution planning."},
)
AGGREGATES = (
    {"name": "EnterpriseQuantumCivilizationIntelligenceAggregate", "root": "QuantumCivilizationNode", "entities": ("QuantumCivilizationNode", "CollectiveIntelligenceNetwork", "KnowledgeCommunity", "CognitiveAgentSociety", "SharedKnowledgeAsset", "CollectiveDecision", "IntelligenceExchange", "EvolutionMilestone", "CivilizationCapability"), "value_objects": ("CollectiveIntelligenceScore", "KnowledgeContributionScore", "CollaborationIndex", "CognitiveNetworkHealth", "EvolutionLevel", "CivilizationReadinessScore"), "events": ("CollectiveIntelligenceCreatedEvent", "KnowledgeContributionRegisteredEvent", "CognitiveNetworkExpandedEvent", "CollectiveDecisionGeneratedEvent", "CivilizationCapabilityEvolvedEvent", "FutureIntelligenceMilestoneReachedEvent")},
    {"name": "QuantumCivilizationIntelligenceAggregate", "root": "QuantumCivilizationNode", "entities": ("CivilizationBrainSession", "CollectiveReasoningTrace"), "value_objects": ("CollectiveIntelligenceScore", "CivilizationReadinessScore"), "events": ("CollectiveIntelligenceCreatedEvent",)},
    {"name": "CollectiveNetworkAggregate", "root": "CollectiveIntelligenceNetwork", "entities": ("NetworkEdge", "ExchangeChannel"), "value_objects": ("CognitiveNetworkHealth", "CollaborationIndex"), "events": ("IntelligenceNodeConnectedEvent", "CognitiveNetworkExpandedEvent")},
    {"name": "CognitiveEcosystemAggregate", "root": "KnowledgeCommunity", "entities": ("CommunityNode", "DomainCluster"), "value_objects": ("CollaborationIndex", "CollectiveIntelligenceScore"), "events": ("CognitiveNetworkExpandedEvent",)},
    {"name": "KnowledgeCivilizationAggregate", "root": "SharedKnowledgeAsset", "entities": ("ContributionRecord", "KnowledgeDistribution"), "value_objects": ("KnowledgeContributionScore", "EvolutionLevel"), "events": ("KnowledgeSharedEvent", "KnowledgeContributionRegisteredEvent")},
    {"name": "CollectiveDecisionAggregate", "root": "CollectiveDecision", "entities": ("ConsensusRound", "ScenarioEvaluation"), "value_objects": ("CollectiveIntelligenceScore", "CollaborationIndex"), "events": ("CollectiveDecisionCreatedEvent", "CollectiveDecisionGeneratedEvent")},
    {"name": "FutureEvolutionAggregate", "root": "EvolutionMilestone", "entities": ("CapabilityDelta", "ForecastScenario"), "value_objects": ("EvolutionLevel", "CivilizationReadinessScore"), "events": ("CivilizationCapabilityEvolvedEvent", "FutureMilestoneReachedEvent", "FutureIntelligenceMilestoneReachedEvent")},
)
DOMAIN_SERVICES = (
    {"id": "quantum_civilization_intelligence_service", "responsibility": "coordinate civilization-scale collective reasoning", "inputs": ("civilization_request",), "outputs": ("node_ref",), "rules": ("via_p215_v", "via_p215_u", "module_local_llm_forbidden"), "events": ("CollectiveIntelligenceCreatedEvent",)},
    {"id": "collective_network_service", "responsibility": "connect intelligence nodes and exchange channels", "inputs": ("network_spec",), "outputs": ("network_ref",), "rules": ("ungoverned_cross_tenant_intelligence_federation_forbidden", "via_p215_t"), "events": ("IntelligenceNodeConnectedEvent",)},
    {"id": "cognitive_ecosystem_service", "responsibility": "manage cognitive communities and ecosystems", "inputs": ("ecosystem_spec",), "outputs": ("ecosystem_ref",), "rules": ("via_p215_v", "via_p215_q"), "events": ("CognitiveNetworkExpandedEvent",)},
    {"id": "knowledge_civilization_service", "responsibility": "preserve and distribute shared knowledge refs", "inputs": ("contribution_spec",), "outputs": ("asset_ref",), "rules": ("via_p214_g", "document_id_refs_only"), "events": ("KnowledgeSharedEvent",)},
    {"id": "agent_society_service", "responsibility": "govern multi-agent civilization societies", "inputs": ("society_spec",), "outputs": ("society_ref",), "rules": ("via_p215_v", "via_p215_k"), "events": ("CognitiveNetworkExpandedEvent",)},
    {"id": "collective_decision_service", "responsibility": "form consensus decisions via P213", "inputs": ("decision_context",), "outputs": ("decision_ref",), "rules": ("via_p213", "via_workflow", "opaque_collective_decisions_forbidden"), "events": ("CollectiveDecisionCreatedEvent",)},
    {"id": "evolution_intelligence_service", "responsibility": "track civilization capability milestones", "inputs": ("evolution_spec",), "outputs": ("milestone_ref",), "rules": ("via_p215_u", "via_p215_k"), "events": ("CivilizationCapabilityEvolvedEvent",)},
)
CORE_EVENTS = (
    {"name": "IntelligenceNodeConnectedEvent", "producer": "collective_intelligence_network", "consumers": "ecosystem,twin,audit"},
    {"name": "KnowledgeSharedEvent", "producer": "knowledge_civilization", "consumers": "kg,search,p214_g"},
    {"name": "CollectiveDecisionCreatedEvent", "producer": "collective_decision_intelligence", "consumers": "p213,workflow,audit,p215_k"},
    {"name": "CognitiveNetworkExpandedEvent", "producer": "global_cognitive_ecosystem", "consumers": "network,twin"},
    {"name": "CivilizationCapabilityEvolvedEvent", "producer": "future_intelligence_evolution", "consumers": "strategy,board,p215_v"},
    {"name": "FutureMilestoneReachedEvent", "producer": "future_intelligence_evolution", "consumers": "notifications,strategy,p215_k"},
)
CIVILIZATION_CORE = {"present_required": True, "capabilities": ("collective_reasoning", "knowledge_synthesis", "cross_domain_intelligence", "civilization_memory", "strategic_intelligence_coordination", "collective_problem_solving"), "via_p215_v": True, "via_p215_u": True, "module_local_llm_forbidden": True}
COLLECTIVE_NETWORK = {"present_required": True, "connects": ("quantum_ai_systems", "autonomous_agents", "enterprise_systems", "research_intelligence", "knowledge_networks", "human_experts"), "capabilities": ("intelligence_sharing", "collective_learning", "distributed_reasoning", "knowledge_collaboration"), "ungoverned_cross_tenant_intelligence_federation_forbidden": True, "via_p215_t": True}
COGNITIVE_ECOSYSTEM = {"present_required": True, "manages": ("cognitive_communities", "ai_agent_communities", "research_networks", "enterprise_intelligence_nodes", "knowledge_domains"), "capabilities": ("collaboration", "knowledge_exchange", "collective_innovation", "intelligence_growth"), "via_p215_v": True, "via_p215_q": True}
KNOWLEDGE_CIVILIZATION = {"present_required": True, "manages": ("universal_enterprise_knowledge", "historical_intelligence", "scientific_knowledge", "strategic_knowledge", "operational_experience"), "capabilities": ("knowledge_preservation", "knowledge_evolution", "knowledge_discovery", "knowledge_distribution"), "document_id_refs_only": True, "via_p214_g": True}
AGENT_SOCIETY = {"present_required": True, "manages": ("business_agents", "research_agents", "scientific_agents", "security_agents", "executive_agents", "autonomous_intelligence_agents"), "capabilities": ("agent_cooperation", "agent_negotiation", "agent_learning", "agent_governance", "collective_intelligence_formation"), "via_p215_v": True, "via_p215_u": True, "via_p215_k": True}
COLLECTIVE_DECISION = {"present_required": True, "capabilities": ("consensus_intelligence", "multi_agent_reasoning", "scenario_evaluation", "strategic_decision_formation", "collective_recommendation_generation"), "via_p213": True, "via_workflow": True, "opaque_collective_decisions_forbidden": True}
FUTURE_EVOLUTION = {"present_required": True, "capabilities": ("civilization_intelligence_growth", "future_capability_discovery", "evolution_planning"), "via_p215_u": True, "via_p215_k": True, "via_p215_r": True}
CONTEXT_MAP = (
    {"from": "quantum_civilization_intelligence_core", "to": "quantum_qgi", "type": "conformist", "via": "P215-V"},
    {"from": "quantum_civilization_intelligence_core", "to": "quantum_evolution", "type": "conformist", "via": "P215-U"},
    {"from": "collective_intelligence_network", "to": "quantum_os", "type": "customer_supplier", "via": "P215-T"},
    {"from": "collective_decision_intelligence", "to": "decision_intelligence", "type": "anti_corruption_layer", "via": "P213"},
    {"from": "knowledge_civilization", "to": "knowledge_rag", "type": "customer_supplier", "via": "P214-G"},
    {"from": "multi_agent_society", "to": "quantum_governance_ethics", "type": "conformist", "via": "P215-K"},
    {"from": "future_intelligence_evolution", "to": "quantum_strategy", "type": "customer_supplier", "via": "P215-R"},
    {"from": "global_cognitive_ecosystem", "to": "quantum_research", "type": "customer_supplier", "via": "P215-Q"},
)
MICROSERVICES = (
    {"id": "quantum_civilization_intelligence_service", "bc": "BC-01", "aggregate": "QuantumCivilizationIntelligenceAggregate", "api": "/quantum/civilization", "db": "quantum_*", "events": ("CollectiveIntelligenceCreatedEvent",), "security": ("quantum.read",), "scaling": "civilization_replicas"},
    {"id": "collective_network_service", "bc": "BC-02", "aggregate": "CollectiveNetworkAggregate", "api": "/quantum/civilization/network", "db": "quantum_*", "events": ("IntelligenceNodeConnectedEvent",), "security": ("quantum.write",), "scaling": "network_workers"},
    {"id": "cognitive_ecosystem_service", "bc": "BC-03", "aggregate": "CognitiveEcosystemAggregate", "api": "/quantum/civilization/ecosystem", "db": "quantum_*", "events": ("CognitiveNetworkExpandedEvent",), "security": ("quantum.read",), "scaling": "ecosystem_replicas"},
    {"id": "knowledge_civilization_service", "bc": "BC-04", "aggregate": "KnowledgeCivilizationAggregate", "api": "/quantum/civilization/knowledge", "db": "quantum_*", "events": ("KnowledgeSharedEvent",), "security": ("quantum.write",), "scaling": "knowledge_workers"},
    {"id": "agent_society_service", "bc": "agents", "aggregate": "EnterpriseQuantumCivilizationIntelligenceAggregate", "api": "/quantum/civilization/agents", "db": "quantum_*", "events": ("CognitiveNetworkExpandedEvent",), "security": ("quantum.write",), "scaling": "agent_workers"},
    {"id": "collective_decision_service", "bc": "BC-05", "aggregate": "CollectiveDecisionAggregate", "api": "/quantum/civilization/decisions", "db": "quantum_*", "events": ("CollectiveDecisionCreatedEvent",), "security": ("quantum.write",), "scaling": "decision_workers"},
    {"id": "evolution_intelligence_service", "bc": "BC-06", "aggregate": "FutureEvolutionAggregate", "api": "/quantum/civilization/evolution", "db": "quantum_*", "events": ("CivilizationCapabilityEvolvedEvent",), "security": ("quantum.read",), "scaling": "evolution_replicas"},
    {"id": "civilization_knowledge_graph_service", "bc": "kg", "aggregate": "EnterpriseQuantumCivilizationIntelligenceAggregate", "api": "/quantum/civilization/knowledge-graph", "db": "quantum_*", "events": ("KnowledgeSharedEvent",), "security": ("quantum.read",), "scaling": "kg_replicas"},
    {"id": "civilization_digital_twin_service", "bc": "twin", "aggregate": "EnterpriseQuantumCivilizationIntelligenceAggregate", "api": "/quantum/civilization/digital-twin", "db": "quantum_*", "events": ("FutureMilestoneReachedEvent",), "security": ("quantum.read",), "scaling": "twin_replicas"},
)
KNOWLEDGE_GRAPH = {"present_required": True, "nodes": ("intelligence_entities", "knowledge_assets", "agents", "communities", "decisions", "discoveries", "capabilities"), "relationships": ("collaborates_with", "learns_from", "contributes_to", "influences", "evolves", "creates")}
DIGITAL_TWIN = {"present_required": True, "represents": ("collective_intelligence_state", "knowledge_evolution_state", "agent_ecosystem_state", "collaboration_network", "future_scenarios"), "enables": ("civilization_simulation", "evolution_forecasting", "collective_optimization"), "via_p215_l": True, "via_p215_v": True}
COMMANDS = ("CreateIntelligenceNetworkCommand", "RegisterKnowledgeContributionCommand", "CreateCollectiveDecisionCommand", "ConnectCognitiveNodeCommand", "TriggerCivilizationEvolutionCommand")
QUERIES = ("GetCollectiveIntelligenceStateQuery", "GetKnowledgeNetworkQuery", "GetAgentCommunityQuery", "GetCivilizationCapabilityQuery", "GetEvolutionForecastQuery")
API_SURFACES = ("/api/v1/quantum/civilization", "/api/v1/quantum/civilization/network", "/api/v1/quantum/civilization/ecosystem", "/api/v1/quantum/civilization/knowledge", "/api/v1/quantum/civilization/agents", "/api/v1/quantum/civilization/decisions", "/api/v1/quantum/civilization/evolution", "/api/v1/quantum/civilization/knowledge-graph", "/api/v1/quantum/civilization/digital-twin")
API_STYLES = ("REST", "GraphQL", "gRPC", "Streaming", "Event")
SECURITY = {"present_required": True, "zero_trust_civilization_intelligence": True, "human_ai_quantum_collaboration": True, "via_p215_v": True, "via_p215_u": True, "via_p215_t": True, "via_p215_k": True, "via_p213": True, "via_policy_engine": True, "via_workflow": True, "via_audit": True, "never_replace_p215_v": True, "never_replace_p215_u": True, "never_replace_p215_t": True, "never_replace_core_platform": True, "never_replace_p215_k": True, "module_local_llm_forbidden": True, "ungoverned_cross_tenant_intelligence_federation_forbidden": True, "opaque_collective_decisions_forbidden": True, "controls": ("civilization_authz", "tenant_isolated_federation", "explainable_collective_decision", "responsible_collective_ai_gate")}
DEPLOYMENT = {"present_required": True, "cloud_native": True, "components": ("quantum_intelligence_infrastructure", "cognitive_network_platform", "agent_ecosystem_runtime", "knowledge_graph_database", "civilization_digital_twin", "ai_compute_infrastructure", "security_infrastructure", "governance_layer", "observability_platform")}
TESTING = ("collective_intelligence_testing", "knowledge_exchange_testing", "agent_collaboration_testing", "decision_quality_testing", "network_resilience_testing", "security_testing", "governance_testing", "evolution_simulation_testing", "performance_testing")
CURSOR_OUTPUTS = ("civilization_vision", "ddd_domain_model", "domain_architecture", "civilization_core", "collective_network", "cognitive_ecosystem", "knowledge_civilization", "agent_society", "collective_decision", "knowledge_graph", "digital_twin", "cqrs", "event_sourcing", "microservices", "integration", "deployment", "testing", "quality_gates_dod", "adr_468", "enterprise_quantum_civilization_law")
QUALITY_GATES_REJECT_IF = ("quantum_civilization_intelligence_layer_is_missing", "collective_intelligence_network_is_missing", "global_cognitive_ecosystem_is_missing", "knowledge_civilization_platform_is_missing", "multi_agent_intelligence_society_is_missing", "collective_decision_intelligence_is_missing", "future_intelligence_evolution_is_missing", "knowledge_graph_integration_is_missing", "digital_twin_integration_is_missing", "cqrs_architecture_is_missing", "event_architecture_is_missing", "microservices_architecture_is_missing", "api_first_architecture_is_missing", "cloud_native_deployment_is_missing", "sibling_quantum_bc", "replace_p215_v_qgi_fabric", "replace_p215_u_evolution_fabric", "replace_p215_t_control_plane", "replace_core_platform", "replace_p215_k_trust_gate", "module_local_llm", "ungoverned_cross_tenant_intelligence_federation", "opaque_collective_decisions")

def vision() -> dict[str, Any]:
    return {"role": "MEOS Quantum Civilization Intelligence Fabric", "principle": PRINCIPLE, "equation": "Individual Intelligence -> AI Intelligence -> Quantum General Intelligence -> Collective Intelligence -> Civilization Knowledge Network -> Future Intelligence Ecosystem", "why": ("enterprises_require_collective_intelligence", "isolated_systems_cannot_solve_global_complexity", "knowledge_sharing_needs_intelligent_networks", "collective_reasoning_is_strategic", "meos_needs_civilization_scale_layer"), "builds_on_p215_a": True, "builds_on_p215_v": True, "builds_on_p215_u": True, "via_p213": True, "governed_by_p215_k": True, "never_replace_p215_v": True, "never_replace_p215_u": True, "never_replace_p215_t": True, "never_replace_core_platform": True, "never_replace_p215_k": True, "qgi_gate": QGI_GATE, "evolution_gate": EVOLUTION_GATE, "os_gate": OS_GATE, "trust_gate": TRUST_GATE}

def domain_model() -> dict[str, Any]:
    return {"core_domain": CORE_DOMAIN, "supporting_domains": [dict(d) for d in SUPPORTING_DOMAINS], "supporting_count": len(SUPPORTING_DOMAINS), "generic_domains": list(GENERIC_DOMAINS)}

def bounded_contexts() -> dict[str, Any]:
    return {"contexts": [dict(c) for c in LOGICAL_BOUNDED_CONTEXTS], "context_count": len(LOGICAL_BOUNDED_CONTEXTS)}

def aggregates() -> dict[str, Any]:
    return {"aggregates": [dict(a) for a in AGGREGATES], "aggregate_count": len(AGGREGATES)}

def domain_services() -> dict[str, Any]:
    return {"services": [dict(s) for s in DOMAIN_SERVICES], "service_count": len(DOMAIN_SERVICES)}

def events() -> dict[str, Any]:
    return {"core_events": [dict(e) for e in CORE_EVENTS], "core_event_count": len(CORE_EVENTS), "version_strategy": "event_version_field", "retention_policy": "tenant_scoped_immutable_append"}

def civilization_core() -> dict[str, Any]:
    return dict(CIVILIZATION_CORE)

def collective_network() -> dict[str, Any]:
    return dict(COLLECTIVE_NETWORK)

def cognitive_ecosystem() -> dict[str, Any]:
    return dict(COGNITIVE_ECOSYSTEM)

def knowledge_civilization() -> dict[str, Any]:
    return dict(KNOWLEDGE_CIVILIZATION)

def agent_society() -> dict[str, Any]:
    return dict(AGENT_SOCIETY)

def collective_decision() -> dict[str, Any]:
    return dict(COLLECTIVE_DECISION)

def future_evolution() -> dict[str, Any]:
    return dict(FUTURE_EVOLUTION)

def context_map() -> dict[str, Any]:
    return {"relationships": [dict(r) for r in CONTEXT_MAP], "relationship_count": len(CONTEXT_MAP)}

def microservices() -> dict[str, Any]:
    return {"services": [dict(s) for s in MICROSERVICES], "service_count": len(MICROSERVICES)}

def knowledge_graph() -> dict[str, Any]:
    return dict(KNOWLEDGE_GRAPH)

def digital_twin() -> dict[str, Any]:
    return dict(DIGITAL_TWIN)

def cqrs() -> dict[str, Any]:
    return {"commands": list(COMMANDS), "command_count": len(COMMANDS), "queries": list(QUERIES), "query_count": len(QUERIES)}

def api() -> dict[str, Any]:
    return {"surfaces": list(API_SURFACES), "styles": list(API_STYLES), "api_first_present_required": True, "qgi_gate_api": "/api/v1/quantum/qgi"}

def integrations() -> dict[str, Any]:
    return {"peers": ("P215-A", "P215-T", "P215-U", "P215-V", "P215-R", "P215-S", "P215-Q", "P215-K", "P215-H", "P213", "P214-G", "Policy Engine", "Workflow", "Audit Platform", "Observability"), "via_events_and_acl": True, "contracts": ("collective_intelligence_apis", "knowledge_exchange_protocols", "agent_communication_standards", "civilization_events", "intelligence_federation_contracts"), "never_replace_p215_v": True, "ungoverned_cross_tenant_intelligence_federation_forbidden": True}

def security() -> dict[str, Any]:
    return dict(SECURITY)

def deployment() -> dict[str, Any]:
    return dict(DEPLOYMENT)

def testing() -> dict[str, Any]:
    return {"suites": list(TESTING), "suite_count": len(TESTING)}

def cursor_outputs() -> dict[str, Any]:
    return {"outputs": list(CURSOR_OUTPUTS), "count": len(CURSOR_OUTPUTS)}

def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF), "count": len(QUALITY_GATES_REJECT_IF)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE"}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "principle": PRINCIPLE, "fabric": FABRIC, "qgi_gate": QGI_GATE, "evolution_gate": EVOLUTION_GATE, "os_gate": OS_GATE, "trust_gate": TRUST_GATE,
        "builds_on": ["P215-A", "P215-B", "P215-C", "P215-D", "P215-E", "P215-F", "P215-G", "P215-H", "P215-I", "P215-J", "P215-K", "P215-L", "P215-M", "P215-N", "P215-O", "P215-P", "P215-Q", "P215-R", "P215-S", "P215-T", "P215-U", "P215-V", "P213", "P214-G", "ADR-465", "ADR-466", "ADR-467", "ADR-403", "ADR-454"],
        "vision": vision(), "domain_model": domain_model(), "bounded_contexts": bounded_contexts(),
        "aggregates": aggregates(), "domain_services": domain_services(), "events": events(),
        "civilization_core": civilization_core(), "collective_network": collective_network(),
        "cognitive_ecosystem": cognitive_ecosystem(), "knowledge_civilization": knowledge_civilization(),
        "agent_society": agent_society(), "collective_decision": collective_decision(),
        "future_evolution": future_evolution(),
        "context_map": context_map(), "microservices": microservices(), "knowledge_graph": knowledge_graph(),
        "digital_twin": digital_twin(), "cqrs": cqrs(), "api": api(), "integrations": integrations(),
        "security": security(), "deployment": deployment(), "testing": testing(),
        "cursor_outputs": cursor_outputs(), "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "quantum_civilization_intelligence_layer_present_required": True,
        "collective_intelligence_network_present_required": True,
        "global_cognitive_ecosystem_present_required": True,
        "knowledge_civilization_platform_present_required": True,
        "multi_agent_intelligence_society_present_required": True,
        "collective_decision_intelligence_present_required": True,
        "future_intelligence_evolution_present_required": True,
        "knowledge_graph_integration_present_required": True,
        "digital_twin_integration_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "api_first_architecture_present_required": True,
        "cloud_native_deployment_present_required": True,
        "sibling_quantum_bc_forbidden": True,
        "never_replace_p215_v": True,
        "never_replace_p215_u": True,
        "never_replace_p215_t": True,
        "never_replace_core_platform": True,
        "never_replace_p215_k": True,
        "ungoverned_cross_tenant_intelligence_federation_forbidden": True,
        "opaque_collective_decisions_forbidden": True,
        "builds_on_p215_a": True, "builds_on_p215_v": True, "builds_on_p215_u": True,
        "via_p215_v": True, "via_p215_u": True, "via_p215_t": True, "via_p213": True, "via_p214_g": True,
        "via_p215_k": True, "via_policy_engine": True, "via_workflow": True, "via_audit": True,
        "governed_by_p215_k": True,
        "api_prefix": f"{API_PREFIX}/civilization",
        "forbidden_sibling_bc": [
            "quantum_civilization_platform",
            "quantum_collective_intelligence_platform",
            "quantum_cognitive_ecosystem_platform",
            "quantum_knowledge_civilization_platform",
            "quantum_agent_society_platform",
        ],
    }

def civilization_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /quantum/civilization",
        "GET /quantum/civilization/network",
        "GET /quantum/civilization/ecosystem",
        "GET /quantum/civilization/knowledge",
        "GET /quantum/civilization/agents",
        "GET /quantum/civilization/decisions",
        "GET /quantum/civilization/evolution",
        "GET /quantum/civilization/knowledge-graph",
        "GET /quantum/civilization/digital-twin",
        "GET /quantum/civilization/readiness",
    ], "qgi_gate_routes": ["GET /quantum/qgi", "GET /quantum/qgi/readiness"]}
