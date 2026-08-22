"""Plugin SDK example manifests vs PLUGIN_MANIFEST.v1.json."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

REPO = Path(__file__).resolve().parents[3]
MANIFEST_SCHEMA = REPO / "docs" / "architecture" / "plugins" / "PLUGIN_MANIFEST.v1.json"
EXAMPLES = REPO / "packages" / "plugin-sdk" / "examples"


@pytest.fixture(scope="module")
def validator() -> Draft202012Validator:
    schema = json.loads(MANIFEST_SCHEMA.read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


@pytest.mark.parametrize(
    "rel",
    [
        "com.marpich.demo-sales-widget/marpich.plugin.json",
        "com.marpich.demo-report-pack/marpich.plugin.json",
    ],
)
def test_seed_examples_match_manifest_schema(validator: Draft202012Validator, rel: str):
    payload = json.loads((EXAMPLES / rel).read_text(encoding="utf-8"))
    errors = sorted(e.message for e in validator.iter_errors(payload))
    assert not errors, errors


def test_invalid_plugin_id_is_rejected(validator: Draft202012Validator):
    payload = json.loads(
        (EXAMPLES / "com.marpich.demo-sales-widget" / "marpich.plugin.json").read_text(
            encoding="utf-8"
        )
    )
    payload["pluginId"] = "not-a-reverse-dns"
    errors = list(validator.iter_errors(payload))
    assert errors
