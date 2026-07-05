"""General Ledger AI engine — explainable recommendations for GL operations."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from contexts.financial_kernel.domain.aggregates.gl_ai import GLAICapability

GL_AI_CATALOG: dict[str, dict] = {
    GLAICapability.POSTING_SUGGESTIONS.value: {
        "label": "Posting Suggestions",
        "description": "Suggest balanced journal lines for a transaction",
    },
    GLAICapability.ACCOUNT_SUGGESTIONS.value: {
        "label": "Account Suggestions",
        "description": "Recommend GL accounts based on transaction context",
    },
    GLAICapability.DUPLICATE_DETECTION.value: {
        "label": "Duplicate Detection",
        "description": "Detect duplicate or near-duplicate journal postings",
    },
    GLAICapability.FRAUD_DETECTION.value: {
        "label": "Fraud Detection",
        "description": "Flag suspicious journal patterns and amounts",
    },
    GLAICapability.CLOSING_ASSISTANT.value: {
        "label": "Closing Assistant",
        "description": "Period-end close checklist and blockers",
    },
    GLAICapability.ANOMALY_DETECTION.value: {
        "label": "Anomaly Detection",
        "description": "Statistical outliers in journal amounts",
    },
    GLAICapability.FINANCIAL_INSIGHTS.value: {
        "label": "Financial Insights",
        "description": "Key insights from posted GL activity",
    },
    GLAICapability.AUTOMATIC_CLASSIFICATION.value: {
        "label": "Automatic Classification",
        "description": "Classify journals by entry type and category",
    },
    GLAICapability.FORECASTING.value: {
        "label": "Forecasting",
        "description": "Project revenue and expenses from GL history",
    },
    GLAICapability.JOURNAL_EXPLANATION.value: {
        "label": "Journal Explanation",
        "description": "Plain-language explanation of a journal entry",
    },
    GLAICapability.VARIANCE_ANALYSIS.value: {
        "label": "Variance Analysis",
        "description": "Budget vs actual and period-over-period variance",
    },
    GLAICapability.AI_CFO_DASHBOARD.value: {
        "label": "AI CFO Dashboard",
        "description": "Executive GL dashboard with explainable recommendations",
    },
}


def list_gl_ai_catalog() -> list[dict]:
    return [
        {
            "capability": key,
            **meta,
            "autonomous_posting": False,
            "explainable": True,
        }
        for key, meta in GL_AI_CATALOG.items()
    ]


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
        "autonomous_posting": False,
    }


def _journal_total(journal: dict) -> float:
    return round(
        sum(float(l.get("debit", 0)) for l in journal.get("lines", [])),
        2,
    )


def _sum_by_category(
    journals: list[dict], account_types: dict[str, str], category: str
) -> float:
    total = 0.0
    for journal in journals:
        if journal.get("status") != "posted":
            continue
        for line in journal.get("lines", []):
            code = line.get("account_code", "")
            if account_types.get(code) != category:
                continue
            debit = float(line.get("debit", 0))
            credit = float(line.get("credit", 0))
            if category == "revenue":
                total += credit - debit
            else:
                total += debit - credit
    return round(total, 2)


def suggest_posting_lines(
    *,
    description: str,
    amount: float,
    accounts: list[dict],
    account_types: dict[str, str],
) -> dict:
    expense_accts = [a for a in accounts if account_types.get(a["code"]) == "expense"]
    asset_accts = [a for a in accounts if account_types.get(a["code"]) == "asset"]
    debit_acct = expense_accts[0] if expense_accts else accounts[0] if accounts else None
    credit_acct = next(
        (a for a in asset_accts if "cash" in a.get("name", "").lower()),
        asset_accts[0] if asset_accts else accounts[1] if len(accounts) > 1 else None,
    )
    lines = []
    if debit_acct and credit_acct:
        lines = [
            {"account_code": debit_acct["code"], "debit": amount, "credit": 0, "description": description},
            {"account_code": credit_acct["code"], "debit": 0, "credit": amount, "description": description},
        ]
    recs = []
    if lines:
        recs.append(
            explainable_recommendation(
                priority="medium",
                category="posting_suggestions",
                action="review_suggested_lines",
                detail=f"Suggested balanced entry for {amount}",
                explanation=(
                    f"Based on description '{description}', debit {debit_acct['code']} "
                    f"({debit_acct.get('name', '')}) and credit {credit_acct['code']} "
                    f"({credit_acct.get('name', '')})."
                ),
                evidence=[{"lines": lines}],
                confidence=0.78,
            )
        )
    return {
        "description": description,
        "amount": amount,
        "suggested_lines": lines,
        "recommendations": recs,
    }


def suggest_accounts(
    *,
    description: str,
    amount: float | None,
    accounts: list[dict],
    account_types: dict[str, str],
) -> dict:
    desc_lower = description.lower()
    suggestions: list[dict] = []
    for acct in accounts:
        score = 0.3
        name_lower = acct.get("name", "").lower()
        code = acct.get("code", "")
        cat = account_types.get(code, "")
        if "revenue" in desc_lower and cat == "revenue":
            score = 0.9
        elif any(w in desc_lower for w in ("expense", "payroll", "salary")) and cat == "expense":
            score = 0.85
        elif any(w in desc_lower for w in ("cash", "payment", "deposit")) and cat == "asset":
            score = 0.88
        elif any(w in name_lower for w in desc_lower.split() if len(w) > 3):
            score = 0.7
        if score >= 0.5:
            suggestions.append(
                {
                    "account_code": code,
                    "account_name": acct.get("name"),
                    "account_category": cat,
                    "confidence": round(score, 2),
                    "reason": f"Matched category {cat} for '{description}'",
                }
            )
    suggestions.sort(key=lambda s: s["confidence"], reverse=True)
    recs = []
    if suggestions:
        top = suggestions[0]
        recs.append(
            explainable_recommendation(
                priority="medium",
                category="account_suggestions",
                action="use_suggested_account",
                detail=f"Top account: {top['account_code']}",
                explanation=top["reason"],
                evidence=[top],
                confidence=top["confidence"],
            )
        )
    return {"description": description, "amount": amount, "suggestions": suggestions[:5], "recommendations": recs}


def detect_duplicate_journals(journals: list[dict]) -> dict:
    seen: dict[str, list[dict]] = {}
    duplicates: list[dict] = []
    for journal in journals:
        if journal.get("status") != "posted":
            continue
        key_parts = [
            journal.get("source_context", ""),
            journal.get("source_document_id", ""),
            str(_journal_total(journal)),
        ]
        key = "|".join(key_parts)
        if key in seen:
            for prior in seen[key]:
                duplicates.append(
                    {
                        "journal_id": journal.get("id"),
                        "duplicate_of": prior.get("id"),
                        "source_document_id": journal.get("source_document_id"),
                        "amount": _journal_total(journal),
                    }
                )
        seen.setdefault(key, []).append(journal)

    idem_seen: dict[str, str] = {}
    for journal in journals:
        ikey = journal.get("idempotency_key", "")
        if not ikey:
            continue
        if ikey in idem_seen:
            duplicates.append(
                {
                    "journal_id": journal.get("id"),
                    "duplicate_of": idem_seen[ikey],
                    "idempotency_key": ikey,
                    "reason": "idempotency_collision",
                }
            )
        else:
            idem_seen[ikey] = journal.get("id", "")

    recs = []
    for dup in duplicates[:5]:
        recs.append(
            explainable_recommendation(
                priority="high",
                category="duplicate_detection",
                action="review_duplicate",
                detail=f"Journal {dup['journal_id']} may duplicate {dup.get('duplicate_of')}",
                explanation=(
                    f"Matching source/amount or idempotency key detected. "
                    f"Amount: {dup.get('amount', 'N/A')}."
                ),
                evidence=[dup],
                confidence=0.91,
            )
        )
    return {
        "duplicate_count": len(duplicates),
        "duplicates": duplicates,
        "recommendations": recs,
    }


def detect_journal_fraud(journals: list[dict], *, threshold: float = 50000) -> dict:
    alerts: list[dict] = []
    for journal in journals:
        if journal.get("status") != "posted":
            continue
        total = _journal_total(journal)
        if total >= threshold:
            alerts.append(
                {
                    "journal_id": journal.get("id"),
                    "amount": total,
                    "risk": "high",
                    "reason": "unusual_amount",
                }
            )
        if total > 0 and total % 1000 == 0 and total >= 10000:
            alerts.append(
                {
                    "journal_id": journal.get("id"),
                    "amount": total,
                    "risk": "medium",
                    "reason": "round_amount_pattern",
                }
            )
        lines = journal.get("lines", [])
        if len(lines) == 2 and all(
            float(l.get("debit", 0)) == float(l.get("credit", 0)) == 0 for l in lines
        ):
            pass
        off_hours = journal.get("created_at", "")
        if off_hours and ("T02:" in off_hours or "T03:" in off_hours):
            alerts.append(
                {
                    "journal_id": journal.get("id"),
                    "risk": "low",
                    "reason": "off_hours_posting",
                }
            )

    score = min(1.0, len(alerts) * 0.15)
    recs = []
    for alert in alerts[:5]:
        recs.append(
            explainable_recommendation(
                priority=alert.get("risk", "medium"),
                category="fraud_detection",
                action="investigate_journal",
                detail=f"Journal {alert['journal_id']}: {alert['reason']}",
                explanation=(
                    f"Suspicious pattern detected — {alert['reason']} "
                    f"with amount {alert.get('amount', 'N/A')}."
                ),
                evidence=[alert],
                confidence=0.85,
            )
        )
    return {
        "fraud_score": round(score, 2),
        "alert_count": len(alerts),
        "alerts": alerts,
        "recommendations": recs,
    }


def closing_assistant(
    *,
    journals: list[dict],
    account_types: dict[str, str],
    period_status: str = "open",
) -> dict:
    unposted = [j for j in journals if j.get("status") in ("draft", "pending_approval")]
    draft_count = len(unposted)
    has_revenue = any(
        account_types.get(l.get("account_code", "")) == "revenue"
        for j in journals
        for l in j.get("lines", [])
    )
    has_expense = any(
        account_types.get(l.get("account_code", "")) == "expense"
        for j in journals
        for l in j.get("lines", [])
    )
    checklist = [
        {"item": "all_journals_posted", "passed": draft_count == 0, "count": draft_count},
        {"item": "revenue_accounts_present", "passed": has_revenue},
        {"item": "expense_accounts_present", "passed": has_expense},
        {"item": "period_open", "passed": period_status == "open"},
    ]
    blockers = [c for c in checklist if not c["passed"]]
    recs = []
    for blocker in blockers:
        recs.append(
            explainable_recommendation(
                priority="high",
                category="closing_assistant",
                action="resolve_blocker",
                detail=f"Close blocker: {blocker['item']}",
                explanation=f"Period close requires {blocker['item']} before proceeding.",
                evidence=[blocker],
                confidence=0.95,
            )
        )
    if not blockers:
        recs.append(
            explainable_recommendation(
                priority="low",
                category="closing_assistant",
                action="proceed_to_close",
                detail="All close checks passed",
                explanation="No blockers detected; period is ready for close review.",
                confidence=0.9,
            )
        )
    return {
        "ready_to_close": len(blockers) == 0,
        "checklist": checklist,
        "blockers": blockers,
        "unposted_count": draft_count,
        "recommendations": recs,
    }


def detect_anomalies(journals: list[dict], *, std_multiplier: float = 2.0) -> dict:
    amounts = [_journal_total(j) for j in journals if j.get("status") == "posted" and _journal_total(j) > 0]
    if not amounts:
        return {"anomaly_count": 0, "anomalies": [], "recommendations": []}
    mean = sum(amounts) / len(amounts)
    variance = sum((a - mean) ** 2 for a in amounts) / len(amounts)
    std = variance ** 0.5
    threshold = mean + std_multiplier * std
    anomalies = []
    for journal in journals:
        if journal.get("status") != "posted":
            continue
        total = _journal_total(journal)
        if total > threshold:
            anomalies.append(
                {
                    "journal_id": journal.get("id"),
                    "amount": total,
                    "mean": round(mean, 2),
                    "threshold": round(threshold, 2),
                    "deviation": round((total - mean) / max(std, 1), 2),
                }
            )
    recs = []
    for anomaly in anomalies[:5]:
        recs.append(
            explainable_recommendation(
                priority="medium",
                category="anomaly_detection",
                action="review_outlier",
                detail=f"Journal {anomaly['journal_id']} amount {anomaly['amount']} exceeds threshold",
                explanation=(
                    f"Amount is {anomaly['deviation']} standard deviations above mean "
                    f"({anomaly['mean']}). Threshold: {anomaly['threshold']}."
                ),
                evidence=[anomaly],
                confidence=0.82,
            )
        )
    return {"anomaly_count": len(anomalies), "anomalies": anomalies, "recommendations": recs}


def generate_financial_insights(
    *,
    journals: list[dict],
    account_types: dict[str, str],
) -> dict:
    posted = [j for j in journals if j.get("status") == "posted"]
    revenue = _sum_by_category(posted, account_types, "revenue")
    expenses = _sum_by_category(posted, account_types, "expense")
    profit = round(revenue - expenses, 2)
    insights = []
    if profit < 0:
        insights.append(
            {
                "type": "profitability",
                "severity": "warning",
                "message": f"Operating loss of {abs(profit):,.2f}",
            }
        )
    if len(posted) < 5:
        insights.append(
            {
                "type": "data_volume",
                "severity": "info",
                "message": "Limited journal history — insights may improve with more data",
            }
        )
    margin = round(profit / revenue * 100, 2) if revenue else 0
    if margin > 20:
        insights.append(
            {
                "type": "margin",
                "severity": "positive",
                "message": f"Healthy margin at {margin}%",
            }
        )
    recs = [
        explainable_recommendation(
            priority="medium" if i.get("severity") == "warning" else "low",
            category="financial_insights",
            action="review_insight",
            detail=i["message"],
            explanation=f"Insight type: {i['type']}. Derived from {len(posted)} posted journals.",
            evidence=[i],
            confidence=0.88,
        )
        for i in insights
    ]
    if not recs:
        recs.append(
            explainable_recommendation(
                priority="low",
                category="financial_insights",
                action="maintain",
                detail="GL activity within normal parameters",
                explanation=f"Revenue {revenue:,.2f}, expenses {expenses:,.2f}, profit {profit:,.2f}.",
                confidence=0.85,
            )
        )
    return {
        "revenue": revenue,
        "expenses": expenses,
        "profit": profit,
        "margin_percent": margin,
        "insights": insights,
        "recommendations": recs,
    }


def classify_journal(journal: dict, account_types: dict[str, str]) -> dict:
    entry_type = journal.get("journal_entry_type", "standard")
    posting_mode = journal.get("posting_mode", "automatic")
    categories = set()
    for line in journal.get("lines", []):
        cat = account_types.get(line.get("account_code", ""), "")
        if cat:
            categories.add(cat)
    if entry_type == "closing":
        classification = "closing_entry"
    elif entry_type == "adjusting":
        classification = "adjusting_entry"
    elif journal.get("reverses_journal_id"):
        classification = "reversal"
    elif "revenue" in categories and "asset" in categories:
        classification = "revenue_recognition"
    elif "expense" in categories and "asset" in categories:
        classification = "expense_payment"
    elif posting_mode == "manual":
        classification = "manual_adjustment"
    else:
        classification = "standard_posting"
    recs = [
        explainable_recommendation(
            priority="low",
            category="automatic_classification",
            action="apply_classification",
            detail=f"Classified as {classification}",
            explanation=(
                f"Based on entry_type={entry_type}, categories={sorted(categories)}, "
                f"posting_mode={posting_mode}."
            ),
            evidence=[{"classification": classification, "categories": sorted(categories)}],
            confidence=0.87,
        )
    ]
    return {
        "journal_id": journal.get("id"),
        "classification": classification,
        "categories": sorted(categories),
        "confidence": 0.87,
        "recommendations": recs,
    }


def forecast_gl(
    *,
    journals: list[dict],
    account_types: dict[str, str],
    months: int = 3,
) -> dict:
    revenue = _sum_by_category(journals, account_types, "revenue")
    expenses = _sum_by_category(journals, account_types, "expense")
    posted_count = max(len([j for j in journals if j.get("status") == "posted"]), 1)
    monthly_rev = round(revenue / posted_count, 2)
    monthly_exp = round(expenses / posted_count, 2)
    forecast = []
    for i in range(1, months + 1):
        month = (datetime.now(UTC) + timedelta(days=30 * i)).strftime("%Y-%m")
        forecast.append(
            {
                "month": month,
                "projected_revenue": round(monthly_rev * (1 + 0.02 * i), 2),
                "projected_expenses": round(monthly_exp * (1 + 0.01 * i), 2),
                "projected_profit": round(monthly_rev * (1 + 0.02 * i) - monthly_exp * (1 + 0.01 * i), 2),
            }
        )
    trend = "positive" if revenue > expenses else "negative"
    recs = [
        explainable_recommendation(
            priority="medium",
            category="forecasting",
            action="review_forecast",
            detail=f"GL trend is {trend}",
            explanation=(
                f"Based on {posted_count} posted journals: avg monthly revenue {monthly_rev:,.2f}, "
                f"expenses {monthly_exp:,.2f}. Projected {months} months forward."
            ),
            evidence=forecast[:2],
            confidence=0.8,
        )
    ]
    return {
        "historical_revenue": revenue,
        "historical_expenses": expenses,
        "monthly_averages": {"revenue": monthly_rev, "expenses": monthly_exp},
        "forecast": forecast,
        "trend": trend,
        "recommendations": recs,
    }


def explain_journal(journal: dict, account_types: dict[str, str], accounts: dict[str, str]) -> dict:
    lines = journal.get("lines", [])
    parts = []
    total_debit = 0.0
    for line in lines:
        code = line.get("account_code", "")
        debit = float(line.get("debit", 0))
        credit = float(line.get("credit", 0))
        total_debit += debit
        name = accounts.get(code, code)
        cat = account_types.get(code, "unknown")
        if debit:
            parts.append(f"Debit {debit:,.2f} to {code} ({name}) [{cat}]")
        if credit:
            parts.append(f"Credit {credit:,.2f} to {code} ({name}) [{cat}]")
    explanation = (
        f"This journal ({journal.get('status', 'unknown')} status) records a "
        f"{journal.get('journal_entry_type', 'standard')} entry totaling {total_debit:,.2f}. "
        + "; ".join(parts)
        + f". Source: {journal.get('source_context')}/{journal.get('source_document_id')}."
    )
    recs = [
        explainable_recommendation(
            priority="low",
            category="journal_explanation",
            action="review_explanation",
            detail=explanation[:200],
            explanation=explanation,
            evidence=[{"journal_id": journal.get("id"), "line_count": len(lines)}],
            confidence=0.95,
        )
    ]
    return {
        "journal_id": journal.get("id"),
        "explanation": explanation,
        "line_summary": parts,
        "recommendations": recs,
    }


def analyze_variance(
    *,
    journals: list[dict],
    budgets: list[dict],
    account_types: dict[str, str],
) -> dict:
    variances: list[dict] = []
    for budget in budgets:
        code = budget.get("account_code", "")
        if account_types.get(code) != "expense":
            continue
        budget_amt = float(budget.get("amount", 0))
        consumed = float(budget.get("consumed", 0))
        remaining = float(budget.get("remaining", budget_amt - consumed))
        variance_pct = round((consumed - budget_amt) / budget_amt * 100, 2) if budget_amt else 0
        variances.append(
            {
                "account_code": code,
                "budget": budget_amt,
                "actual": consumed,
                "variance": round(consumed - budget_amt, 2),
                "variance_percent": variance_pct,
                "cost_center": budget.get("cost_center"),
            }
        )
    over_budget = [v for v in variances if v["variance"] > 0]
    recs = []
    for v in over_budget[:5]:
        recs.append(
            explainable_recommendation(
                priority="high" if v["variance_percent"] > 10 else "medium",
                category="variance_analysis",
                action="investigate_variance",
                detail=f"Account {v['account_code']} over budget by {v['variance_percent']}%",
                explanation=(
                    f"Budget {v['budget']:,.2f} vs actual {v['actual']:,.2f}. "
                    f"Variance: {v['variance']:,.2f}."
                ),
                evidence=[v],
                confidence=0.9,
            )
        )
    if not recs:
        recs.append(
            explainable_recommendation(
                priority="low",
                category="variance_analysis",
                action="no_action",
                detail="All accounts within budget",
                explanation="No material budget variances detected.",
                confidence=0.85,
            )
        )
    return {
        "variance_count": len(variances),
        "over_budget_count": len(over_budget),
        "variances": variances,
        "recommendations": recs,
    }


def build_gl_cfo_dashboard(
    *,
    journals: list[dict],
    budgets: list[dict],
    account_types: dict[str, str],
    accounts: list[dict],
) -> dict:
    insights = generate_financial_insights(journals=journals, account_types=account_types)
    fraud = detect_journal_fraud(journals)
    duplicates = detect_duplicate_journals(journals)
    forecast = forecast_gl(journals=journals, account_types=account_types)
    variance = analyze_variance(journals=journals, budgets=budgets, account_types=account_types)
    all_recs = (
        insights.get("recommendations", [])
        + fraud.get("recommendations", [])
        + duplicates.get("recommendations", [])
        + forecast.get("recommendations", [])
        + variance.get("recommendations", [])
    )
    all_recs.sort(key=lambda r: {"high": 0, "medium": 1, "low": 2}.get(r["priority"], 3))
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "kpis": {
            "revenue": insights.get("revenue"),
            "expenses": insights.get("expenses"),
            "profit": insights.get("profit"),
            "margin_percent": insights.get("margin_percent"),
            "fraud_score": fraud.get("fraud_score"),
            "duplicate_count": duplicates.get("duplicate_count"),
            "forecast_trend": forecast.get("trend"),
        },
        "widgets": [
            {"id": "insights", "type": "financial_insights", "data": insights},
            {"id": "fraud", "type": "fraud_detection", "data": fraud},
            {"id": "duplicates", "type": "duplicate_detection", "data": duplicates},
            {"id": "forecast", "type": "forecasting", "data": forecast},
            {"id": "variance", "type": "variance_analysis", "data": variance},
        ],
        "recommendations": all_recs[:10],
        "explainable": True,
        "autonomous_posting": False,
    }
