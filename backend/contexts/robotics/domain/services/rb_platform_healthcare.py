"""P216-I Enterprise Healthcare Robotics — immutable catalog."""
from __future__ import annotations
from typing import Any

PROMPT_ID = "P216-I"
ADR = 481
SOR = "robotics"
API_PREFIX = "/api/v1/robotics"
PRODUCT = (
    "Enterprise Robotics Healthcare Robotics, Medical AI, "
    "Surgical Robotics & Digital Healthcare Automation Platform"
)
CAPABILITY = "CAP-PLT-RB-001"
HEALTHCARE_VISION = (
    "MEOS Healthcare Robotics Platform SHALL unify clinical robots, medical AI, "
    "surgical robotics and hospital automation as intelligent participants within "
    "the MEOS Healthcare Intelligence Ecosystem."
)
MISSION = (
    "Create a safe, AI-native, patient-centric, autonomous healthcare ecosystem "
    "that augments clinicians, improves outcomes and automates healthcare operations."
)
VISION = (
    "Every healthcare robot, clinical AI system, medical device and healthcare "
    "workflow shall operate as an intelligent participant inside the MEOS "
    "Healthcare Intelligence Ecosystem."
)
FABRIC = "meos_healthcare_robotics_fabric"
FOUNDATION_GATE = "P216"
MISSION_GATE = "P216-A"
STRATEGY_GATE = "P216-B"
DOMAIN_GATE = "P216-C"
RUNTIME_GATE = "P216-D"
PHYSICAL_AI_GATE = "P216-E"
INDUSTRIAL_GATE = "P216-F"
LOGISTICS_GATE = "P216-G"
MOBILITY_GATE = "P216-H"
SUPREME_GATE = "P215-Z"
AI_GATE = "P214-Z"
CORE_DOMAIN = "enterprise_healthcare_intelligence"
AGGREGATE = "HealthcareRoboticsAggregate"

