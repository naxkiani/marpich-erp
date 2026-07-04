"""Default module configuration keys merged on activation."""
from __future__ import annotations

MODULE_DEFAULTS: dict[str, dict] = {
    "healthcare.patient-management": {"max_patients_per_ward": 50},
    "healthcare.billing": {"auto_post_billing": True},
    "platform.finance": {"fiscal_year_start": "01-01"},
    "retail.pos": {"offline_mode": False},
}
