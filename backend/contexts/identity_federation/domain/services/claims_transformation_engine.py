"""Claims transformation engine — policy-driven attribute/claims mapping."""
from __future__ import annotations

from typing import Any


TRANSFORM_TYPES = ("direct", "template", "lookup", "concat", "split", "lowercase", "uppercase")


def transform_claims(
    *,
    raw_claims: dict[str, Any],
    mappings: list[dict],
) -> dict[str, Any]:
    """Transform external claims to internal claims using configured mappings."""
    result: dict[str, Any] = {}
    sorted_mappings = sorted(mappings, key=lambda m: m.get("priority", 100))
    for mapping in sorted_mappings:
        if not mapping.get("enabled", True):
            continue
        source = mapping.get("source_claim", "")
        target = mapping.get("target_claim", "")
        if not source or not target:
            continue
        value = raw_claims.get(source)
        if value is None:
            continue
        transform_type = mapping.get("transform_type", "direct")
        config = mapping.get("transform_config") or {}
        result[target] = _apply_transform(value, transform_type, config)
    return result


def _apply_transform(value: Any, transform_type: str, config: dict) -> Any:
    if transform_type == "direct":
        return value
    if transform_type == "template":
        template = config.get("template", "{value}")
        return template.replace("{value}", str(value))
    if transform_type == "lookup":
        lookup = config.get("lookup", {})
        return lookup.get(str(value), config.get("default", value))
    if transform_type == "concat":
        prefix = config.get("prefix", "")
        suffix = config.get("suffix", "")
        return f"{prefix}{value}{suffix}"
    if transform_type == "split":
        sep = config.get("separator", "@")
        parts = str(value).split(sep)
        index = int(config.get("index", 0))
        return parts[index] if len(parts) > index else value
    if transform_type == "lowercase":
        return str(value).lower()
    if transform_type == "uppercase":
        return str(value).upper()
    return value


def map_attributes(
    *,
    external_attributes: dict[str, Any],
    attribute_mappings: list[dict],
) -> dict[str, Any]:
    """Map external directory attributes to internal identity attributes."""
    result: dict[str, Any] = {}
    for mapping in attribute_mappings:
        if not mapping.get("enabled", True):
            continue
        ext = mapping.get("external_attribute", "")
        internal = mapping.get("internal_attribute", "")
        if not ext or not internal:
            continue
        value = external_attributes.get(ext)
        if value is None and mapping.get("required"):
            if mapping.get("default_value") is not None:
                result[internal] = mapping["default_value"]
            continue
        if value is not None:
            result[internal] = value
    return result
