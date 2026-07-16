"""Enterprise Risk Platform engine."""
from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime

from contexts.risk.domain.aggregates.risk_platform import (
    RiskCapability,
    RiskCategory,
    RiskSeverity,
    RiskStatus,
)

PLATFORM_CATALOG: dict[str, dict] = {
    RiskCapability.FINANCIAL_RISK.value: {"label": "Financial Risk", "category": RiskCategory.FINANCIAL.value},
    RiskCapability.OPERATIONAL_RISK.value: {"label": "Operational Risk", "category": RiskCategory.OPERATIONAL.value},
    RiskCapability.CYBER_RISK.value: {"label": "Cyber Risk", "category": RiskCategory.CYBER.value},
    RiskCapability.COMPLIANCE_RISK.value: {
        "label": "Compliance Risk",
        "category": RiskCategory.COMPLIANCE.value,
        "delegates_to": "grc",
        "no_duplication": True,
    },
    RiskCapability.VENDOR_RISK.value: {"label": "Vendor Risk", "category": RiskCategory.VENDOR.value},
    RiskCapability.PROJECT_RISK.value: {"label": "Project Risk", "category": RiskCategory.PROJECT.value},
    RiskCapability.TREASURY_RISK.value: {
        "label": "Treasury Risk",
        "category": RiskCategory.TREASURY.value,
        "delegates_to": "treasury_risk",
        "no_duplication": True,
    },
    RiskCapability.FX_RISK.value: {
        "label": "FX Risk",
        "category": RiskCategory.FX.value,
        "delegates_to": "fx_risk",
        "no_duplication": True,
    },
    RiskCapability.CREDIT_RISK.value: {"label": "Credit Risk", "category": RiskCategory.CREDIT.value},
    RiskCapability.LIQUIDITY_RISK.value: {
        "label": "Liquidity Risk",
        "category": RiskCategory.LIQUIDITY.value,
        "delegates_to": "treasury_risk",
    },
    RiskCapability.RISK_MATRIX.value: {"label": "Risk Matrix", "likelihood_impact": True},
    RiskCapability.RISK_REGISTER.value: {"label": "Risk Register", "canonical": True},
    RiskCapability.RISK_DASHBOARD.value: {"label": "Risk Dashboard"},
    RiskCapability.RISK_HEATMAP.value: {"label": "Risk Heatmap", "visual": True},
    RiskCapability.AI_RISK_PREDICTION.value: {
        "label": "AI Risk Prediction",
        "explainable": True,
        "autonomous_execution": False,
    },
}

POLICY_KEYS = [
    "risk.escalation.threshold",
    "risk.matrix.size",
    "risk.ai.confidence_threshold",
    "risk.heatmap.top_n",
    "risk.register.auto_escalate",
]

CATEGORY_DELEGATION: dict[str, str | None] = {
    RiskCategory.TREASURY.value: "treasury_risk",
    RiskCategory.FX.value: "fx_risk",
    RiskCategory.LIQUIDITY.value: "treasury_risk",
    RiskCategory.COMPLIANCE.value: "grc",
}

DEFAULT_SEED_RISKS: list[dict] = [
    {"title": "Revenue recognition variance", "category": RiskCategory.FINANCIAL.value, "likelihood": 3, "impact": 4},
    {"title": "Process failure in order fulfillment", "category": RiskCategory.OPERATIONAL.value, "likelihood": 2, "impact": 3},
    {"title": "Phishing attack on employee accounts", "category": RiskCategory.CYBER.value, "likelihood": 4, "impact": 4},
    {"title": "Regulatory non-compliance fine", "category": RiskCategory.COMPLIANCE.value, "likelihood": 2, "impact": 5, "delegated_to": "grc"},
    {"title": "Critical vendor dependency", "category": RiskCategory.VENDOR.value, "likelihood": 3, "impact": 4},
    {"title": "Project deadline overrun", "category": RiskCategory.PROJECT.value, "likelihood": 4, "impact": 3},
    {"title": "Treasury liquidity shortfall", "category": RiskCategory.TREASURY.value, "likelihood": 2, "impact": 5, "delegated_to": "treasury_risk"},
    {"title": "FX exposure concentration", "category": RiskCategory.FX.value, "likelihood": 3, "impact": 4, "delegated_to": "fx_risk"},
    {"title": "Customer credit default", "category": RiskCategory.CREDIT.value, "likelihood": 3, "impact": 4},
    {"title": "Cash reserve below minimum", "category": RiskCategory.LIQUIDITY.value, "likelihood": 2, "impact": 5, "delegated_to": "treasury_risk"},
]


