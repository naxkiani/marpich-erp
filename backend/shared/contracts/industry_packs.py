"""Industry pack catalog — synced from packages/shared-kernel industry-packs.ts."""
from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

_CATALOG_PATH = Path(__file__).with_name("industry_packs.json")


@dataclass(frozen=True, slots=True)
class IndustryPack:
    pack_id: str
    display_name: str
    description: str
    required_modules: tuple[str, ...]
    optional_modules: tuple[str, ...]
    compliance_frameworks: tuple[str, ...]
    default_locale: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "pack_id": self.pack_id,
            "display_name": self.display_name,
            "description": self.description,
            "required_modules": list(self.required_modules),
            "optional_modules": list(self.optional_modules),
            "compliance_frameworks": list(self.compliance_frameworks),
            "default_locale": self.default_locale,
        }


def _parse_pack(raw: dict[str, Any]) -> IndustryPack:
    return IndustryPack(
        pack_id=raw["packId"],
        display_name=raw["displayName"],
        description=raw["description"],
        required_modules=tuple(raw["requiredModules"]),
        optional_modules=tuple(raw["optionalModules"]),
        compliance_frameworks=tuple(raw["complianceFrameworks"]),
        default_locale=raw["defaultLocale"],
    )


@lru_cache(maxsize=1)
def _load_catalog() -> dict[str, IndustryPack]:
    data = json.loads(_CATALOG_PATH.read_text(encoding="utf-8"))
    return {key: _parse_pack(value) for key, value in data.items()}


def get_industry_pack(pack_id: str) -> IndustryPack | None:
    return _load_catalog().get(pack_id)


def list_industry_packs() -> list[IndustryPack]:
    return list(_load_catalog().values())


def resolve_modules_for_pack(pack_id: str, optional: list[str] | None = None) -> list[str]:
    pack = get_industry_pack(pack_id)
    if not pack:
        return []
    enabled = set(pack.required_modules)
    if optional:
        allowed = set(pack.optional_modules)
        enabled.update(m for m in optional if m in allowed)
    return sorted(enabled)