SUPPORTING_DOMAINS = (
    "patient_care",
    "clinical_operations",
    "medical_robotics",
    "surgical_robotics",
    "medical_imaging",
    "laboratory_automation",
    "pharmacy_automation",
    "clinical_decision_support",
    "hospital_logistics",
    "telemedicine",
    "rehabilitation_robotics",
    "healthcare_digital_twin",
    "medical_device_management",
    "infection_control",
)
ENTITIES = (
    "Patient",
    "Clinician",
    "Hospital",
    "MedicalRobot",
    "SurgicalRobot",
    "MedicalDevice",
    "ClinicalEncounter",
    "TreatmentPlan",
    "MedicalImage",
    "LaboratoryOrder",
    "MedicationOrder",
    "OperatingRoom",
    "PatientDigitalTwin",
    "ClinicalWorkflow",
)
VALUE_OBJECTS = (
    "PatientIdentifier",
    "ClinicalPriority",
    "DiagnosisCode",
    "ProcedureCode",
    "VitalSigns",
    "MedicationDose",
    "RobotCapability",
    "ImagingResult",
    "RiskScore",
    "ConsentStatus",
    "SafetyClassification",
)
BOUNDED_CONTEXTS = (
    {"id": "BC-01", "name": "Patient Care Context", "responsibilities": ("patient_lifecycle", "admissions", "care_coordination", "discharge")},
    {"id": "BC-02", "name": "Medical AI Context", "responsibilities": ("ai_diagnosis", "clinical_recommendations", "risk_prediction", "decision_support")},
    {"id": "BC-03", "name": "Healthcare Robotics Context", "responsibilities": ("service_robots", "patient_assistance", "clinical_logistics", "care_automation")},
    {"id": "BC-04", "name": "Surgical Robotics Context", "responsibilities": ("surgical_planning", "robot_assisted_surgery", "procedure_execution", "surgical_telemetry")},
    {"id": "BC-05", "name": "Medical Imaging Context", "responsibilities": ("imaging_workflows", "ai_image_analysis", "diagnostic_interpretation")},
    {"id": "BC-06", "name": "Laboratory & Pharmacy Context", "responsibilities": ("laboratory_automation", "specimen_handling", "pharmacy_robotics", "medication_management")},
    {"id": "BC-07", "name": "Healthcare Digital Twin Context", "responsibilities": ("patient_modelling", "clinical_simulation", "predictive_care", "treatment_optimisation")},
    {"id": "BC-08", "name": "Clinical Governance Context", "responsibilities": ("compliance", "clinical_quality", "safety_monitoring", "audit")},
)
HEALTHCARE_ROBOTICS = {
    "present_required": True,
    "platform": "meos_healthcare_robotics_platform",
    "components": (
        "hospital_robot_registry",
        "clinical_robot_controller",
        "patient_assistance_manager",
        "medication_delivery_robots",
        "disinfection_robot_manager",
        "laboratory_robot_manager",
        "clinical_workflow_engine",
        "hospital_operations_dashboard",
    ),
    "capabilities": (
        "autonomous_patient_transport",
        "medication_delivery",
        "ward_logistics",
        "laboratory_automation",
        "hospital_asset_transport",
        "disinfection_automation",
        "clinical_assistance",
    ),
}
MEDICAL_AI = {
    "present_required": True,
    "engine": "meos_medical_ai_engine",
    "capabilities": (
        "ai_assisted_diagnosis",
        "clinical_decision_support",
        "medical_image_analysis",
        "predictive_medicine",
        "disease_progression_modelling",
        "personalised_treatment_recommendations",
        "population_health_analytics",
        "clinical_documentation_assistance",
    ),
    "models": (
        "medical_foundation_models",
        "vision_models",
        "clinical_language_models",
        "predictive_models",
        "knowledge_reasoning_models",
    ),
    "via_p214_z": True,
    "explainable_ai": True,
    "responsible_ai": True,
    "human_in_the_loop_required": True,
}
SURGICAL_ROBOTICS = {
    "present_required": True,
    "platform": "meos_surgical_intelligence_platform",
    "capabilities": (
        "pre_operative_planning",
        "procedure_simulation",
        "robot_assisted_surgery",
        "instrument_guidance",
        "intra_operative_monitoring",
        "ai_assisted_navigation",
        "post_operative_analytics",
        "digital_surgical_replay",
    ),
    "human_in_the_loop_required": True,
}
DIGITAL_HEALTHCARE_AUTOMATION = {
    "present_required": True,
    "platform": "meos_healthcare_automation_platform",
    "capabilities": (
        "patient_admission_automation",
        "clinical_workflow_automation",
        "appointment_orchestration",
        "bed_management",
        "resource_allocation",
        "clinical_task_routing",
        "discharge_automation",
        "hospital_command_centre",
    ),
}
CLINICAL_DECISION = {
    "present_required": True,
    "platform": "meos_clinical_decision_intelligence",
    "capabilities": (
        "decision_support",
        "risk_scoring",
        "evidence_based_recommendations",
        "guideline_alignment",
    ),
    "via_p214_z": True,
    "human_in_the_loop_required": True,
}
HEALTHCARE_DIGITAL_TWIN = {
    "present_required": True,
    "platform": "meos_healthcare_digital_twin_platform",
    "represents": (
        "patients", "hospitals", "departments", "medical_devices", "robots",
        "clinical_workflows", "operating_rooms", "medical_assets", "laboratories",
    ),
    "capabilities": (
        "patient_simulation",
        "treatment_simulation",
        "capacity_planning",
        "clinical_optimisation",
        "predictive_care",
        "operational_forecasting",
    ),
}
MEDICAL_KG = {
    "present_required": True,
    "graph": "meos_medical_knowledge_graph",
    "nodes": (
        "patients", "clinicians", "diseases", "symptoms", "diagnoses", "procedures",
        "medications", "medical_devices", "hospitals", "robots", "laboratories", "clinical_guidelines",
    ),
    "relationships": (
        "diagnosed_with", "treated_by", "prescribed", "operated_by", "monitored_by",
        "associated_with", "guided_by", "depends_on", "references", "supports",
    ),
    "enables": (
        "clinical_reasoning",
        "evidence_based_care",
        "decision_intelligence",
        "medical_semantic_search",
    ),
}
OBSERVABILITY = {
    "present_required": True,
    "platform": "meos_healthcare_operations_intelligence_platform",
    "monitors": (
        "patient_safety",
        "clinical_workflows",
        "robot_health",
        "medical_device_health",
        "ai_model_accuracy",
        "hospital_capacity",
        "procedure_outcomes",
        "medication_safety",
        "clinical_kpis",
    ),
    "via_platform_observability": True,
}
SECURITY = {
    "present_required": True,
    "framework": "meos_healthcare_zero_trust_framework",
    "domains": (
        "patient_identity",
        "clinician_identity",
        "medical_device_identity",
        "robot_identity",
        "clinical_authorization",
        "consent_management",
        "data_encryption",
        "medical_api_security",
        "operational_safety",
        "threat_detection",
    ),
    "compliance": (
        "HIPAA", "GDPR", "ISO_13485", "ISO_14971", "IEC_62304", "FHIR_Security",
    ),
    "zero_trust": True,
    "privacy_by_design": True,
    "via_identity": True,
    "via_policy_engine": True,
    "via_workflow": True,
    "via_audit": True,
    "via_integration_platform": True,
    "fhir_hl7_dicom_via_integration_platform_only": True,
    "never_direct_fhir_hl7_dicom_bypass": True,
    "never_duplicate_hospital_clinic_core_logic": True,
    "no_module_local_llm": True,
    "medical_ai_via_p214z_acl_only": True,
    "physical_ai_via_p214z_acl_only": True,
    "human_in_the_loop_required_for_clinical_autonomy": True,
    "never_replace_p216_foundation": True,
    "never_replace_p216_h_mobility": True,
    "never_replace_core_platform": True,
    "never_replace_ai_platform": True,
    "never_replace_p215_z": True,
    "ungated_physical_autonomy_strategy_forbidden": True,
    "opaque_safety_strategy_forbidden": True,
}
COMMANDS = (
    "RegisterPatientCommand",
    "CreateTreatmentPlanCommand",
    "AssignMedicalRobotCommand",
    "StartSurgicalProcedureCommand",
    "DispenseMedicationCommand",
    "GenerateDiagnosisCommand",
    "UpdatePatientDigitalTwinCommand",
)
QUERIES = (
    "GetPatientRecordQuery",
    "GetClinicalStatusQuery",
    "GetRobotStatusQuery",
    "GetProcedureStatusQuery",
    "GetMedicalImageQuery",
    "GetPatientDigitalTwinQuery",
)
CORE_EVENTS = (
    {"name": "PatientAdmittedEvent", "schema": "robotics.healthcare.patient.admitted.v1", "owner": "BC-01", "consumers": "clinical,audit,twin"},
    {"name": "DiagnosisGeneratedEvent", "schema": "robotics.healthcare.diagnosis.generated.v1", "owner": "BC-02", "consumers": "care,audit,analytics"},
    {"name": "TreatmentPlanApprovedEvent", "schema": "robotics.healthcare.treatment.plan.approved.v1", "owner": "BC-08", "consumers": "care,robotics,audit"},
    {"name": "RobotAssignedEvent", "schema": "robotics.healthcare.robot.assigned.v1", "owner": "BC-03", "consumers": "runtime,audit,operations"},
    {"name": "SurgeryInitiatedEvent", "schema": "robotics.healthcare.surgery.initiated.v1", "owner": "BC-04", "consumers": "safety,audit,analytics"},
    {"name": "ProcedureCompletedEvent", "schema": "robotics.healthcare.procedure.completed.v1", "owner": "BC-04", "consumers": "care,twin,audit"},
    {"name": "MedicationDispensedEvent", "schema": "robotics.healthcare.medication.dispensed.v1", "owner": "BC-06", "consumers": "care,audit,pharmacy"},
    {"name": "PatientTransferredEvent", "schema": "robotics.healthcare.patient.transferred.v1", "owner": "BC-01", "consumers": "operations,twin,audit"},
    {"name": "EmergencyDetectedEvent", "schema": "robotics.healthcare.emergency.detected.v1", "owner": "BC-08", "consumers": "care,safety,audit"},
    {"name": "PatientDischargedEvent", "schema": "robotics.healthcare.patient.discharged.v1", "owner": "BC-01", "consumers": "operations,audit,analytics"},
)
MICROSERVICES = (
    {"id": "patient_service", "bc": "BC-01", "api": "/robotics/healthcare/patients", "db": "robotics_*", "events": ("PatientAdmittedEvent", "PatientDischargedEvent", "PatientTransferredEvent"), "security": ("robotics.write",), "scaling": "patient_replicas", "responsibility": "Patient care projections and lifecycle coordination"},
    {"id": "clinical_decision_service", "bc": "BC-02", "api": "/robotics/healthcare/clinical-decision", "db": "robotics_*", "events": ("DiagnosisGeneratedEvent",), "security": ("robotics.write",), "scaling": "cds_workers", "responsibility": "Clinical decision intelligence via P214-Z ACL"},
    {"id": "healthcare_robotics_service", "bc": "BC-03", "api": "/robotics/healthcare/robots", "db": "robotics_*", "events": ("RobotAssignedEvent",), "security": ("robotics.write",), "scaling": "robot_workers", "responsibility": "Hospital service and care automation robots"},
    {"id": "surgical_robotics_service", "bc": "BC-04", "api": "/robotics/healthcare/surgery", "db": "robotics_*", "events": ("SurgeryInitiatedEvent", "ProcedureCompletedEvent"), "security": ("robotics.write",), "scaling": "surgery_workers", "responsibility": "Surgical robotics planning and telemetry"},
    {"id": "medical_imaging_service", "bc": "BC-05", "api": "/robotics/healthcare/imaging", "db": "robotics_*", "events": ("DiagnosisGeneratedEvent",), "security": ("robotics.read",), "scaling": "imaging_workers", "responsibility": "Imaging workflow projections via Integration Platform"},
    {"id": "laboratory_service", "bc": "BC-06", "api": "/robotics/healthcare/laboratory", "db": "robotics_*", "events": ("MedicationDispensedEvent",), "security": ("robotics.write",), "scaling": "lab_workers", "responsibility": "Laboratory automation projections"},
    {"id": "pharmacy_service", "bc": "BC-06", "api": "/robotics/healthcare/pharmacy", "db": "robotics_*", "events": ("MedicationDispensedEvent",), "security": ("robotics.write",), "scaling": "pharmacy_workers", "responsibility": "Pharmacy robotics and medication projections"},
    {"id": "digital_twin_service", "bc": "BC-07", "api": "/robotics/healthcare/digital-twin", "db": "robotics_*", "events": ("ProcedureCompletedEvent", "PatientTransferredEvent"), "security": ("robotics.read",), "scaling": "twin_workers", "responsibility": "Healthcare digital twin sync"},
    {"id": "medical_knowledge_graph_service", "bc": "BC-02", "api": "/robotics/healthcare/knowledge-graph", "db": "robotics_*", "events": ("DiagnosisGeneratedEvent", "TreatmentPlanApprovedEvent"), "security": ("robotics.read",), "scaling": "kg_workers", "responsibility": "Medical knowledge graph projections"},
    {"id": "hospital_operations_service", "bc": "BC-01", "api": "/robotics/healthcare/operations", "db": "robotics_*", "events": ("PatientAdmittedEvent", "PatientDischargedEvent"), "security": ("robotics.write",), "scaling": "ops_workers", "responsibility": "Digital healthcare automation and hospital command centre"},
    {"id": "clinical_analytics_service", "bc": "BC-08", "api": "/robotics/healthcare/analytics", "db": "robotics_*", "events": ("ProcedureCompletedEvent", "EmergencyDetectedEvent"), "security": ("robotics.read",), "scaling": "analytics_workers", "responsibility": "Clinical analytics and governance facets"},
)
INTEGRATION = {
    "present_required": True,
    "targets": (
        "p216d_robotics_os",
        "p216e_physical_ai",
        "p216h_autonomous_mobility",
        "p214z_ai_master",
        "p215z_quantum_supreme",
        "electronic_health_records",
        "hospital_information_systems",
        "fhir_servers",
        "hl7_interfaces",
        "dicom_platforms",
        "laboratory_information_systems",
        "pharmacy_systems",
        "medical_iot_platform",
        "healthcare_digital_twin_platform",
        "integration_platform",
    ),
    "mechanisms": (
        "clinical_apis",
        "robot_mission_interfaces",
        "fhir_via_integration_connectors",
        "hl7_via_integration_connectors",
        "dicom_via_integration_connectors",
        "healthcare_event_contracts",
    ),
    "via_p216_d": True,
    "via_p216_e": True,
    "via_p216_h": True,
    "via_p214_z": True,
    "via_p215_z": True,
    "via_p213": True,
    "via_integration_platform": True,
    "never_direct_fhir_hl7_dicom_bypass": True,
    "never_duplicate_hospital_clinic_core_logic": True,
}
DEPLOYMENT = {
    "present_required": True,
    "model": "hybrid_healthcare_robotics_infrastructure",
    "includes": (
        "healthcare_cloud_platform",
        "hospital_edge_platform",
        "clinical_ai_cluster",
        "robotics_runtime_cluster",
        "digital_twin_cluster",
        "knowledge_graph_cluster",
        "medical_integration_gateway",
        "observability_platform",
        "security_operations_centre",
        "disaster_recovery_platform",
    ),
    "deployment_models": (
        "clinic",
        "hospital",
        "hospital_network",
        "regional_health_system",
        "national_healthcare_platform",
    ),
    "cloud_native": True,
    "edge_native": True,
}
TESTING = (
    "clinical_workflow_testing",
    "medical_ai_validation",
    "healthcare_robot_testing",
    "surgical_simulation_testing",
    "medical_device_integration_testing",
    "fhir_hl7_testing",
    "dicom_validation",
    "security_testing",
    "privacy_testing",
    "performance_testing",
    "resilience_testing",
    "clinical_safety_validation",
)
API_SURFACES = (
    "/api/v1/robotics/healthcare",
    "/api/v1/robotics/healthcare/vision",
    "/api/v1/robotics/healthcare/domain",
    "/api/v1/robotics/healthcare/bounded-contexts",
    "/api/v1/robotics/healthcare/robotics",
    "/api/v1/robotics/healthcare/medical-ai",
    "/api/v1/robotics/healthcare/surgical",
    "/api/v1/robotics/healthcare/automation",
    "/api/v1/robotics/healthcare/clinical-decision",
    "/api/v1/robotics/healthcare/digital-twin",
    "/api/v1/robotics/healthcare/knowledge-graph",
    "/api/v1/robotics/healthcare/observability",
    "/api/v1/robotics/healthcare/security",
    "/api/v1/robotics/healthcare/cqrs",
    "/api/v1/robotics/healthcare/events",
    "/api/v1/robotics/healthcare/microservices",
    "/api/v1/robotics/healthcare/integration",
    "/api/v1/robotics/healthcare/deployment",
    "/api/v1/robotics/healthcare/testing",
)
API_STYLES = ("REST", "GraphQL", "gRPC", "Streaming", "Event")
QUALITY_GATES_REJECT_IF = (
    "healthcare_robotics_platform_is_missing",
    "medical_ai_platform_is_missing",
    "surgical_robotics_platform_is_missing",
    "clinical_decision_intelligence_is_missing",
    "digital_healthcare_automation_platform_is_missing",
    "healthcare_digital_twin_is_missing",
    "medical_knowledge_graph_is_missing",
    "security_compliance_architecture_is_missing",
    "cqrs_architecture_is_missing",
    "event_architecture_is_missing",
    "microservices_architecture_is_missing",
    "cloud_edge_deployment_is_missing",
    "enterprise_healthcare_integration_is_missing",
    "testing_validation_architecture_is_missing",
    "sibling_robotics_bc",
    "replace_p216_h_mobility",
    "direct_fhir_hl7_dicom_bypass",
    "duplicate_hospital_clinic_core_logic",
    "module_local_llm",
)