def list_capability_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in PLATFORM_CATALOG.items()]


def list_policy_keys() -> list[str]:
    return list(POLICY_KEYS)


def list_categories() -> list[dict]:
    return [
        {"category": c.value, "label": c.value.replace("_", " ").title(), "delegates_to": CATEGORY_DELEGATION.get(c.value)}
        for c in RiskCategory
    ]


def dependency_map() -> dict:
    nodes = [{"id": "risk_platform", "type": "platform", "label": "Enterprise Risk Platform"}]
    edges = []
    for mod in ("treasury", "currency_exchange", "grc", "compliance", "fraud_detection", "banking"):
        nodes.append({"id": mod, "type": "module", "label": mod})
        edges.append({"from": mod, "to": "risk_platform", "type": "feeds_risk"})
    for svc in ("policy", "audit"):
        nodes.append({"id": svc, "type": "shared_service", "label": svc})
        edges.append({"from": "risk_platform", "to": svc, "type": "delegates"})
    return {"nodes": nodes, "edges": edges, "no_risk_duplication": True}


def compute_risk_score(likelihood: int, impact: int) -> int:
    return likelihood * impact


def severity_from_score(score: int, escalation_threshold: int = 12) -> str:
    if score >= escalation_threshold + 8:
        return RiskSeverity.CRITICAL.value
    if score >= escalation_threshold:
        return RiskSeverity.HIGH.value
    if score >= 6:
        return RiskSeverity.MEDIUM.value
    return RiskSeverity.LOW.value


def build_risk_matrix(*, risks: list[dict], matrix_size: int = 5) -> dict:
    cells: dict[str, dict] = {}
    for likelihood in range(1, matrix_size + 1):
        for impact in range(1, matrix_size + 1):
            key = f"{likelihood}:{impact}"
            cells[key] = {"likelihood": likelihood, "impact": impact, "count": 0, "risks": []}

    for risk in risks:
        if risk.get("status") == RiskStatus.CLOSED.value:
            continue
        lk = min(matrix_size, max(1, risk.get("likelihood", 1)))
        im = min(matrix_size, max(1, risk.get("impact", 1)))
        key = f"{lk}:{im}"
        if key in cells:
            cells[key]["count"] += 1
            cells[key]["risks"].append(risk.get("risk_ref"))

    return {
        "matrix_size": matrix_size,
        "cells": list(cells.values()),
        "total_mapped": sum(c["count"] for c in cells.values()),
    }


def build_heatmap(*, risks: list[dict], top_n: int = 10) -> dict:
    open_risks = [r for r in risks if r.get("status") not in (RiskStatus.CLOSED.value,)]
    by_category: dict[str, list[dict]] = defaultdict(list)
    for risk in open_risks:
        by_category[risk.get("category", "unknown")].append(risk)

    heatmap = []
    for category, items in sorted(by_category.items()):
        avg_score = round(sum(r.get("risk_score", 0) for r in items) / len(items), 1) if items else 0
        max_score = max((r.get("risk_score", 0) for r in items), default=0)
        heatmap.append({
            "category": category,
            "risk_count": len(items),
            "avg_score": avg_score,
            "max_score": max_score,
            "intensity": min(100, round(avg_score / 25 * 100, 1)),
            "top_risks": sorted(items, key=lambda r: r.get("risk_score", 0), reverse=True)[:3],
        })

    heatmap.sort(key=lambda h: h["avg_score"], reverse=True)
    return {
        "categories": heatmap[:top_n],
        "total_open": len(open_risks),
        "highest_category": heatmap[0]["category"] if heatmap else None,
    }


