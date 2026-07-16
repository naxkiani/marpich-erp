"""Enterprise Risk Platform aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class RiskCapability(StrEnum):
    FINANCIAL_RISK = "financial_risk"
    OPERATIONAL_RISK = "operational_risk"
    CYBER_RISK = "cyber_risk"
    COMPLIANCE_RISK = "compliance_risk"
    VENDOR_RISK = "vendor_risk"
    PROJECT_RISK = "project_risk"
    TREASURY_RISK = "treasury_risk"
    FX_RISK = "fx_risk"
    CREDIT_RISK = "credit_risk"
    LIQUIDITY_RISK = "liquidity_risk"
    RISK_MATRIX = "risk_matrix"
    RISK_REGISTER = "risk_register"
    RISK_DASHBOARD = "risk_dashboard"
    RISK_HEATMAP = "risk_heatmap"
    AI_RISK_PREDICTION = "ai_risk_prediction"


class RiskCategory(StrEnum):
    FINANCIAL = "financial"
    OPERATIONAL = "operational"
    CYBER = "cyber"
    COMPLIANCE = "compliance"
    VENDOR = "vendor"
    PROJECT = "project"
    TREASURY = "treasury"
    FX = "fx"
    CREDIT = "credit"
    LIQUIDITY = "liquidity"


class RiskStatus(StrEnum):
    OPEN = "open"
    MITIGATING = "mitigating"
    ACCEPTED = "accepted"
    CLOSED = "closed"
    ESCALATED = "escalated"


class RiskSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(eq=False, kw_only=True)
class RiskTenantProfile(AggregateRoot):
    tenant_id: str
    profile_ref: str
    matrix_size: int = 5
    escalation_threshold: int = 12
    ai_enabled: bool = True
    enabled_categories: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        profile_ref: str,
        enabled_categories: list[str],
        metadata: dict | None = None,
    ) -> RiskTenantProfile:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            profile_ref=profile_ref,
            enabled_categories=enabled_categories,
            metadata=metadata or {},
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "profile_ref": self.profile_ref,
            "tenant_id": self.tenant_id,
            "matrix_size": self.matrix_size,
            "escalation_threshold": self.escalation_threshold,
            "ai_enabled": self.ai_enabled,
            "enabled_categories": self.enabled_categories,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class EnterpriseRiskItem(AggregateRoot):
    tenant_id: str
    risk_ref: str
    title: str
    category: str
    likelihood: int
    impact: int
    risk_score: int
    severity: str
    status: str
    owner_id: str = ""
    source_module: str = ""
    mitigation_plan: str = ""
    delegated_to: str | None = None
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        risk_ref: str,
        title: str,
        category: str,
        likelihood: int,
        impact: int,
        risk_score: int,
        severity: str,
        owner_id: str = "",
        source_module: str = "",
        mitigation_plan: str = "",
        delegated_to: str | None = None,
        metadata: dict | None = None,
    ) -> EnterpriseRiskItem:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            risk_ref=risk_ref,
            title=title,
            category=category,
            likelihood=likelihood,
            impact=impact,
            risk_score=risk_score,
            severity=severity,
            status=RiskStatus.OPEN.value,
            owner_id=owner_id,
            source_module=source_module,
            mitigation_plan=mitigation_plan,
            delegated_to=delegated_to,
            metadata=metadata or {},
        )

    def escalate(self) -> None:
        self.status = RiskStatus.ESCALATED.value
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "risk_ref": self.risk_ref,
            "tenant_id": self.tenant_id,
            "title": self.title,
            "category": self.category,
            "likelihood": self.likelihood,
            "impact": self.impact,
            "risk_score": self.risk_score,
            "severity": self.severity,
            "status": self.status,
            "owner_id": self.owner_id,
            "source_module": self.source_module,
            "mitigation_plan": self.mitigation_plan,
            "delegated_to": self.delegated_to,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class RiskMatrixSnapshot(AggregateRoot):
    tenant_id: str
    matrix_ref: str
    matrix_size: int
    cells: list[dict] = field(default_factory=list)
    total_risks: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def build(
        cls,
        *,
        tenant_id: str,
        matrix_ref: str,
        matrix_size: int,
        cells: list[dict],
        total_risks: int,
    ) -> RiskMatrixSnapshot:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            matrix_ref=matrix_ref,
            matrix_size=matrix_size,
            cells=cells,
            total_risks=total_risks,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "matrix_ref": self.matrix_ref,
            "tenant_id": self.tenant_id,
            "matrix_size": self.matrix_size,
            "cells": self.cells,
            "total_risks": self.total_risks,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class RiskPrediction(AggregateRoot):
    tenant_id: str
    prediction_ref: str
    category: str
    predicted_score: float
    trend: str
    recommendations: list[dict] = field(default_factory=list)
    factors: list[dict] = field(default_factory=list)
    confidence: float = 0.8
    explainable: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def generate(
        cls,
        *,
        tenant_id: str,
        prediction_ref: str,
        category: str,
        predicted_score: float,
        trend: str,
        recommendations: list[dict],
        factors: list[dict],
        confidence: float = 0.8,
    ) -> RiskPrediction:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            prediction_ref=prediction_ref,
            category=category,
            predicted_score=predicted_score,
            trend=trend,
            recommendations=recommendations,
            factors=factors,
            confidence=confidence,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "prediction_ref": self.prediction_ref,
            "tenant_id": self.tenant_id,
            "category": self.category,
            "predicted_score": self.predicted_score,
            "trend": self.trend,
            "recommendations": self.recommendations,
            "factors": self.factors,
            "confidence": self.confidence,
            "explainable": self.explainable,
            "autonomous_execution": False,
            "created_at": self.created_at.isoformat(),
        }
