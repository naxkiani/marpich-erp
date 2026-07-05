"""Default policy seeds per domain — activated on tenant provision."""
from __future__ import annotations

from datetime import UTC, datetime

DEFAULT_POLICY_TEMPLATES: dict[str, list[dict]] = {
    "hospital": [
        {
            "key": "admission.eligibility",
            "name": "Emergency Admission Criteria",
            "priority": 100,
            "conditions": [{"field": "encounter.type", "operator": "eq", "value": "emergency"}],
            "rules": [
                {
                    "outcome": "allow_admission",
                    "parameters": {"required_documents": ["id", "insurance_card"], "max_wait_minutes": 30},
                }
            ],
            "exceptions": [
                {
                    "id": "pediatric",
                    "name": "Pediatric override",
                    "conditions": [{"field": "patient.age", "operator": "lt", "value": 18}],
                    "rules": [
                        {
                            "outcome": "allow_admission",
                            "parameters": {"required_documents": ["guardian_consent"]},
                        }
                    ],
                }
            ],
            "approval_required": False,
        },
    ],
    "university": [
        {
            "key": "enrollment.max_credits",
            "name": "Maximum Credits Per Semester",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "within_limit", "parameters": {"max_credits": 24}}],
            "approval_required": False,
        },
    ],
    "bank": [
        {
            "key": "lending.single_exposure_limit",
            "name": "Single Exposure Limit",
            "priority": 100,
            "conditions": [{"field": "customer.tier", "operator": "eq", "value": "gold"}],
            "rules": [
                {"outcome": "within_limit", "parameters": {"max_amount": 750000, "requires_committee": False}}
            ],
            "approval_required": False,
        },
        {
            "key": "kyc.identity.verification_required",
            "name": "Identity Verification Requirements",
            "priority": 100,
            "conditions": [],
            "rules": [
                {
                    "outcome": "require_documents",
                    "parameters": {
                        "required_documents": ["passport", "national_id"],
                        "business_documents": ["business_registration", "tax_number"],
                    },
                }
            ],
            "approval_required": False,
        },
        {
            "key": "kyc.document.passport_validity",
            "name": "Passport Validity Minimum",
            "priority": 100,
            "conditions": [{"field": "days_until_expiry", "operator": "lt", "value": 90}],
            "rules": [{"outcome": "reject_expired", "parameters": {"min_validity_days": 90}}],
            "approval_required": False,
        },
        {
            "key": "kyc.risk.classification",
            "name": "KYC Risk Classification",
            "priority": 100,
            "conditions": [],
            "rules": [
                {
                    "outcome": "low_risk",
                    "parameters": {"risk_class": "low", "requires_edd": False},
                }
            ],
            "exceptions": [
                {
                    "id": "pep_high_risk",
                    "name": "PEP high risk override",
                    "conditions": [{"field": "pep_status", "operator": "eq", "value": "confirmed"}],
                    "rules": [
                        {
                            "outcome": "high_risk",
                            "parameters": {"risk_class": "high", "requires_edd": True},
                        }
                    ],
                }
            ],
            "approval_required": False,
        },
        {
            "key": "kyc.dd.enhanced_threshold",
            "name": "Enhanced Due Diligence Threshold",
            "priority": 100,
            "conditions": [{"field": "pep_status", "operator": "in", "value": ["potential_match", "confirmed"]}],
            "rules": [{"outcome": "enhanced_due_diligence", "parameters": {"requires_edd": True}}],
            "approval_required": False,
        },
        {
            "key": "kyc.pep.screening",
            "name": "PEP Screening Rules",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "clear", "parameters": {}}],
            "exceptions": [
                {
                    "id": "pep_confirmed",
                    "name": "PEP confirmed match",
                    "conditions": [{"field": "match_score", "operator": "gte", "value": 0.85}],
                    "rules": [{"outcome": "confirmed_pep", "parameters": {"review_required": True}}],
                },
                {
                    "id": "pep_potential",
                    "name": "PEP potential match",
                    "conditions": [{"field": "match_score", "operator": "gte", "value": 0.7}],
                    "rules": [{"outcome": "potential_match", "parameters": {"review_required": True}}],
                },
            ],
            "approval_required": False,
        },
        {
            "key": "kyc.sanctions.screening",
            "name": "Sanctions Screening Rules",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "clear", "parameters": {}}],
            "exceptions": [
                {
                    "id": "sanctions_block",
                    "name": "Sanctions block",
                    "conditions": [{"field": "match_score", "operator": "gte", "value": 0.9}],
                    "rules": [{"outcome": "block", "parameters": {"action": "block_onboarding"}}],
                },
                {
                    "id": "sanctions_potential",
                    "name": "Sanctions potential match",
                    "conditions": [{"field": "match_score", "operator": "gte", "value": 0.75}],
                    "rules": [{"outcome": "potential_match", "parameters": {"review_required": True}}],
                },
            ],
            "approval_required": False,
        },
        {
            "key": "kyc.periodic.review_interval",
            "name": "Periodic KYC Review Interval",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "schedule_review", "parameters": {"interval_days": 365}}],
            "exceptions": [
                {
                    "id": "high_risk_review",
                    "name": "High risk shorter interval",
                    "conditions": [{"field": "risk_class", "operator": "eq", "value": "high"}],
                    "rules": [{"outcome": "schedule_review", "parameters": {"interval_days": 180}}],
                },
                {
                    "id": "edd_review",
                    "name": "EDD shorter interval",
                    "conditions": [{"field": "due_diligence_level", "operator": "eq", "value": "enhanced"}],
                    "rules": [{"outcome": "schedule_review", "parameters": {"interval_days": 90}}],
                },
            ],
            "approval_required": False,
        },
        {
            "key": "kyc.approval.required_level",
            "name": "KYC Approval Levels",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "approve", "parameters": {"required_levels": 1}}],
            "exceptions": [
                {
                    "id": "edd_approval",
                    "name": "EDD requires two levels",
                    "conditions": [{"field": "due_diligence_level", "operator": "eq", "value": "enhanced"}],
                    "rules": [{"outcome": "approve", "parameters": {"required_levels": 2}}],
                },
                {
                    "id": "pep_approval",
                    "name": "PEP requires three levels",
                    "conditions": [{"field": "pep_status", "operator": "eq", "value": "confirmed"}],
                    "rules": [{"outcome": "approve", "parameters": {"required_levels": 3}}],
                },
            ],
            "approval_required": False,
        },
        {
            "key": "deposit.interest.rate",
            "name": "Deposit Interest Rate",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "apply_rate", "parameters": {"rate_annual": 2.5}}],
            "exceptions": [
                {
                    "id": "term_rate",
                    "name": "Term deposit higher rate",
                    "conditions": [{"field": "deposit_type", "operator": "eq", "value": "term"}],
                    "rules": [{"outcome": "apply_rate", "parameters": {"rate_annual": 5.0}}],
                },
                {
                    "id": "current_rate",
                    "name": "Current account lower rate",
                    "conditions": [{"field": "deposit_type", "operator": "eq", "value": "current"}],
                    "rules": [{"outcome": "apply_rate", "parameters": {"rate_annual": 0.5}}],
                },
            ],
            "approval_required": False,
        },
        {
            "key": "deposit.early_withdrawal.penalty",
            "name": "Early Withdrawal Penalty",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "apply_penalty", "parameters": {"penalty_pct": 1.0}}],
            "exceptions": [
                {
                    "id": "near_maturity_waive",
                    "name": "Waive penalty near maturity",
                    "conditions": [{"field": "days_to_maturity", "operator": "lte", "value": 7}],
                    "rules": [{"outcome": "waive_penalty", "parameters": {"penalty_pct": 0.0}}],
                },
                {
                    "id": "large_early_withdrawal",
                    "name": "Higher penalty for large early withdrawal",
                    "conditions": [{"field": "amount", "operator": "gte", "value": 50000}],
                    "rules": [{"outcome": "apply_penalty", "parameters": {"penalty_pct": 2.5}}],
                },
            ],
            "approval_required": False,
        },
        {
            "key": "deposit.approval.required_level",
            "name": "Deposit Transaction Approval Levels",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "approve", "parameters": {"required_levels": 1}}],
            "exceptions": [
                {
                    "id": "large_withdrawal",
                    "name": "Large withdrawal requires two levels",
                    "conditions": [
                        {"field": "transaction_type", "operator": "eq", "value": "withdrawal"},
                        {"field": "amount", "operator": "gte", "value": 10000},
                    ],
                    "rules": [{"outcome": "approve", "parameters": {"required_levels": 2}}],
                },
            ],
            "approval_required": False,
        },
        {
            "key": "deposit.term.maturity_notice",
            "name": "Term Deposit Maturity Notice",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "notify", "parameters": {"notice_days": 14}}],
            "approval_required": False,
        },
        {
            "key": "deposit.recurring.schedule",
            "name": "Recurring Deposit Schedule",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "schedule", "parameters": {"frequency": "monthly", "grace_days": 3}}],
            "approval_required": False,
        },
        {
            "key": "deposit.profit.distribution",
            "name": "Profit Distribution Rules",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "distribute", "parameters": {"profit_share_pct": 3.0}}],
            "approval_required": False,
        },
        {
            "key": "loan.interest.rate",
            "name": "Loan Interest Rate",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "apply_rate", "parameters": {"rate_annual": 12.0}}],
            "exceptions": [
                {
                    "id": "mortgage_rate",
                    "name": "Mortgage lower rate",
                    "conditions": [{"field": "loan_type", "operator": "eq", "value": "mortgage"}],
                    "rules": [{"outcome": "apply_rate", "parameters": {"rate_annual": 8.5}}],
                },
                {
                    "id": "microfinance_rate",
                    "name": "Microfinance rate",
                    "conditions": [{"field": "loan_type", "operator": "eq", "value": "microfinance"}],
                    "rules": [{"outcome": "apply_rate", "parameters": {"rate_annual": 18.0}}],
                },
            ],
            "approval_required": False,
        },
        {
            "key": "loan.approval.required_level",
            "name": "Loan Approval Levels",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "approve", "parameters": {"required_levels": 1}}],
            "exceptions": [
                {
                    "id": "large_loan",
                    "name": "Large loan requires two levels",
                    "conditions": [{"field": "amount", "operator": "gt", "value": 100000}],
                    "rules": [{"outcome": "approve", "parameters": {"required_levels": 2}}],
                },
            ],
            "approval_required": False,
        },
        {
            "key": "loan.penalty.late_payment",
            "name": "Late Payment Penalty",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "apply_penalty", "parameters": {"penalty_pct": 1.0}}],
            "approval_required": False,
        },
        {
            "key": "loan.restructure.rules",
            "name": "Loan Restructuring Rules",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"max_extensions": 2}}],
            "approval_required": False,
        },
        {
            "key": "loan.settlement.discount",
            "name": "Loan Settlement Discount",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "apply_discount", "parameters": {"discount_pct": 5.0}}],
            "approval_required": False,
        },
        {
            "key": "loan.early_closure.penalty",
            "name": "Early Closure Penalty",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "apply_penalty", "parameters": {"penalty_pct": 2.0}}],
            "approval_required": False,
        },
        {
            "key": "loan.credit_risk.threshold",
            "name": "Credit Risk Thresholds",
            "priority": 100,
            "conditions": [],
            "rules": [
                {
                    "outcome": "evaluate",
                    "parameters": {
                        "max_dti_ratio": 0.45,
                        "min_collateral_coverage_pct": 100,
                        "large_loan_threshold": 100000,
                    },
                }
            ],
            "approval_required": False,
        },
        {
            "key": "lending.debt_to_income_ratio",
            "name": "Debt-to-Income Ceiling",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "within_limit", "parameters": {"max_dti_ratio": 0.45}}],
            "approval_required": False,
        },
        {
            "key": "lending.collateral.haircut",
            "name": "Collateral Valuation Haircut",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "apply_haircut", "parameters": {"haircut_pct": 10.0}}],
            "approval_required": False,
        },
        {
            "key": "interest.calculation.method",
            "name": "Interest Calculation Method",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "apply_method", "parameters": {"method": "simple"}}],
            "exceptions": [
                {
                    "id": "term_compound",
                    "name": "Term deposits use compound",
                    "conditions": [{"field": "product_context", "operator": "eq", "value": "deposit"}],
                    "rules": [{"outcome": "apply_method", "parameters": {"method": "compound"}}],
                },
            ],
            "approval_required": False,
        },
        {
            "key": "interest.compounding.frequency",
            "name": "Compounding Frequency",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "apply", "parameters": {"periods_per_year": 12}}],
            "approval_required": False,
        },
        {
            "key": "interest.rate.fixed",
            "name": "Fixed Interest Rate",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "apply_rate", "parameters": {"rate_annual": 5.0}}],
            "approval_required": False,
        },
        {
            "key": "interest.rate.floating",
            "name": "Floating Interest Rate",
            "priority": 100,
            "conditions": [],
            "rules": [
                {
                    "outcome": "apply_rate",
                    "parameters": {"index_rate_annual": 4.0, "spread_bps": 150, "index_ref": "SOFR"},
                }
            ],
            "approval_required": False,
        },
        {
            "key": "interest.rate.promotional",
            "name": "Promotional Interest Rate",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "apply_rate", "parameters": {"promotional_rate_annual": 3.5, "duration_days": 90}}],
            "approval_required": False,
        },
        {
            "key": "interest.grace.period",
            "name": "Interest Grace Period",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "apply_grace", "parameters": {"grace_days": 7}}],
            "approval_required": False,
        },
        {
            "key": "interest.penalty.rate",
            "name": "Penalty Interest Rate",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "apply_penalty", "parameters": {"penalty_multiplier": 1.5}}],
            "approval_required": False,
        },
        {
            "key": "interest.profit_sharing",
            "name": "Profit Sharing Allocation",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "distribute", "parameters": {"profit_share_pct": 0.0}}],
            "approval_required": False,
        },
        {
            "key": "payment.transfer.daily_limit",
            "name": "Daily Transfer Limit",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "within_limit", "parameters": {"max_amount": 100000, "currency": "USD"}}],
            "approval_required": False,
        },
        {
            "key": "payment.transfer.single_limit",
            "name": "Single Transfer Limit",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "within_limit", "parameters": {"max_amount": 50000, "currency": "USD"}}],
            "approval_required": False,
        },
        {
            "key": "payment.approval.required_level",
            "name": "Transfer Approval Levels",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "approve", "parameters": {"required_levels": 1}}],
            "exceptions": [
                {
                    "id": "large_transfer",
                    "name": "Large transfer requires two levels",
                    "conditions": [{"field": "amount", "operator": "gt", "value": 25000}],
                    "rules": [{"outcome": "approve", "parameters": {"required_levels": 2}}],
                },
            ],
            "approval_required": False,
        },
        {
            "key": "payment.fraud.threshold",
            "name": "Payment Fraud Thresholds",
            "priority": 100,
            "conditions": [],
            "rules": [
                {
                    "outcome": "evaluate",
                    "parameters": {
                        "block_score": 30,
                        "review_score": 60,
                        "large_amount": 50000,
                        "velocity_limit": 10,
                    },
                }
            ],
            "approval_required": False,
        },
        {
            "key": "payment.fraud.velocity",
            "name": "Transfer Velocity Rules",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "monitor", "parameters": {"max_transfers_per_day": 20}}],
            "approval_required": False,
        },
        {
            "key": "payment.scheduled.execution",
            "name": "Scheduled Transfer Execution",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"max_schedule_days": 365}}],
            "approval_required": False,
        },
        {
            "key": "payment.standing_order.rules",
            "name": "Standing Order Rules",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"max_amount": 25000, "frequencies": ["daily", "weekly", "monthly"]}}],
            "approval_required": False,
        },
        {
            "key": "payment.real_time.settlement",
            "name": "Real-Time Payment Settlement",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "instant", "parameters": {"max_amount": 10000}}],
            "approval_required": False,
        },
        {
            "key": "payment.government.routing",
            "name": "Government Payment Routing",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "route", "parameters": {"routing_code": "GOV-TREASURY"}}],
            "approval_required": False,
        },
        {
            "key": "payment.salary.batch",
            "name": "Salary Transfer Batch Rules",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"max_items": 500, "max_total": 5000000}}],
            "approval_required": False,
        },
        {
            "key": "settlement.interbank.cutoff",
            "name": "Interbank Settlement Cutoff",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"cutoff_time": "16:00", "timezone": "UTC"}}],
            "approval_required": False,
        },
        {
            "key": "settlement.clearing.window",
            "name": "Clearing Window",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"window_hours": 4}}],
            "approval_required": False,
        },
        {
            "key": "settlement.match.tolerance",
            "name": "Reconciliation Match Tolerance",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"amount_tolerance": 0.01}}],
            "approval_required": False,
        },
        {
            "key": "settlement.retry.max_attempts",
            "name": "Settlement Exception Retry Limit",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"max_attempts": 3}}],
            "approval_required": False,
        },
        {
            "key": "settlement.adjustment.approval_level",
            "name": "Manual Adjustment Approval",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "approve", "parameters": {"required_levels": 1}}],
            "approval_required": False,
        },
        {
            "key": "settlement.reconciliation.auto_match",
            "name": "Automatic Reconciliation Matching",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"min_match_score": 0.7}}],
            "approval_required": False,
        },
        {
            "key": "settlement.exception.escalation",
            "name": "Exception Escalation Threshold",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "escalate", "parameters": {"after_retries": 3}}],
            "approval_required": False,
        },
        {
            "key": "branch.opening.checklist",
            "name": "Branch Opening Checklist",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"require_vault_check": True}}],
            "approval_required": False,
        },
        {
            "key": "branch.closing.checklist",
            "name": "Branch Closing Checklist",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"require_balance_reconciliation": True}}],
            "approval_required": False,
        },
        {
            "key": "branch.vault.limit",
            "name": "Branch Vault Limit",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"max_balance": 500000, "currency": "USD"}}],
            "approval_required": False,
        },
        {
            "key": "branch.cash.counter.limit",
            "name": "Cash Counter Limit",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"max_amount": 25000, "currency": "USD"}}],
            "approval_required": False,
        },
        {
            "key": "branch.kpi.targets",
            "name": "Branch KPI Targets",
            "priority": 100,
            "conditions": [],
            "rules": [
                {
                    "outcome": "allow",
                    "parameters": {
                        "transaction_volume": 1000,
                        "customer_wait_minutes": 5,
                        "default_target": 100,
                    },
                }
            ],
            "approval_required": False,
        },
        {
            "key": "branch.employee.max_assignments",
            "name": "Max Employee Assignments",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"max_assignments": 50}}],
            "approval_required": False,
        },
        {
            "key": "branch.cash.drawer.limit",
            "name": "Teller Cash Drawer Limit",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"max_drawer_balance": 10000, "currency": "USD"}}],
            "approval_required": False,
        },
        {
            "key": "branch.large_cash.transaction_threshold",
            "name": "Large Cash Transaction Threshold",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"threshold": 5000, "currency": "USD"}}],
            "approval_required": False,
        },
        {
            "key": "security.critical.approval_required",
            "name": "Critical Banking Action Approval",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "require_approval", "parameters": {"approval_amount": 10000, "four_eyes_amount": 100000, "required_approvals": 1, "four_eyes_levels": 2}}],
            "approval_required": False,
        },
        {
            "key": "security.transaction.limit",
            "name": "Security Transaction Limit",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"max_amount": 50000, "currency": "USD"}}],
            "approval_required": False,
        },
        {
            "key": "security.daily.limit",
            "name": "Security Daily Limit",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"max_daily": 100000, "currency": "USD"}}],
            "approval_required": False,
        },
        {
            "key": "security.velocity.limit",
            "name": "Security Velocity Limit",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"max_count": 50}}],
            "approval_required": False,
        },
        {
            "key": "security.device.trust",
            "name": "Device Trust Policy",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"require_trusted_device": False}}],
            "approval_required": False,
        },
        {
            "key": "security.risk.threshold",
            "name": "Risk Authentication Threshold",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"block_threshold": 30, "step_up_threshold": 60, "large_amount": 25000, "velocity_limit": 20}}],
            "approval_required": False,
        },
        {
            "key": "security.emergency.freeze",
            "name": "Emergency Freeze Authorization",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {}}],
            "approval_required": False,
        },
        {
            "key": "security.maker_checker.rules",
            "name": "Maker Checker Rules",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"allowed_roles": ["admin"], "allowed_permissions": ["*"]}}],
            "approval_required": False,
        },
        {
            "key": "security.four_eyes.levels",
            "name": "Four Eyes Approval Levels",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"required_levels": 2}}],
            "approval_required": False,
        },
        {
            "key": "security.session.timeout",
            "name": "Session Monitoring Timeout",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"timeout_minutes": 30}}],
            "approval_required": False,
        },
        {
            "key": "security.monitoring.threshold",
            "name": "Transaction Monitoring Threshold",
            "priority": 100,
            "conditions": [],
            "rules": [{"outcome": "allow", "parameters": {"alert_threshold": 40}}],
            "approval_required": False,
        },
    ],
    "tax": [
        {
            "key": "vat.rate",
            "name": "Standard VAT Rate",
            "priority": 100,
            "conditions": [{"field": "jurisdiction", "operator": "eq", "value": "IR"}],
            "rules": [{"outcome": "apply_rate", "parameters": {"rate": 0.09}}],
            "exceptions": [
                {
                    "id": "medical_exempt",
                    "name": "Medical exemption",
                    "conditions": [{"field": "product.category", "operator": "eq", "value": "medical"}],
                    "rules": [{"outcome": "apply_rate", "parameters": {"rate": 0.0}}],
                }
            ],
            "approval_required": False,
        },
    ],
    "exchange": [
        {
            "key": "trading.hours",
            "name": "Regular Trading Hours",
            "priority": 100,
            "conditions": [],
            "rules": [
                {
                    "outcome": "market_open",
                    "parameters": {"open": "09:00", "close": "17:00", "timezone": "Asia/Tehran"},
                }
            ],
            "approval_required": False,
        },
    ],
    "construction": [
        {
            "key": "safety.ppe_required",
            "name": "PPE Requirement on Site",
            "priority": 100,
            "conditions": [{"field": "site.active", "operator": "eq", "value": True}],
            "rules": [{"outcome": "require_ppe", "parameters": {"items": ["helmet", "vest", "boots"]}}],
            "approval_required": False,
        },
    ],
    "government": [
        {
            "key": "procurement.threshold",
            "name": "Public Procurement Approval Threshold",
            "priority": 100,
            "conditions": [],
            "rules": [
                {
                    "outcome": "approval_required",
                    "parameters": {"threshold_amount": 50000, "currency": "USD"},
                }
            ],
            "approval_required": False,
        },
    ],
}


def default_effective_from() -> datetime:
    return datetime.now(UTC)