def build_dashboard(
    *,
    profile: dict | None,
    risks: list[dict],
    matrix: dict,
    heatmap: dict,
    predictions: list[dict],
) -> dict:
    open_risks = [r for r in risks if r.get("status") not in (RiskStatus.CLOSED.value,)]
    escalated = [r for r in risks if r.get("status") == RiskStatus.ESCALATED.value]
    by_category: dict[str, int] = defaultdict(int)
    by_severity: dict[str, int] = defaultdict(int)
    for risk in open_risks:
        by_category[risk.get("category", "unknown")] += 1
        by_severity[risk.get("severity", "low")] += 1

    avg_score = round(sum(r.get("risk_score", 0) for r in open_risks) / len(open_risks), 1) if open_risks else 0

    return {
        "summary": {
            "total_risks": len(risks),
            "open_risks": len(open_risks),
            "escalated_risks": len(escalated),
            "avg_risk_score": avg_score,
            "capabilities": len(PLATFORM_CATALOG),
            "enabled_categories": profile.get("enabled_categories", []) if profile else [],
            "predictions_count": len(predictions),
        },
        "by_category": dict(by_category),
        "by_severity": dict(by_severity),
        "matrix_summary": {"total_mapped": matrix.get("total_mapped", 0), "matrix_size": matrix.get("matrix_size", 5)},
        "heatmap_summary": {
            "highest_category": heatmap.get("highest_category"),
            "total_open": heatmap.get("total_open", 0),
        },
        "recent_predictions": predictions[:5],
        "delegation": {
            "treasury_risk": True,
            "fx_risk": True,
            "grc_compliance": True,
            "local_risk_duplication": False,
        },
        "generated_at": datetime.now(UTC).isoformat(),
    }


def ai_risk_prediction(
    *,
    category: str | None,
    risks: list[dict],
    escalation_threshold: int,
    confidence_threshold: float,
) -> dict:
    filtered = risks
    if category:
        filtered = [r for r in risks if r.get("category") == category]

    open_risks = [r for r in filtered if r.get("status") not in (RiskStatus.CLOSED.value,)]
    if not open_risks:
        return {
            "predicted_score": 0.0,
            "trend": "stable",
            "recommendations": [],
            "factors": [{"factor": "no_open_risks", "weight": 0}],
            "confidence": confidence_threshold,
            "explainable": True,
            "autonomous_execution": False,
        }

    avg_score = sum(r.get("risk_score", 0) for r in open_risks) / len(open_risks)
    high_count = len([r for r in open_risks if r.get("risk_score", 0) >= escalation_threshold])
    escalated = len([r for r in open_risks if r.get("status") == RiskStatus.ESCALATED.value])

    predicted = min(25.0, round(avg_score * (1 + high_count * 0.1 + escalated * 0.15), 1))
    trend = "increasing" if high_count > len(open_risks) * 0.3 else "stable" if high_count == 0 else "moderate"

    factors = [
        {"factor": "avg_risk_score", "value": round(avg_score, 1), "weight": 0.4},
        {"factor": "high_risk_count", "value": high_count, "weight": 0.3},
        {"factor": "escalated_count", "value": escalated, "weight": 0.2},
        {"factor": "open_risk_count", "value": len(open_risks), "weight": 0.1},
    ]

    recommendations = []
    if trend == "increasing":
        recommendations.append({
            "title": "Escalate high-risk items",
            "action": f"Review {high_count} risks above threshold {escalation_threshold}",
            "evidence": {"high_count": high_count},
        })
    if category == RiskCategory.CYBER.value and avg_score >= 10:
        recommendations.append({
            "title": "Strengthen cyber controls",
            "action": "Enable security monitoring and access reviews",
            "evidence": {"avg_score": avg_score},
        })

    confidence = min(0.95, confidence_threshold + len(open_risks) * 0.02)

    return {
        "category": category or "all",
        "predicted_score": predicted,
        "trend": trend,
        "recommendations": recommendations,
        "factors": factors,
        "confidence": round(confidence, 2),
        "explainable": True,
        "autonomous_execution": False,
    }
