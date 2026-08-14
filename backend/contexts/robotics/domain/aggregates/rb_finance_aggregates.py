"""P216-R aggregates — financial robotics / autonomous banking invariants."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import UTC, datetime
from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId

def _tid(tenant_id: str, code: str) -> str:
    if not tenant_id.strip():
        raise ValueError(code)
    return tenant_id.strip()

def _mk(root_cls, tenant_id: str, ref_name: str, ref_value: str, err: str, event: str):
    tid = _tid(tenant_id, err + ".tenant")
    obj = root_cls(id=UniqueId.generate(), tenant_id=tid, **{ref_name: ref_value.strip()}, present=True, status="enabled")
    obj.pending_events.append(event)
    return obj

@dataclass(eq=False, kw_only=True)
class FinancialRoboticsRoot(AggregateRoot):
    tenant_id: str; robotics_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, robotics_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.finance.financial_robotics_platform_is_missing")
        return _mk(cls, tenant_id, "robotics_ref", robotics_ref, "robotics.finance.financial_robotics_platform_is_missing", "FinancialRobotCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousBankingRoot(AggregateRoot):
    tenant_id: str; banking_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, banking_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.finance.autonomous_banking_platform_is_missing")
        return _mk(cls, tenant_id, "banking_ref", banking_ref, "robotics.finance.autonomous_banking_platform_is_missing", "PaymentCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class FinanceAutomationRoot(AggregateRoot):
    tenant_id: str; automation_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, automation_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.finance.finance_automation_platform_is_missing")
        return _mk(cls, tenant_id, "automation_ref", automation_ref, "robotics.finance.finance_automation_platform_is_missing", "FinancialOptimisedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AiFinancialIntelligenceRoot(AggregateRoot):
    tenant_id: str; ai_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ai_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.finance.ai_financial_intelligence_is_missing")
        return _mk(cls, tenant_id, "ai_ref", ai_ref, "robotics.finance.ai_financial_intelligence_is_missing", "TransactionCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class RiskIntelligenceRoot(AggregateRoot):
    tenant_id: str; risk_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, risk_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.finance.risk_intelligence_platform_is_missing")
        return _mk(cls, tenant_id, "risk_ref", risk_ref, "robotics.finance.risk_intelligence_platform_is_missing", "RiskDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ComplianceAutomationRoot(AggregateRoot):
    tenant_id: str; compliance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, compliance_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.finance.compliance_automation_is_missing")
        return _mk(cls, tenant_id, "compliance_ref", compliance_ref, "robotics.finance.compliance_automation_is_missing", "ComplianceValidatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class FinancialDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.finance.financial_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "robotics.finance.financial_digital_twin_is_missing", "FinancialOptimisedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class FinancialKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.finance.financial_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "robotics.finance.financial_knowledge_graph_is_missing", "TransactionCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class FinanceSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.finance.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "robotics.finance.security_architecture_is_missing", "AuditGeneratedEvent")
    def is_missing(self)->bool: return not self.present
