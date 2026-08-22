"""Technical debt registry must not resolve launch P0s without evidence."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
REGISTRY = REPO / "docs" / "meos" / "execution" / "MEOS_TECHNICAL_DEBT_REGISTRY.v1.yaml"
P0_OPEN = ("TD-G26-PROD-CLUSTER", "TD-G25-DIRTY-SHA", "TD-G27-ROLLBACK")


def test_p0_debt_is_not_resolved():
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in data["items"]}
    for debt_id in P0_OPEN:
        assert by_id[debt_id]["status"] != "RESOLVED"
        assert by_id[debt_id]["priority"] == "P0"
    assert data["open_critical_count"] >= 3
    stub = by_id["TD-SDK-STUB-SUCCESS"]
    assert stub["status"] == "RESOLVED"
