"""Enterprise financial dimension engine — catalog, normalization, validation."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.financial_dimension import DimensionType

DIMENSION_CATALOG: dict[str, dict] = {
    DimensionType.COMPANY.value: {
        "label": "Company",
        "description": "Legal entity or operating company",
        "hierarchical": True,
    },
    DimensionType.BRANCH.value: {
        "label": "Branch",
        "description": "Branch or regional office",
        "hierarchical": True,
    },
    DimensionType.DEPARTMENT.value: {
        "label": "Department",
        "description": "Organizational department",
        "hierarchical": True,
    },
    DimensionType.PROJECT.value: {
        "label": "Project",
        "description": "Project or initiative",
        "hierarchical": True,
    },
    DimensionType.COST_CENTER.value: {
        "label": "Cost Center",
        "description": "Cost accumulation unit",
        "hierarchical": True,
    },
    DimensionType.PROFIT_CENTER.value: {
        "label": "Profit Center",
        "description": "Profit responsibility unit",
        "hierarchical": True,
    },
    DimensionType.FUND.value: {
        "label": "Fund",
        "description": "Restricted or designated fund",
        "hierarchical": True,
    },
    DimensionType.GRANT.value: {
        "label": "Grant",
        "description": "Grant or sponsorship program",
        "hierarchical": False,
    },
    DimensionType.FACULTY.value: {
        "label": "Faculty",
        "description": "University faculty or school",
        "hierarchical": True,
    },
    DimensionType.HOSPITAL.value: {
        "label": "Hospital",
        "description": "Hospital or medical facility",
        "hierarchical": True,
    },
    DimensionType.WARD.value: {
        "label": "Ward",
        "description": "Hospital ward or clinical unit",
        "hierarchical": True,
    },
    DimensionType.CONSTRUCTION_SITE.value: {
        "label": "Construction Site",
        "description": "Construction project site",
        "hierarchical": False,
    },
    DimensionType.WAREHOUSE.value: {
        "label": "Warehouse",
        "description": "Warehouse or storage location",
        "hierarchical": True,
    },
    DimensionType.COUNTRY.value: {
        "label": "Country",
        "description": "Country or jurisdiction",
        "hierarchical": False,
    },
    DimensionType.CURRENCY.value: {
        "label": "Currency",
        "description": "Transaction or reporting currency axis",
        "hierarchical": False,
    },
    DimensionType.BUSINESS_UNIT.value: {
        "label": "Business Unit",
        "description": "Business unit or division",
        "hierarchical": True,
    },
}

LEGACY_DIMENSION_FIELDS = ("cost_center", "profit_center", "department", "project", "branch")


def list_dimension_catalog() -> list[dict]:
    return [{"dimension_type": key, **meta} for key, meta in DIMENSION_CATALOG.items()]


def get_dimension_definition(dimension_type: str) -> dict:
    definition = DIMENSION_CATALOG.get(dimension_type)
    if not definition:
        raise KeyError(f"unknown_dimension_type:{dimension_type}")
    return definition


def normalize_dimension_type(dimension_type: str) -> str:
    normalized = dimension_type.strip().lower()
    if normalized == "hospital_ward":
        return DimensionType.WARD.value
    return normalized


def build_dimension_lookup(values: list[dict]) -> dict[str, dict[str, dict]]:
    lookup: dict[str, dict[str, dict]] = {}
    for value in values:
        dim_type = normalize_dimension_type(value.get("dimension_type", ""))
        code = str(value.get("code", "")).upper()
        if not dim_type or not code:
            continue
        lookup.setdefault(dim_type, {})[code] = value
    return lookup


def extract_line_dimensions(line: dict) -> dict[str, str]:
    dims: dict[str, str] = {}
    existing = line.get("dimensions")
    if isinstance(existing, dict):
        for key, val in existing.items():
            if val:
                dims[normalize_dimension_type(key)] = str(val).strip().upper()
    for field in LEGACY_DIMENSION_FIELDS:
        val = line.get(field)
        if val:
            dim_type = normalize_dimension_type(field)
            if field == "branch":
                dim_type = DimensionType.BRANCH.value
            dims[dim_type] = str(val).strip().upper()
    return dims


def enrich_journal_line(line: dict) -> dict:
    enriched = dict(line)
    dims = extract_line_dimensions(line)
    enriched["dimensions"] = dims
    if dims.get(DimensionType.COST_CENTER.value):
        enriched["cost_center"] = dims[DimensionType.COST_CENTER.value]
    if dims.get(DimensionType.PROFIT_CENTER.value):
        enriched["profit_center"] = dims[DimensionType.PROFIT_CENTER.value]
    if dims.get(DimensionType.DEPARTMENT.value):
        enriched["department"] = dims[DimensionType.DEPARTMENT.value]
    if dims.get(DimensionType.PROJECT.value):
        enriched["project"] = dims[DimensionType.PROJECT.value]
    return enriched


def enrich_journal_lines(lines: list[dict]) -> list[dict]:
    return [enrich_journal_line(line) for line in lines]


def merge_header_dimensions(
    lines: list[dict],
    *,
    organization_id: str | None = None,
    branch_id: str | None = None,
) -> list[dict]:
    merged: list[dict] = []
    for line in lines:
        enriched = enrich_journal_line(line)
        dims = dict(enriched.get("dimensions", {}))
        if organization_id and DimensionType.COMPANY.value not in dims:
            dims[DimensionType.COMPANY.value] = organization_id.strip().upper()
        if branch_id and DimensionType.BRANCH.value not in dims:
            dims[DimensionType.BRANCH.value] = branch_id.strip().upper()
        enriched["dimensions"] = dims
        merged.append(enriched)
    return merged


def validate_line_dimensions(
    lines: list[dict],
    *,
    lookup: dict[str, dict[str, dict]],
    strict: bool = True,
) -> tuple[bool, list[dict]]:
    issues: list[dict] = []
    for idx, line in enumerate(lines):
        dims = extract_line_dimensions(line)
        for dim_type, code in dims.items():
            if dim_type not in DIMENSION_CATALOG:
                if strict:
                    issues.append(
                        {
                            "line_index": idx,
                            "dimension_type": dim_type,
                            "code": code,
                            "error": "unknown_dimension_type",
                        }
                    )
                continue
            type_values = lookup.get(dim_type, {})
            if not type_values:
                continue
            value = type_values.get(code.upper())
            if not value:
                issues.append(
                    {
                        "line_index": idx,
                        "dimension_type": dim_type,
                        "code": code,
                        "error": "unknown_dimension_code",
                    }
                )
            elif not value.get("is_active", True):
                issues.append(
                    {
                        "line_index": idx,
                        "dimension_type": dim_type,
                        "code": code,
                        "error": "inactive_dimension",
                    }
                )
    return len(issues) == 0, issues


def summarize_line_dimensions(lines: list[dict]) -> dict:
    all_types: set[str] = set()
    per_line_counts: list[int] = []
    for line in lines:
        dims = extract_line_dimensions(line)
        all_types.update(dims.keys())
        per_line_counts.append(len(dims))
    return {
        "line_count": len(lines),
        "dimension_types_used": sorted(all_types),
        "max_dimensions_per_line": max(per_line_counts) if per_line_counts else 0,
        "avg_dimensions_per_line": round(
            sum(per_line_counts) / max(len(per_line_counts), 1), 2
        ),
        "unlimited_supported": True,
    }