def vision_pack() -> dict[str, Any]:
    return {
        "role": "MEOS Healthcare Robotics Fabric",
        "healthcare_vision": HEALTHCARE_VISION,
        "mission": MISSION,
        "vision": VISION,
        "builds_on_p216": True,
        "builds_on_p216_h": True,
        "builds_on_p216_g": True,
        "builds_on_p216_e": True,
        "builds_on_p216_d": True,
        "builds_on_p215_z": True,
        "builds_on_p214_z": True,
        "never_replace_p216_h_mobility": True,
        "foundation_gate": FOUNDATION_GATE,
        "mobility_gate": MOBILITY_GATE,
        "logistics_gate": LOGISTICS_GATE,
        "physical_ai_gate": PHYSICAL_AI_GATE,
        "runtime_gate": RUNTIME_GATE,
        "supreme_gate": SUPREME_GATE,
        "ai_gate": AI_GATE,
    }

def domain_model() -> dict[str, Any]:
    return {
        "present_required": True,
        "core_domain": CORE_DOMAIN,
        "aggregate": AGGREGATE,
        "supporting_domains": list(SUPPORTING_DOMAINS),
        "supporting_count": len(SUPPORTING_DOMAINS),
        "entities": list(ENTITIES),
        "entity_count": len(ENTITIES),
        "value_objects": list(VALUE_OBJECTS),
        "value_object_count": len(VALUE_OBJECTS),
    }

