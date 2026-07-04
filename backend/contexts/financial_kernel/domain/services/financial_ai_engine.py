"""Financial AI engine — analysis, predictions, recommendations."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta


def _sum_by_type(journals: list[dict], account_types: dict[str, str], acct_type: str) -> float:
    total = 0.0
    for journal in journals:
        if journal.get("status") != "posted":
            continue
        for line in journal.get("lines", []):
            code = line.get("account_code", "")
            if account_types.get(code) != acct_type:
                continue
            debit = float(line.get("debit", 0))
            credit = float(line.get("credit", 0))
            if acct_type == "revenue":
                total += credit - debit
            else:
                total += debit - credit
    return round(total, 2)


def detect_fraud(*, payments: list[dict], threshold: float = 10000) -> dict:
    alerts = []
    for p in payments:
        amount = float(p.get("amount", 0) or p.get("total_amount", 0))
        if amount >= threshold:
            alerts.append(
                {
                    "payment_id": p.get("id"),
                    "amount": amount,
                    "risk": "high" if amount >= threshold * 5 else "medium",
                    "reason": "unusual_amount",
                }
            )
        if p.get("status") == "chargeback":
            alerts.append(
                {
                    "payment_id": p.get("id"),
                    "amount": amount,
                    "risk": "high",
                    "reason": "chargeback_pattern",
                }
            )
    score = min(1.0, len(alerts) * 0.2)
    return {
        "fraud_score": round(score, 2),
        "alert_count": len(alerts),
        "alerts": alerts,
        "recommendation": "review" if alerts else "clear",
    }


def predict_cash_flow(*, journals: list[dict], account_types: dict[str, str], months: int = 3) -> dict:
    revenue = _sum_by_type(journals, account_types, "revenue")
    expenses = _sum_by_type(journals, account_types, "expense")
    net = round(revenue - expenses, 2)
    monthly = round(net / max(len(journals), 1), 2)
    forecast = []
    for i in range(1, months + 1):
        month = (datetime.now(UTC) + timedelta(days=30 * i)).strftime("%Y-%m")
        forecast.append({"month": month, "projected_net_cash_flow": round(monthly * (1 + 0.02 * i), 2)})
    return {
        "historical_net": net,
        "monthly_average": monthly,
        "forecast": forecast,
        "trend": "positive" if net > 0 else "negative",
    }


def forecast_budget(*, budgets: list[dict], journals: list[dict], account_types: dict[str, str]) -> dict:
    items = []
    for b in budgets:
        consumed = float(b.get("consumed", 0))
        amount = float(b.get("amount", 0))
        remaining = float(b.get("remaining", amount - consumed))
        utilization = round(consumed / amount * 100, 2) if amount else 0
        items.append(
            {
                "account_code": b.get("account_code"),
                "budget": amount,
                "consumed": consumed,
                "remaining": remaining,
                "utilization_percent": utilization,
                "forecast_overrun": utilization > 90,
            }
        )
    expenses = _sum_by_type(journals, account_types, "expense")
    return {
        "budget_items": items,
        "total_expense_actual": expenses,
        "at_risk_count": sum(1 for i in items if i["forecast_overrun"]),
    }


def analyze_expenses(*, journals: list[dict], account_types: dict[str, str]) -> dict:
    by_center: dict[str, float] = {}
    total = 0.0
    for journal in journals:
        if journal.get("status") != "posted":
            continue
        for line in journal.get("lines", []):
            if account_types.get(line.get("account_code", "")) != "expense":
                continue
            amount = float(line.get("debit", 0)) - float(line.get("credit", 0))
            center = line.get("cost_center") or "unassigned"
            by_center[center] = round(by_center.get(center, 0) + amount, 2)
            total = round(total + amount, 2)
    top = sorted(by_center.items(), key=lambda x: x[1], reverse=True)[:5]
    return {
        "total_expenses": total,
        "by_cost_center": dict(by_center),
        "top_cost_centers": [{"code": k, "amount": v} for k, v in top],
    }


def predict_revenue(*, journals: list[dict], account_types: dict[str, str], months: int = 3) -> dict:
    revenue = _sum_by_type(journals, account_types, "revenue")
    monthly = round(revenue / max(len(journals), 1), 2)
    forecast = []
    for i in range(1, months + 1):
        month = (datetime.now(UTC) + timedelta(days=30 * i)).strftime("%Y-%m")
        forecast.append({"month": month, "projected_revenue": round(monthly * (1 + 0.03 * i), 2)})
    return {
        "historical_revenue": revenue,
        "monthly_average": monthly,
        "forecast": forecast,
        "growth_rate_percent": 3.0,
    }


def generate_financial_summary(
    *,
    journals: list[dict],
    payments: list[dict],
    account_types: dict[str, str],
) -> dict:
    revenue = _sum_by_type(journals, account_types, "revenue")
    expenses = _sum_by_type(journals, account_types, "expense")
    profit = round(revenue - expenses, 2)
    settled = sum(1 for p in payments if p.get("status") in ("settled", "allocated", "issued"))
    return {
        "revenue": revenue,
        "expenses": expenses,
        "profit": profit,
        "margin_percent": round(profit / revenue * 100, 2) if revenue else 0,
        "journal_count": len(journals),
        "payment_count": len(payments),
        "settled_payments": settled,
        "summary": f"Revenue {revenue:,.2f}, expenses {expenses:,.2f}, profit {profit:,.2f}.",
    }


def analyze_risk(*, payments: list[dict], journals: list[dict], budgets: list[dict]) -> dict:
    risks = []
    chargebacks = [p for p in payments if p.get("status") == "chargeback"]
    if chargebacks:
        risks.append({"type": "payment", "level": "high", "detail": f"{len(chargebacks)} chargebacks"})
    over_budget = [b for b in budgets if float(b.get("consumed", 0)) > float(b.get("amount", 0))]
    if over_budget:
        risks.append({"type": "budget", "level": "medium", "detail": f"{len(over_budget)} over-budget items"})
    if len(journals) == 0:
        risks.append({"type": "data", "level": "low", "detail": "insufficient_journal_data"})
    score = min(1.0, len(risks) * 0.25)
    return {
        "risk_score": round(score, 2),
        "risk_level": "high" if score >= 0.5 else "medium" if score >= 0.25 else "low",
        "risks": risks,
    }


def generate_recommendations(
    *,
    summary: dict,
    risk: dict,
    expense_analysis: dict,
) -> list[dict]:
    recs = []
    if summary.get("profit", 0) < 0:
        recs.append(
            {
                "priority": "high",
                "category": "profitability",
                "action": "reduce_expenses",
                "detail": "Operating at a loss — review top cost centers.",
            }
        )
    if risk.get("risk_level") == "high":
        recs.append(
            {
                "priority": "high",
                "category": "risk",
                "action": "review_payments",
                "detail": "Elevated financial risk detected.",
            }
        )
    top = expense_analysis.get("top_cost_centers", [])
    if top and top[0]["amount"] > summary.get("expenses", 0) * 0.5:
        recs.append(
            {
                "priority": "medium",
                "category": "cost_control",
                "action": "audit_cost_center",
                "detail": f"Cost center {top[0]['code']} drives majority of expenses.",
            }
        )
    if not recs:
        recs.append(
            {
                "priority": "low",
                "category": "general",
                "action": "maintain_course",
                "detail": "Financial indicators within normal range.",
            }
        )
    return recs


def classify_invoice(text: str, amount: float | None = None) -> dict:
    text_lower = text.lower()
    if "credit" in text_lower:
        doc_type = "credit_note"
    elif "debit" in text_lower:
        doc_type = "debit_note"
    elif "purchase" in text_lower or "supplier" in text_lower:
        doc_type = "purchase_invoice"
    elif "receipt" in text_lower:
        doc_type = "receipt"
    elif amount and amount < 0:
        doc_type = "credit_note"
    else:
        doc_type = "sales_invoice"
    return {
        "document_type": doc_type,
        "confidence": 0.85,
        "labels": [doc_type, "financial", "invoice"],
    }


def extract_document_ocr(text: str) -> dict:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    amount = None
    for ln in lines:
        if "$" in ln or "USD" in ln.upper():
            cleaned = ln.replace(",", "")
            nums = "".join(c if c.isdigit() or c == "." else " " for c in cleaned).split()
            for n in nums:
                try:
                    amount = float(n)
                except ValueError:
                    pass
    return {
        "extracted_text": text,
        "line_count": len(lines),
        "detected_amount": amount,
        "fields": {
            "vendor": lines[0] if lines else None,
            "description": lines[1] if len(lines) > 1 else None,
            "amount": amount,
        },
    }


def chatbot_response(*, message: str, context: dict) -> str:
    msg = message.lower()
    if "cash flow" in msg or "cashflow" in msg:
        return "Cash flow analysis is available via POST /financial-ai/analyze/cash_flow_prediction."
    if "fraud" in msg:
        return "Fraud detection scans payments for unusual amounts and chargeback patterns."
    if "budget" in msg:
        return "Budget forecast compares consumed vs allocated amounts across cost centers."
    if "revenue" in msg:
        return f"Current context revenue hint: {context.get('revenue', 'run /analyze/revenue_prediction')}."
    if "risk" in msg:
        return "Risk analysis aggregates payment, budget, and journal signals."
    return (
        "I'm the Lokal Financial Assistant. Ask about cash flow, fraud, budget, revenue, "
        "risk, or request the AI dashboard at GET /financial-ai/dashboard."
    )


def cfo_assistant_response(*, message: str, summary: dict, recommendations: list[dict]) -> dict:
    reply = chatbot_response(message=message, context=summary)
    actions = [r["action"] for r in recommendations[:3]]
    return {
        "reply": reply,
        "executive_summary": summary.get("summary", ""),
        "recommended_actions": actions,
        "kpis": {
            "revenue": summary.get("revenue"),
            "expenses": summary.get("expenses"),
            "profit": summary.get("profit"),
            "margin_percent": summary.get("margin_percent"),
        },
    }


def build_dashboard(
    *,
    summary: dict,
    risk: dict,
    fraud: dict,
    cash_flow: dict,
    recommendations: list[dict],
) -> dict:
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "kpis": {
            "revenue": summary.get("revenue"),
            "expenses": summary.get("expenses"),
            "profit": summary.get("profit"),
            "margin_percent": summary.get("margin_percent"),
            "risk_score": risk.get("risk_score"),
            "fraud_score": fraud.get("fraud_score"),
            "cash_flow_trend": cash_flow.get("trend"),
        },
        "widgets": [
            {"id": "profit_loss", "type": "summary", "data": summary},
            {"id": "risk", "type": "risk_analysis", "data": risk},
            {"id": "fraud", "type": "fraud_detection", "data": fraud},
            {"id": "cash_flow", "type": "cash_flow_prediction", "data": cash_flow},
            {"id": "recommendations", "type": "recommendation", "data": recommendations},
        ],
        "alerts": fraud.get("alerts", []) + risk.get("risks", []),
    }
