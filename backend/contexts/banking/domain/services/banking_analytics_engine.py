"""Banking Analytics Platform domain logic."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from contexts.banking.domain.aggregates.banking_analytics_engine import AnalyticsCapability

ANALYTICS_CATALOG: dict[str, dict] = {
    AnalyticsCapability.LIQUIDITY_KPIS.value: {"label": "Liquidity KPIs", "supported": True},
    AnalyticsCapability.DEPOSIT_TRENDS.value: {"label": "Deposit Trends", "supported": True},
    AnalyticsCapability.LOAN_PORTFOLIO.value: {"label": "Loan Portfolio", "supported": True},
    AnalyticsCapability.CUSTOMER_SEGMENTATION.value: {"label": "Customer Segmentation", "supported": True},
    AnalyticsCapability.BRANCH_PERFORMANCE.value: {"label": "Branch Performance", "supported": True},
    AnalyticsCapability.REVENUE_ANALYSIS.value: {"label": "Revenue Analysis", "supported": True},
    AnalyticsCapability.RISK_INDICATORS.value: {"label": "Risk Indicators", "supported": True},
    AnalyticsCapability.PORTFOLIO_QUALITY.value: {"label": "Portfolio Quality", "supported": True},
    AnalyticsCapability.DELINQUENCY_ANALYSIS.value: {"label": "Delinquency Analysis", "supported": True},
    AnalyticsCapability.FORECASTING.value: {"label": "Forecasting", "supported": True},
    AnalyticsCapability.FRAUD_DETECTION.value: {"label": "Fraud Detection", "supported": True},
    AnalyticsCapability.CUSTOMER_INSIGHTS.value: {"label": "Customer Insights", "supported": True},
    AnalyticsCapability.EXECUTIVE_DASHBOARD.value: {"label": "Executive Dashboard", "supported": True},
    AnalyticsCapability.AI_BANKING_ASSISTANT.value: {
        "label": "AI Banking Assistant",
        "autonomous_execution": False,
        "explainable": True,
    },
}

ANALYTICS_POLICY_KEYS: list[dict] = [
    {"key": "analytics.liquidity.threshold", "description": "Minimum liquidity ratio threshold"},
    {"key": "analytics.delinquency.warning", "description": "Delinquency rate warning threshold"},
    {"key": "analytics.fraud.alert_threshold", "description": "Fraud alert score threshold"},
    {"key": "analytics.forecast.horizon", "description": "Forecast projection horizon in days"},
    {"key": "analytics.segmentation.rules", "description": "Customer segmentation tier rules"},
    {"key": "analytics.revenue.target", "description": "Revenue target thresholds"},
    {"key": "analytics.risk.indicator_threshold", "description": "Risk indicator alert threshold"},
    {"key": "analytics.portfolio.quality_minimum", "description": "Minimum portfolio quality score"},
]


def list_analytics_catalog() -> list[dict]:
    return [
        {
            "capability": k,
            **v,
            "explainable": v.get("explainable", k == AnalyticsCapability.AI_BANKING_ASSISTANT.value),
        }
        for k, v in ANALYTICS_CATALOG.items()
    ]


def list_analytics_policy_keys() -> list[dict]:
    return list(ANALYTICS_POLICY_KEYS)


def explainable_recommendation(
    *,
    priority: str,
    category: str,
    action: str,
    detail: str,
    explanation: str,
    evidence: list[dict] | None = None,
    confidence: float = 0.8,
) -> dict:
    return {
        "priority": priority,
        "category": category,
        "action": action,
        "detail": detail,
        "explanation": explanation,
        "evidence": evidence or [],
        "confidence": round(confidence, 2),
        "autonomous_execution": False,
        "explainable": True,
    }


def _sum_balances(accounts: list[dict]) -> float:
    return round(sum(float(a.get("balance", 0)) for a in accounts), 2)


def _active_loans(loans: list[dict]) -> list[dict]:
    active = {"active", "disbursed", "restructured"}
    return [l for l in loans if l.get("status") in active]


def build_liquidity_kpis(*, ctx: dict, policy_params: dict) -> dict:
    accounts = ctx["accounts"]
    deposits = ctx["deposits"]
    loans = _active_loans(ctx["loans"])
    total_deposits = round(sum(float(d.get("balance", 0)) for d in deposits), 2)
    total_loans = round(sum(float(l.get("outstanding_principal", 0)) for l in loans), 2)
    liquid_balance = _sum_balances(accounts)
    loan_to_deposit = round(total_loans / total_deposits, 4) if total_deposits else 0
    liquidity_ratio = round(liquid_balance / total_deposits, 4) if total_deposits else 0
    threshold = float(policy_params.get("min_liquidity_ratio", 0.15))

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "kpis": {
            "total_deposits": total_deposits,
            "total_loans_outstanding": total_loans,
            "liquid_balance": liquid_balance,
            "loan_to_deposit_ratio": loan_to_deposit,
            "liquidity_ratio": liquidity_ratio,
            "deposit_coverage": round(total_deposits / total_loans, 4) if total_loans else 0,
        },
        "status": "healthy" if liquidity_ratio >= threshold else "attention",
        "threshold": threshold,
    }


def build_deposit_trends(*, ctx: dict) -> dict:
    deposits = ctx["deposits"]
    transactions = ctx["deposit_transactions"]
    by_type: dict[str, float] = {}
    monthly: dict[str, dict] = {}

    for d in deposits:
        dtype = d.get("deposit_type", "savings")
        by_type[dtype] = round(by_type.get(dtype, 0) + float(d.get("balance", 0)), 2)

    for txn in transactions:
        month = (txn.get("posted_at") or datetime.now(UTC).isoformat())[:7]
        bucket = monthly.setdefault(month, {"deposits": 0.0, "withdrawals": 0.0})
        amount = float(txn.get("amount", 0))
        if txn.get("transaction_type") == "withdrawal":
            bucket["withdrawals"] = round(bucket["withdrawals"] + amount, 2)
        else:
            bucket["deposits"] = round(bucket["deposits"] + amount, 2)

    sorted_months = sorted(monthly.items())[-6:]
    net_trend = 0.0
    if len(sorted_months) >= 2:
        first_net = sorted_months[0][1]["deposits"] - sorted_months[0][1]["withdrawals"]
        last_net = sorted_months[-1][1]["deposits"] - sorted_months[-1][1]["withdrawals"]
        net_trend = round(last_net - first_net, 2)

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "total_deposit_balance": round(sum(by_type.values()), 2),
        "by_product_type": by_type,
        "monthly_flow": [{"period": m, **v} for m, v in sorted_months],
        "net_flow_trend": net_trend,
        "trend_direction": "growing" if net_trend >= 0 else "declining",
        "account_count": len(deposits),
    }


def build_loan_portfolio(*, ctx: dict) -> dict:
    loans = ctx["loans"]
    active = _active_loans(loans)
    by_type: dict[str, dict] = {}
    total_principal = 0.0
    total_outstanding = 0.0

    for loan in loans:
        ltype = loan.get("loan_type", "personal")
        bucket = by_type.setdefault(ltype, {"count": 0, "principal": 0.0, "outstanding": 0.0})
        bucket["count"] += 1
        bucket["principal"] = round(bucket["principal"] + float(loan.get("principal", 0)), 2)
        bucket["outstanding"] = round(bucket["outstanding"] + float(loan.get("outstanding_principal", 0)), 2)
        total_principal += float(loan.get("principal", 0))
        total_outstanding += float(loan.get("outstanding_principal", 0))

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "total_loans": len(loans),
        "active_loans": len(active),
        "total_principal": round(total_principal, 2),
        "total_outstanding": round(total_outstanding, 2),
        "by_loan_type": by_type,
        "avg_loan_size": round(total_principal / len(loans), 2) if loans else 0,
    }


def build_customer_segmentation(*, ctx: dict, policy_params: dict) -> dict:
    customers = ctx["customers"]
    accounts = ctx["accounts"]
    tiers = policy_params.get("tiers", ["retail", "premium", "corporate"])
    segments: dict[str, dict] = {t: {"count": 0, "total_balance": 0.0} for t in tiers}
    segments["unclassified"] = {"count": 0, "total_balance": 0.0}

    balance_by_customer: dict[str, float] = {}
    for acct in accounts:
        cid = acct.get("customer_id", "")
        balance_by_customer[cid] = round(balance_by_customer.get(cid, 0) + float(acct.get("balance", 0)), 2)

    for customer in customers:
        tier = customer.get("customer_tier") or customer.get("segment") or "retail"
        if tier not in segments:
            tier = "unclassified"
        segments[tier]["count"] += 1
        segments[tier]["total_balance"] = round(
            segments[tier]["total_balance"] + balance_by_customer.get(str(customer.get("id", "")), 0), 2
        )

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "total_customers": len(customers),
        "segments": segments,
        "top_segment": max(segments.items(), key=lambda x: x[1]["total_balance"])[0] if customers else None,
    }


def build_branch_performance(*, ctx: dict) -> dict:
    offices = ctx["branch_offices"]
    kpis = ctx["branch_kpis"]
    by_office: dict[str, dict] = {}

    for office in offices:
        oid = str(office.get("id", ""))
        by_office[oid] = {
            "office_code": office.get("code"),
            "office_name": office.get("name"),
            "office_type": office.get("office_type"),
            "kpi_count": 0,
            "total_transactions": 0,
            "total_volume": 0.0,
        }

    for kpi in kpis:
        oid = kpi.get("office_id", "")
        bucket = by_office.setdefault(oid, {"office_code": oid, "kpi_count": 0, "total_transactions": 0, "total_volume": 0.0})
        bucket["kpi_count"] += 1
        bucket["total_transactions"] += int(kpi.get("transaction_count", 0))
        bucket["total_volume"] = round(bucket["total_volume"] + float(kpi.get("volume", 0)), 2)

    ranked = sorted(by_office.values(), key=lambda x: x.get("total_volume", 0), reverse=True)

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "branch_count": len(offices),
        "kpi_records": len(kpis),
        "by_branch": ranked,
        "top_branch": ranked[0] if ranked else None,
    }


def build_revenue_analysis(*, ctx: dict, policy_params: dict) -> dict:
    accruals = ctx["interest_accruals"]
    loan_txns = ctx["loan_transactions"]
    total_interest = round(sum(float(a.get("accrued_amount", 0)) for a in accruals), 2)
    fee_income = round(
        sum(float(t.get("amount", 0)) for t in loan_txns if t.get("transaction_type") == "penalty"), 2
    )
    total_revenue = round(total_interest + fee_income, 2)
    target = float(policy_params.get("monthly_target", 100000))

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "interest_income": total_interest,
        "fee_income": fee_income,
        "total_revenue": total_revenue,
        "revenue_target": target,
        "target_achievement_pct": round(total_revenue / target * 100, 2) if target else 0,
        "accrual_count": len(accruals),
    }


def build_risk_indicators(*, ctx: dict, policy_params: dict) -> dict:
    credit_risks = ctx["credit_risks"]
    fraud_checks = ctx["fraud_checks"]
    alerts = ctx["security_alerts"]
    threshold = float(policy_params.get("alert_threshold", 60))

    high_risk = [r for r in credit_risks if r.get("risk_grade") in {"high", "critical"}]
    flagged_fraud = [f for f in fraud_checks if f.get("flagged")]
    open_alerts = [a for a in alerts if a.get("status") == "open"]
    risk_score = min(100, len(high_risk) * 15 + len(flagged_fraud) * 10 + len(open_alerts) * 5)

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "composite_risk_score": risk_score,
        "risk_level": "high" if risk_score >= threshold else "medium" if risk_score >= threshold / 2 else "low",
        "high_risk_loans": len(high_risk),
        "flagged_fraud_count": len(flagged_fraud),
        "open_security_alerts": len(open_alerts),
        "threshold": threshold,
        "indicators": {
            "credit_risk": len(high_risk),
            "fraud": len(flagged_fraud),
            "monitoring_alerts": len(open_alerts),
        },
    }


def build_portfolio_quality(*, ctx: dict, policy_params: dict) -> dict:
    loans = _active_loans(ctx["loans"])
    installments = ctx["loan_installments"]
    overdue = [i for i in installments if i.get("status") == "overdue"]
    total_outstanding = sum(float(l.get("outstanding_principal", 0)) for l in loans)
    overdue_amount = round(sum(float(i.get("amount_due", 0)) for i in overdue), 2)
    npl_ratio = round(overdue_amount / total_outstanding, 4) if total_outstanding else 0
    quality_score = round(max(0, 100 - npl_ratio * 500), 2)
    minimum = float(policy_params.get("minimum_score", 70))

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "portfolio_quality_score": quality_score,
        "npl_ratio": npl_ratio,
        "overdue_installments": len(overdue),
        "overdue_amount": overdue_amount,
        "active_loan_count": len(loans),
        "status": "healthy" if quality_score >= minimum else "degraded",
        "minimum_score": minimum,
    }


def build_delinquency_analysis(*, ctx: dict, policy_params: dict) -> dict:
    installments = ctx["loan_installments"]
    loans = ctx["loans"]
    warning_rate = float(policy_params.get("warning_rate", 0.05))
    overdue = [i for i in installments if i.get("status") == "overdue"]
    due = [i for i in installments if i.get("status") in {"due", "scheduled"}]
    delinquency_rate = round(len(overdue) / len(installments), 4) if installments else 0

    by_bucket: dict[str, int] = {"1-30": 0, "31-60": 0, "61-90": 0, "90+": 0}
    now = datetime.now(UTC)
    for inst in overdue:
        due_date = inst.get("due_date")
        if due_date:
            try:
                days = (now - datetime.fromisoformat(due_date.replace("Z", "+00:00"))).days
            except ValueError:
                days = 30
        else:
            days = 30
        if days <= 30:
            by_bucket["1-30"] += 1
        elif days <= 60:
            by_bucket["31-60"] += 1
        elif days <= 90:
            by_bucket["61-90"] += 1
        else:
            by_bucket["90+"] += 1

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "delinquency_rate": delinquency_rate,
        "overdue_count": len(overdue),
        "due_count": len(due),
        "total_installments": len(installments),
        "active_loans": len(_active_loans(loans)),
        "aging_buckets": by_bucket,
        "status": "warning" if delinquency_rate >= warning_rate else "normal",
        "warning_threshold": warning_rate,
    }


def build_forecasting(*, ctx: dict, policy_params: dict) -> dict:
    horizon = int(policy_params.get("horizon_days", 90))
    deposits = ctx["deposit_transactions"]
    transfers = ctx["transfers"]
    monthly_deposits: dict[str, float] = {}
    monthly_transfers: dict[str, float] = {}

    for txn in deposits:
        month = (txn.get("posted_at") or datetime.now(UTC).isoformat())[:7]
        monthly_deposits[month] = round(monthly_deposits.get(month, 0) + float(txn.get("amount", 0)), 2)

    for txn in transfers:
        month = (txn.get("created_at") or datetime.now(UTC).isoformat())[:7]
        monthly_transfers[month] = round(monthly_transfers.get(month, 0) + float(txn.get("amount", 0)), 2)

    avg_deposit = round(sum(monthly_deposits.values()) / max(len(monthly_deposits), 1), 2)
    avg_transfer = round(sum(monthly_transfers.values()) / max(len(monthly_transfers), 1), 2)
    months_ahead = max(1, horizon // 30)

    projections = []
    for i in range(1, months_ahead + 1):
        future = (datetime.now(UTC) + timedelta(days=30 * i)).strftime("%Y-%m")
        projections.append({
            "period": future,
            "projected_deposits": avg_deposit,
            "projected_transfers": avg_transfer,
            "net_flow": round(avg_deposit - avg_transfer, 2),
        })

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "horizon_days": horizon,
        "avg_monthly_deposits": avg_deposit,
        "avg_monthly_transfers": avg_transfer,
        "projections": projections,
        "confidence": 0.75 if len(monthly_deposits) >= 3 else 0.55,
        "method": "moving_average",
    }


def build_fraud_detection(*, ctx: dict, policy_params: dict) -> dict:
    fraud_checks = ctx["fraud_checks"]
    alerts = ctx["security_alerts"]
    threshold = float(policy_params.get("alert_threshold", 70))
    flagged = [f for f in fraud_checks if f.get("flagged") or float(f.get("risk_score", 0)) >= threshold]
    open_alerts = [a for a in alerts if a.get("status") == "open"]

    patterns: dict[str, int] = {}
    for f in flagged:
        reason = f.get("reason", "unknown")
        patterns[reason] = patterns.get(reason, 0) + 1

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "flagged_transactions": len(flagged),
        "total_fraud_checks": len(fraud_checks),
        "open_monitoring_alerts": len(open_alerts),
        "fraud_patterns": patterns,
        "alert_threshold": threshold,
        "detection_rate": round(len(flagged) / len(fraud_checks), 4) if fraud_checks else 0,
    }


def build_customer_insights(*, ctx: dict) -> dict:
    customers = ctx["customers"]
    accounts = ctx["accounts"]
    transfers = ctx["transfers"]
    insights: list[dict] = []

    multi_account = sum(1 for c in customers if sum(1 for a in accounts if a.get("customer_id") == str(c.get("id"))) > 1)
    if multi_account:
        insights.append({
            "type": "multi_account_holders",
            "count": multi_account,
            "detail": f"{multi_account} customers hold multiple accounts",
        })

    high_value = [a for a in accounts if float(a.get("balance", 0)) >= 50000]
    if high_value:
        insights.append({
            "type": "high_value_accounts",
            "count": len(high_value),
            "detail": f"{len(high_value)} accounts exceed 50,000 balance threshold",
        })

    active_transfers = len([t for t in transfers if t.get("status") in {"posted", "completed", "approved"}])
    insights.append({
        "type": "transfer_activity",
        "count": active_transfers,
        "detail": f"{active_transfers} completed transfers in portfolio",
    })

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "customer_count": len(customers),
        "account_count": len(accounts),
        "insights": insights,
        "insight_count": len(insights),
    }


def generate_banking_recommendations(*, ctx: dict, policy_params: dict) -> dict:
    recommendations: list[dict] = []
    liquidity = build_liquidity_kpis(ctx=ctx, policy_params=policy_params.get("liquidity", {}))
    delinquency = build_delinquency_analysis(ctx=ctx, policy_params=policy_params.get("delinquency", {}))
    portfolio = build_portfolio_quality(ctx=ctx, policy_params=policy_params.get("portfolio", {}))
    fraud = build_fraud_detection(ctx=ctx, policy_params=policy_params.get("fraud", {}))
    revenue = build_revenue_analysis(ctx=ctx, policy_params=policy_params.get("revenue", {}))

    if liquidity["status"] == "attention":
        recommendations.append(explainable_recommendation(
            priority="high",
            category="liquidity",
            action="strengthen_liquidity_buffer",
            detail=f"Liquidity ratio {liquidity['kpis']['liquidity_ratio']:.2%} below threshold",
            explanation="Deposit growth is not keeping pace with loan book expansion.",
            evidence=[{"metric": "liquidity_ratio", "value": liquidity["kpis"]["liquidity_ratio"]}],
            confidence=0.89,
        ))

    if delinquency["status"] == "warning":
        recommendations.append(explainable_recommendation(
            priority="high",
            category="delinquency",
            action="intensify_collections",
            detail=f"Delinquency rate {delinquency['delinquency_rate']:.2%} exceeds warning threshold",
            explanation="Overdue installments are rising — prioritize early-stage recovery.",
            evidence=[{"metric": "overdue_count", "value": delinquency["overdue_count"]}],
            confidence=0.91,
        ))

    if portfolio["status"] == "degraded":
        recommendations.append(explainable_recommendation(
            priority="medium",
            category="portfolio_quality",
            action="review_credit_policy",
            detail=f"Portfolio quality score {portfolio['portfolio_quality_score']} below minimum",
            explanation="NPL ratio is eroding portfolio quality — tighten underwriting criteria.",
            evidence=[{"metric": "npl_ratio", "value": portfolio["npl_ratio"]}],
            confidence=0.85,
        ))

    if fraud["flagged_transactions"] > 0:
        recommendations.append(explainable_recommendation(
            priority="high",
            category="fraud",
            action="escalate_fraud_review",
            detail=f"{fraud['flagged_transactions']} flagged transaction(s) detected",
            explanation="Fraud patterns require immediate compliance review.",
            evidence=[{"metric": "flagged", "value": fraud["flagged_transactions"]}],
            confidence=0.93,
        ))

    if revenue["target_achievement_pct"] < 80:
        recommendations.append(explainable_recommendation(
            priority="medium",
            category="revenue",
            action="accelerate_fee_products",
            detail=f"Revenue at {revenue['target_achievement_pct']:.1f}% of target",
            explanation="Interest and fee income below target — review pricing and cross-sell.",
            evidence=[{"metric": "total_revenue", "value": revenue["total_revenue"]}],
            confidence=0.82,
        ))

    by_category: dict[str, list[dict]] = {}
    for rec in recommendations:
        by_category.setdefault(rec["category"], []).append(rec)

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "recommendation_count": len(recommendations),
        "by_category": by_category,
        "recommendations": recommendations,
        "autonomous_execution": False,
        "explainable": True,
    }


def build_executive_dashboard(*, ctx: dict, policy_params: dict) -> dict:
    liquidity = build_liquidity_kpis(ctx=ctx, policy_params=policy_params.get("liquidity", {}))
    deposits = build_deposit_trends(ctx=ctx)
    loans = build_loan_portfolio(ctx=ctx)
    risk = build_risk_indicators(ctx=ctx, policy_params=policy_params.get("risk", {}))
    portfolio = build_portfolio_quality(ctx=ctx, policy_params=policy_params.get("portfolio", {}))
    revenue = build_revenue_analysis(ctx=ctx, policy_params=policy_params.get("revenue", {}))
    recs = generate_banking_recommendations(ctx=ctx, policy_params=policy_params)

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "audience": "executive",
        "headline": {
            "total_deposits": liquidity["kpis"]["total_deposits"],
            "total_loans_outstanding": liquidity["kpis"]["total_loans_outstanding"],
            "liquidity_ratio": liquidity["kpis"]["liquidity_ratio"],
            "portfolio_quality_score": portfolio["portfolio_quality_score"],
            "composite_risk_score": risk["composite_risk_score"],
            "total_revenue": revenue["total_revenue"],
            "deposit_trend": deposits["trend_direction"],
            "active_loans": loans["active_loans"],
        },
        "risk_summary": risk,
        "revenue_summary": revenue,
        "recommendations_count": recs["recommendation_count"],
        "explainable": True,
    }


def generate_ai_banking_assistant(*, ctx: dict, policy_params: dict) -> dict:
    liquidity = build_liquidity_kpis(ctx=ctx, policy_params=policy_params.get("liquidity", {}))
    delinquency = build_delinquency_analysis(ctx=ctx, policy_params=policy_params.get("delinquency", {}))
    fraud = build_fraud_detection(ctx=ctx, policy_params=policy_params.get("fraud", {}))
    forecast = build_forecasting(ctx=ctx, policy_params=policy_params.get("forecast", {}))
    recs = generate_banking_recommendations(ctx=ctx, policy_params=policy_params)

    insights: list[str] = []
    if liquidity["status"] == "attention":
        insights.append(
            f"Liquidity ratio at {liquidity['kpis']['liquidity_ratio']:.2%} — review funding strategy."
        )
    if delinquency["status"] == "warning":
        insights.append(
            f"Delinquency rate {delinquency['delinquency_rate']:.2%} — collections intervention recommended."
        )
    if fraud["flagged_transactions"] > 0:
        insights.append(f"{fraud['flagged_transactions']} fraud flag(s) require compliance review.")
    if forecast["confidence"] < 0.6:
        insights.append("Forecast confidence is low — accumulate more historical data.")
    if not insights:
        insights.append("Banking portfolio is stable — monitor liquidity and delinquency trends.")

    top_recs = sorted(recs["recommendations"], key=lambda r: r["priority"] == "high", reverse=True)[:5]

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "assistant": "banking_ai",
        "insights": insights,
        "top_recommendations": top_recs,
        "kpi_snapshot": liquidity["kpis"],
        "forecast_summary": {
            "horizon_days": forecast["horizon_days"],
            "confidence": forecast["confidence"],
        },
        "recommendation_summary": {
            "total": recs["recommendation_count"],
            "categories": list(recs["by_category"].keys()),
        },
        "explanation": (
            f"AI assistant analyzed {len(ctx['customers'])} customers, "
            f"{len(ctx['loans'])} loans, and {len(ctx['deposits'])} deposits. "
            f"Generated {len(insights)} insight(s) and {recs['recommendation_count']} explainable recommendation(s)."
        ),
        "autonomous_execution": False,
        "explainable": True,
    }


def build_analytics_dashboard(*, ctx: dict, policy_params: dict) -> dict:
    liquidity = build_liquidity_kpis(ctx=ctx, policy_params=policy_params.get("liquidity", {}))
    recs = generate_banking_recommendations(ctx=ctx, policy_params=policy_params)
    executive = build_executive_dashboard(ctx=ctx, policy_params=policy_params)

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "summary": {
            "capability_count": len(ANALYTICS_CATALOG),
            "customer_count": len(ctx["customers"]),
            "loan_count": len(ctx["loans"]),
            "deposit_count": len(ctx["deposits"]),
            "recommendation_count": recs["recommendation_count"],
        },
        "liquidity_kpis": liquidity["kpis"],
        "executive_headline": executive["headline"],
        "explainable": True,
    }


CAPABILITY_POLICY_KEY = {
    AnalyticsCapability.LIQUIDITY_KPIS.value: "liquidity",
    AnalyticsCapability.DELINQUENCY_ANALYSIS.value: "delinquency",
    AnalyticsCapability.FRAUD_DETECTION.value: "fraud",
    AnalyticsCapability.FORECASTING.value: "forecast",
    AnalyticsCapability.CUSTOMER_SEGMENTATION.value: "segmentation",
    AnalyticsCapability.REVENUE_ANALYSIS.value: "revenue",
    AnalyticsCapability.RISK_INDICATORS.value: "risk",
    AnalyticsCapability.PORTFOLIO_QUALITY.value: "portfolio",
}


CAPABILITY_BUILDERS = {
    AnalyticsCapability.LIQUIDITY_KPIS.value: lambda ctx, p: build_liquidity_kpis(ctx=ctx, policy_params=p),
    AnalyticsCapability.DEPOSIT_TRENDS.value: lambda ctx, p: build_deposit_trends(ctx=ctx),
    AnalyticsCapability.LOAN_PORTFOLIO.value: lambda ctx, p: build_loan_portfolio(ctx=ctx),
    AnalyticsCapability.CUSTOMER_SEGMENTATION.value: lambda ctx, p: build_customer_segmentation(ctx=ctx, policy_params=p),
    AnalyticsCapability.BRANCH_PERFORMANCE.value: lambda ctx, p: build_branch_performance(ctx=ctx),
    AnalyticsCapability.REVENUE_ANALYSIS.value: lambda ctx, p: build_revenue_analysis(ctx=ctx, policy_params=p),
    AnalyticsCapability.RISK_INDICATORS.value: lambda ctx, p: build_risk_indicators(ctx=ctx, policy_params=p),
    AnalyticsCapability.PORTFOLIO_QUALITY.value: lambda ctx, p: build_portfolio_quality(ctx=ctx, policy_params=p),
    AnalyticsCapability.DELINQUENCY_ANALYSIS.value: lambda ctx, p: build_delinquency_analysis(ctx=ctx, policy_params=p),
    AnalyticsCapability.FORECASTING.value: lambda ctx, p: build_forecasting(ctx=ctx, policy_params=p),
    AnalyticsCapability.FRAUD_DETECTION.value: lambda ctx, p: build_fraud_detection(ctx=ctx, policy_params=p),
    AnalyticsCapability.CUSTOMER_INSIGHTS.value: lambda ctx, p: build_customer_insights(ctx=ctx),
    AnalyticsCapability.EXECUTIVE_DASHBOARD.value: lambda ctx, p: build_executive_dashboard(ctx=ctx, policy_params=p),
    AnalyticsCapability.AI_BANKING_ASSISTANT.value: lambda ctx, p: generate_ai_banking_assistant(ctx=ctx, policy_params=p),
}