def bounded_contexts() -> dict[str, Any]:
    return {"present_required": True, "contexts": [dict(c) for c in BOUNDED_CONTEXTS], "context_count": len(BOUNDED_CONTEXTS)}

def robotics_platform() -> dict[str, Any]:
    return dict(HEALTHCARE_ROBOTICS)

def medical_ai() -> dict[str, Any]:
    return dict(MEDICAL_AI)

def surgical() -> dict[str, Any]:
    return dict(SURGICAL_ROBOTICS)

def automation() -> dict[str, Any]:
    return dict(DIGITAL_HEALTHCARE_AUTOMATION)

def clinical_decision() -> dict[str, Any]:
    return dict(CLINICAL_DECISION)

def digital_twin() -> dict[str, Any]:
    return dict(HEALTHCARE_DIGITAL_TWIN)

def knowledge_graph() -> dict[str, Any]:
    return dict(MEDICAL_KG)

def observability() -> dict[str, Any]:
    return dict(OBSERVABILITY)

def security() -> dict[str, Any]:
    return dict(SECURITY)

def cqrs() -> dict[str, Any]:
    return {"commands": list(COMMANDS), "command_count": len(COMMANDS), "queries": list(QUERIES), "query_count": len(QUERIES)}

def events() -> dict[str, Any]:
    return {"core_events": [dict(e) for e in CORE_EVENTS], "core_event_count": len(CORE_EVENTS)}

