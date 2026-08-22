"""Registry YAML vs startup honesty sets — no silent ACTIVE ghosts."""
from __future__ import annotations

from pathlib import Path

import yaml

from core.presentation.api.startup_registry import (
    BLUEPRINT_CONTEXT_IDS,
    DEFERRED_CONTEXT_IDS,
    EMPTY_INDUSTRY_SCAFFOLD_IDS,
)

ROOT = Path(__file__).resolve().parents[3]
YAML_PATH = ROOT / "docs" / "meos" / "execution" / "MEOS_APPLICATION_REGISTRY.v1.yaml"


def _load_yaml() -> dict:
    return yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))


def _load_apps() -> list[dict]:
    data = _load_yaml()
    apps = data.get("applications") or []
    assert isinstance(apps, list)
    return apps


def test_registry_yaml_exists():
    assert YAML_PATH.is_file()


def test_blueprint_ids_are_blueprint_status():
    apps = {a["id"]: a for a in _load_apps()}
    for ctx in sorted(BLUEPRINT_CONTEXT_IDS):
        assert ctx in apps, f"blueprint {ctx} missing from registry YAML"
        assert apps[ctx]["status"] == "BLUEPRINT"


def test_empty_scaffolds_are_coming_soon():
    apps = {a["id"]: a for a in _load_apps()}
    for ctx in sorted(EMPTY_INDUSTRY_SCAFFOLD_IDS):
        assert ctx in apps, f"scaffold {ctx} missing from registry YAML"
        assert apps[ctx]["status"] in {"SCAFFOLDED", "coming_soon", "COMING_SOON"}


def test_nav_items_have_application_entries():
    data = _load_yaml()
    apps = {a["id"] for a in data.get("applications") or []}
    missing: list[str] = []
    for group in data.get("nav_groups") or []:
        for item in group.get("items") or []:
            if item not in apps:
                missing.append(item)
    assert missing == [], f"nav IDs without application entries: {missing}"


def test_deferred_missing_packages_not_active():
    apps = {a["id"]: a for a in _load_apps()}
    forbidden = {"ACTIVE", "PRODUCTION_READY"}
    extra_deferred = DEFERRED_CONTEXT_IDS - EMPTY_INDUSTRY_SCAFFOLD_IDS
    for ctx in extra_deferred:
        if ctx in apps:
            assert apps[ctx]["status"] not in forbidden
