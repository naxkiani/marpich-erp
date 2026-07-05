"""Enterprise account hierarchy tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.financial_kernel.container import get_financial_kernel_service, reset_financial_kernel_service
from contexts.financial_kernel.domain.services.account_hierarchy_engine import (
    detect_duplicates,
    generate_visual_account_tree,
    validate_tree_integrity,
)
from contexts.financial_kernel.domain.services.coa_tree_service import flatten_tree
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    reset_financial_kernel_service()
    get_financial_kernel_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "hier@kernel.dev", "password": "SecurePass123!", "display_name": "Hierarchy Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "hier@kernel.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_provision_creates_default_tree():
    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": "hier-prov", "payload": {"industry_pack": "retail"}}
    )
    trees = (await svc.list_account_trees("hier-prov")).unwrap()
    assert len(trees) == 1
    assert trees[0]["is_default"] is True
    assert trees[0]["account_count"] > 0


def test_integrity_and_duplicate_detection():
    integrity = validate_tree_integrity([])
    assert integrity["valid"] is True

    class _Acct:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    accounts = [
        _Acct(id="1", code="100", name="A", account_key="a", parent_account_id=None, tenant_id="t", level=0, tree_path="a", account_category=type("C", (), {"value": "asset"})(), account_type="cash", is_posting=True, display_order=0),
        _Acct(id="2", code="100", name="B", account_key="b", parent_account_id=None, tenant_id="t", level=0, tree_path="b", account_category=type("C", (), {"value": "asset"})(), account_type="cash", is_posting=True, display_order=0),
    ]
    dups = detect_duplicates(accounts)  # type: ignore[arg-type]
    assert len(dups) == 1
    assert dups[0]["issue_type"] == "duplicate_code"


@pytest.mark.asyncio
async def test_create_tree_apply_template_and_visual(client):
    slug = "hier-tree"
    headers = await _auth_headers(client, slug)

    create = await client.post(
        "/api/v1/financial-kernel/account-hierarchy/trees",
        headers=headers,
        json={"name": "Management COA", "tree_type": "management"},
    )
    assert create.status_code == 201
    tree_id = create.json()["data"]["id"]

    apply = await client.post(
        f"/api/v1/financial-kernel/account-hierarchy/trees/{tree_id}/templates/apply",
        headers=headers,
        json={"template_key": "coa.enterprise", "template_type": "industry"},
    )
    assert apply.status_code == 201
    assert apply.json()["data"]["account_count"] > 10

    visual = await client.get(
        f"/api/v1/financial-kernel/account-hierarchy/trees/{tree_id}/visual",
        headers=headers,
    )
    assert visual.status_code == 200
    data = visual.json()["data"]
    assert "mermaid" in data
    assert data["node_count"] > 0
    assert data["visual"]["nodes"]


@pytest.mark.asyncio
async def test_drag_drop_move_and_versioning(client):
    slug = "hier-move"
    headers = await _auth_headers(client, slug)
    svc = get_financial_kernel_service()

    tree = (await svc.create_account_tree(tenant_id=slug, name="Move Tree")).unwrap()
    tree_id = tree["id"]
    await svc.apply_template_to_tree(
        tenant_id=slug,
        tree_id=tree_id,
        template_key="coa.retail",
        template_type="industry",
    )
    structure = (await svc.get_hierarchy_structure(slug, tree_id)).unwrap()
    flat = flatten_tree(structure)
    assets = next(n for n in flat if n["account_key"] == "assets")
    cash = next(n for n in flat if n["account_key"] == "pos_cash")

    move = await client.post(
        f"/api/v1/financial-kernel/account-hierarchy/trees/{tree_id}/move",
        headers=headers,
        json={"account_id": cash["id"], "new_parent_id": assets["id"], "position": 1},
    )
    assert move.status_code == 200
    moved = move.json()["data"]["account"]
    assert moved["parent_account_id"] == assets["id"]
    assert moved["level"] == 1

    versions = await client.get(
        f"/api/v1/financial-kernel/account-hierarchy/trees/{tree_id}/versions",
        headers=headers,
    )
    assert versions.status_code == 200
    assert len(versions.json()["data"]) >= 2


@pytest.mark.asyncio
async def test_search_filters_validate_import_export(client):
    slug = "hier-ops"
    headers = await _auth_headers(client, slug)
    svc = get_financial_kernel_service()

    tree = (await svc.create_account_tree(tenant_id=slug, name="Ops Tree")).unwrap()
    tree_id = tree["id"]
    await svc.apply_template_to_tree(
        tenant_id=slug,
        tree_id=tree_id,
        template_key="coa.retail",
        template_type="industry",
    )

    search = await client.get(
        f"/api/v1/financial-kernel/account-hierarchy/trees/{tree_id}/search",
        headers=headers,
        params={"q": "cash", "is_posting": True},
    )
    assert search.status_code == 200
    assert len(search.json()["data"]) >= 1

    validate = await client.get(
        f"/api/v1/financial-kernel/account-hierarchy/trees/{tree_id}/validate",
        headers=headers,
    )
    assert validate.status_code == 200
    assert validate.json()["data"]["valid"] is True

    export_resp = await client.get(
        f"/api/v1/financial-kernel/account-hierarchy/trees/{tree_id}/export",
        headers=headers,
    )
    assert export_resp.status_code == 200
    rows = export_resp.json()["data"]["rows"]
    assert len(rows) > 0

    import_resp = await client.post(
        f"/api/v1/financial-kernel/account-hierarchy/trees/{tree_id}/import",
        headers=headers,
        json={
            "rows": [
                {
                    "code": "CUSTOM-99",
                    "name": "Custom Leaf",
                    "account_category": "asset",
                    "account_key": "custom_leaf",
                    "parent_code": rows[0]["code"],
                    "is_posting": True,
                }
            ]
        },
    )
    assert import_resp.status_code == 201
    assert import_resp.json()["data"]["imported_count"] == 1


@pytest.mark.asyncio
async def test_ai_optimize_and_multiple_trees(client):
    slug = "hier-multi"
    headers = await _auth_headers(client, slug)
    svc = get_financial_kernel_service()

    primary = (await svc.create_account_tree(tenant_id=slug, name="Primary", is_default=True)).unwrap()
    statutory = (await svc.create_account_tree(tenant_id=slug, name="Statutory", tree_type="statutory")).unwrap()
    await svc.apply_template_to_tree(
        tenant_id=slug,
        tree_id=primary["id"],
        template_key="coa.enterprise",
        template_type="industry",
    )

    trees = await client.get("/api/v1/financial-kernel/account-hierarchy/trees", headers=headers)
    assert trees.status_code == 200
    assert len(trees.json()["data"]) == 2

    ai = await client.get(
        f"/api/v1/financial-kernel/account-hierarchy/trees/{primary['id']}/ai-optimize",
        headers=headers,
    )
    assert ai.status_code == 200
    assert "optimization_score" in ai.json()["data"]
    assert ai.json()["data"]["recommendation"] in ("optimal", "review", "restructure")

    templates = await client.get(
        "/api/v1/financial-kernel/account-hierarchy/templates",
        headers=headers,
    )
    assert templates.status_code == 200
    assert "industry" in templates.json()["data"]
    assert statutory["id"]


@pytest.mark.asyncio
async def test_unlimited_depth_in_tree(client):
    slug = "hier-depth"
    headers = await _auth_headers(client, slug)
    svc = get_financial_kernel_service()
    tree = (await svc.create_account_tree(tenant_id=slug, name="Deep Tree")).unwrap()
    tree_id = tree["id"]

    import_resp = await client.post(
        f"/api/v1/financial-kernel/account-hierarchy/trees/{tree_id}/import",
        headers=headers,
        json={
            "rows": [
                {"code": "L0", "name": "Root", "account_category": "asset", "account_key": "root"},
                {"code": "L1", "name": "L1", "account_category": "asset", "parent_code": "L0"},
                {"code": "L2", "name": "L2", "account_category": "asset", "parent_code": "L1"},
                {"code": "L3", "name": "L3", "account_category": "asset", "parent_code": "L2"},
                {"code": "L4", "name": "L4", "account_category": "asset", "parent_code": "L3"},
            ]
        },
    )
    assert import_resp.status_code == 201
    structure = (await svc.get_hierarchy_structure(slug, tree_id)).unwrap()
    flat = flatten_tree(structure)
    deepest = max(flat, key=lambda n: n["level"])
    assert deepest["level"] == 4

    visual = generate_visual_account_tree(structure)
    assert visual["max_depth"] >= 5