def microservices() -> dict[str, Any]:
    return {"services": [dict(s) for s in MICROSERVICES], "service_count": len(MICROSERVICES)}

def integration() -> dict[str, Any]:
    return dict(INTEGRATION)

def deployment() -> dict[str, Any]:
    return dict(DEPLOYMENT)

def testing() -> dict[str, Any]:
    return {"present_required": True, "suites": list(TESTING), "suite_count": len(TESTING)}

def api() -> dict[str, Any]:
    return {
        "surfaces": list(API_SURFACES),
        "styles": list(API_STYLES),
        "api_first_present_required": True,
        "mobility_gate_api": "/api/v1/robotics/mobility",
        "runtime_gate_api": "/api/v1/robotics/runtime",
    }

def quality_gates() -> dict[str, Any]:
    return {"reject_if": list(QUALITY_GATES_REJECT_IF), "count": len(QUALITY_GATES_REJECT_IF)}

def production_readiness() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "verdict": "ENTERPRISE_GRADE", "foundation_for_p216_j": True}

def catalog() -> dict[str, Any]:
    return {
        "prompt_id": PROMPT_ID, "adr": ADR, "sor": SOR, "product": PRODUCT, "capability": CAPABILITY,
        "healthcare_vision": HEALTHCARE_VISION, "mission": MISSION, "vision": VISION, "principle": HEALTHCARE_VISION,
        "fabric": FABRIC, "foundation_gate": FOUNDATION_GATE, "mission_gate": MISSION_GATE,
        "strategy_gate": STRATEGY_GATE, "domain_gate": DOMAIN_GATE, "runtime_gate": RUNTIME_GATE,
        "physical_ai_gate": PHYSICAL_AI_GATE, "industrial_gate": INDUSTRIAL_GATE,
        "logistics_gate": LOGISTICS_GATE, "mobility_gate": MOBILITY_GATE,
        "supreme_gate": SUPREME_GATE, "ai_gate": AI_GATE,
        "builds_on": [
            "P216", "P216-A", "P216-B", "P216-C", "P216-D", "P216-E", "P216-F", "P216-G", "P216-H",
            "P215-Z", "P214-Z", "P213",
            "ADR-472", "ADR-473", "ADR-474", "ADR-475", "ADR-476", "ADR-477", "ADR-478", "ADR-479", "ADR-480",
        ],
        "vision_pack": vision_pack(),
        "domain_model": domain_model(),
        "bounded_contexts": bounded_contexts(),
        "robotics_platform": robotics_platform(),
        "medical_ai": medical_ai(),
        "surgical": surgical(),
        "automation": automation(),
        "clinical_decision": clinical_decision(),
        "digital_twin": digital_twin(),
        "knowledge_graph": knowledge_graph(),
        "observability": observability(),
        "security": security(),
        "cqrs": cqrs(),
        "events": events(),
        "microservices": microservices(),
        "integration": integration(),
        "deployment": deployment(),
        "testing": testing(),
        "api": api(),
        "quality_gates": quality_gates(),
        "production_readiness": production_readiness(),
        "healthcare_robotics_platform_present_required": True,
        "medical_ai_platform_present_required": True,
        "surgical_robotics_platform_present_required": True,
        "clinical_decision_intelligence_present_required": True,
        "digital_healthcare_automation_platform_present_required": True,
        "healthcare_digital_twin_present_required": True,
        "medical_knowledge_graph_present_required": True,
        "security_compliance_architecture_present_required": True,
        "cqrs_architecture_present_required": True,
        "event_architecture_present_required": True,
        "microservices_architecture_present_required": True,
        "cloud_edge_deployment_present_required": True,
        "enterprise_healthcare_integration_present_required": True,
        "testing_validation_architecture_present_required": True,
        "sibling_robotics_bc_forbidden": True,
        "never_replace_p216_foundation": True,
        "never_replace_p216_a_mission": True,
        "never_replace_p216_b_strategy": True,
        "never_replace_p216_c_domain": True,
        "never_replace_p216_d_runtime": True,
        "never_replace_p216_e_physical_ai": True,
        "never_replace_p216_f_industrial": True,
        "never_replace_p216_g_logistics": True,
        "never_replace_p216_h_mobility": True,
        "never_replace_core_platform": True,
        "never_replace_ai_platform": True,
        "never_replace_p215_z": True,
        "never_direct_fhir_hl7_dicom_bypass": True,
        "fhir_hl7_dicom_via_integration_platform_only": True,
        "never_duplicate_hospital_clinic_core_logic": True,
        "no_module_local_llm": True,
        "medical_ai_via_p214z_acl_only": True,
        "physical_ai_via_p214z_acl_only": True,
        "human_in_the_loop_required_for_clinical_autonomy": True,
        "ungated_physical_autonomy_strategy_forbidden": True,
        "opaque_safety_strategy_forbidden": True,
        "builds_on_p216": True, "builds_on_p216_h": True, "builds_on_p216_g": True,
        "builds_on_p216_e": True, "builds_on_p216_d": True,
        "builds_on_p215_z": True, "builds_on_p214_z": True,
        "via_p216_d": True, "via_p216_e": True, "via_p216_h": True,
        "via_p215_z": True, "via_p214_z": True, "via_p213": True,
        "via_policy_engine": True, "via_workflow": True, "via_audit": True,
        "via_integration_platform": True,
        "api_prefix": f"{API_PREFIX}/healthcare",
        "forbidden_sibling_bc": [
            "healthcare_robotics_platform",
            "medical_ai_platform",
            "surgical_robotics_platform",
            "digital_healthcare_automation_platform",
        ],
        "foundation_for_p216_j": True,
    }

def healthcare_surface() -> dict[str, Any]:
    return {"prompt_id": PROMPT_ID, "routes": [
        "GET /robotics/healthcare",
        "GET /robotics/healthcare/vision",
        "GET /robotics/healthcare/domain",
        "GET /robotics/healthcare/bounded-contexts",
        "GET /robotics/healthcare/robotics",
        "GET /robotics/healthcare/medical-ai",
        "GET /robotics/healthcare/surgical",
        "GET /robotics/healthcare/automation",
        "GET /robotics/healthcare/clinical-decision",
        "GET /robotics/healthcare/digital-twin",
        "GET /robotics/healthcare/knowledge-graph",
        "GET /robotics/healthcare/observability",
        "GET /robotics/healthcare/security",
        "GET /robotics/healthcare/cqrs",
        "GET /robotics/healthcare/events",
        "GET /robotics/healthcare/microservices",
        "GET /robotics/healthcare/integration",
        "GET /robotics/healthcare/deployment",
        "GET /robotics/healthcare/testing",
        "GET /robotics/healthcare/readiness",
    ], "mobility_gate_routes": ["GET /robotics/mobility", "GET /robotics/mobility/readiness"]}
