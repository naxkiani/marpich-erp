"""P355 productization must not fake customers, payments, G26, or production tenants."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
CERT = EXEC / "MEOS_P313_CERTIFICATION_REPORT.md"
MASTER = EXEC / "MEOS_EXECUTION_MASTER_PLAN.md"
G26 = REPO / "scripts" / "meos-ext-g26-readiness.py"
DOC = EXEC / "MEOS_P355_PRODUCTIZATION.md"
ONBOARD = EXEC / "MEOS_CUSTOMER_ONBOARDING.md"
LICENSE = EXEC / "MEOS_LICENSE_MODEL.v1.yaml"
EDITION = EXEC / "MEOS_EDITION_MODEL.v1.yaml"
COMPAT = EXEC / "MEOS_VERSION_COMPATIBILITY.v1.yaml"
READY = REPO / "scripts" / "meos-product-readiness.py"
ENGINE = REPO / "scripts" / "meos_product_engine.py"
COMMERCIAL = REPO / "infrastructure" / "launch" / "commercial"


def test_p355_contracts_exist():
    for path in (DOC, ONBOARD, LICENSE, EDITION, COMPAT, READY, ENGINE):
        assert path.is_file(), path
    for name in ("DEMO", "SELF_HOSTED", "VPS", "KUBERNETES", "CLOUD_READY"):
        assert (COMMERCIAL / name / "MEOS_PACKAGE.yaml").is_file()
        text = (COMMERCIAL / name / "MEOS_PACKAGE.yaml").read_text(encoding="utf-8")
        assert "secrets: none" in text or "secrets: none" in text.replace('"', "")
    license_doc = yaml.safe_load(LICENSE.read_text(encoding="utf-8"))
    assert license_doc["payment_execution"] == "READY_FOR_CREDENTIALS"
    assert license_doc["fake_transactions"] == "FORBIDDEN"
    assert license_doc["g26_ready"] is False
    editions = yaml.safe_load(EDITION.read_text(encoding="utf-8"))
    assert editions["client_side_entitlement_trust"] == "FORBIDDEN"
    assert "community" in editions["editions"]
    assert editions["production_certified"] is False


def test_p355_onboarding_does_not_create_production_tenants():
    spec = importlib.util.spec_from_file_location("meos_product_engine", ENGINE)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    plan = mod.onboarding_plan(authorize_create_tenant=False, production=True)
    assert plan["production_tenant_created"] is False
    assert plan["g26_ready"] is False
    assert any("PRODUCTION_TENANT" in item or "PLAN_ONLY" in item for item in plan["blocked"])
    product = mod.product_identity()
    assert product["commercial_release"] is False
    assert product["g26_ready"] is False
    assert "47258dfd-dirty" not in str(product.get("source_commit"))


def test_p355_product_readiness_does_not_set_g26(monkeypatch):
    spec = importlib.util.spec_from_file_location(
        "meos_product_readiness", READY
    )
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    data = mod.evaluate()
    assert data["g26_ready"] is False
    assert data["production_certified"] is False
    assert data["p0"] == 1
    assert data["p313"] == "NOT_CERTIFIED"
    assert data["go_live_authorization"] == "NOT_APPROVED"
    assert data["payment_execution"] == "READY_FOR_CREDENTIALS"
    assert data["PRODUCTIZATION_LAYER_READY"] is True
    if data.get("product", {}).get("image_digest") == "NOT_AVAILABLE":
        assert data["PRODUCT_READY"] is False


def test_p355_docs_isolate_g26():
    assert "P355" in CERT.read_text(encoding="utf-8")
    assert "P355" in MASTER.read_text(encoding="utf-8")
    assert "NOT_APPROVED" in DOC.read_text(encoding="utf-8")
    assert G26.is_file()
    profile = yaml.safe_load((EXEC / "MEOS_CUSTOMER_DEPLOYMENT_PROFILE.v1.yaml").read_text(encoding="utf-8"))
    assert profile["customer_id"] == "NOT_AVAILABLE"
    assert profile["fake_customer"] == "FORBIDDEN"
    market = yaml.safe_load((EXEC / "MEOS_MARKETPLACE_REQUIREMENTS.v1.yaml").read_text(encoding="utf-8"))
    assert market["fake_listings"] == "FORBIDDEN"
    assert market["implemented_integrations"] == []
