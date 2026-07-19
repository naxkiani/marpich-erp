"""P200-B10 OHS APIs / Events / CQRS foundation + bus/saga tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.identity_federation.application.commands.ohs_commands import (
    AdvanceFederationSagaCommand,
    DispatchCommandBusCommand,
    DispatchQueryBusCommand,
    IngestInboxCommand,
    PublishOhsEventCommand,
    StartFederationSagaCommand,
    handle_advance_federation_saga,
    handle_dispatch_command,
    handle_dispatch_query,
    handle_ingest_inbox,
    handle_publish_ohs_event,
    handle_start_federation_saga,
)
from contexts.identity_federation.application.queries.ohs_queries import handle_get_ohs_surface
from contexts.identity_federation.container import reset_identity_federation_service
from contexts.identity_federation.domain.services.eiftp_ohs_apis_events_cqrs import (
    validate_ohs_apis_events_cqrs_foundation,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_federation_service()
    yield
    reset_identity_federation_service()


@pytest.mark.unit
def test_ohs_foundation_passes():
    result = validate_ohs_apis_events_cqrs_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["foundation_for"] == "P200-B11"
    assert result["graphql_ohs_extended"] is True
    assert result["grpc_ohs_extended"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_command_bus_idempotency_and_query_bus():
    first = await handle_dispatch_command(
        DispatchCommandBusCommand(
            tenant_id="tenant-a",
            name="EvaluateZeroTrust",
            payload={
                "identity_verified": True,
                "device_trusted": True,
                "risk_score": 10,
                "trust_score": 80,
            },
            idempotency_key="idt-1",
        )
    )
    assert first["idempotent_replay"] is False
    assert first["result"]["authz_permit_deny"] is None
    second = await handle_dispatch_command(
        DispatchCommandBusCommand(
            tenant_id="tenant-a",
            name="EvaluateZeroTrust",
            payload={"identity_verified": False},
            idempotency_key="idt-1",
        )
    )
    assert second["idempotent_replay"] is True
    assert second["result"]["gate_action"] == first["result"]["gate_action"]

    query = await handle_dispatch_query(
        DispatchQueryBusCommand(tenant_id="tenant-a", name="GetOhsCatalog")
    )
    assert query["result"]["adr"] == 224


@pytest.mark.unit
@pytest.mark.asyncio
async def test_outbox_publish_inbox_dedupe_and_saga():
    published = await handle_publish_ohs_event(
        PublishOhsEventCommand(
            tenant_id="tenant-a",
            event_name="federation.saga.completed",
            payload={"demo": True},
        )
    )
    assert published["event_name"] == "federation.saga.completed"
    assert published["status"] in ("published", "pending")

    a = await handle_ingest_inbox(
        IngestInboxCommand(
            tenant_id="tenant-a",
            event_id="evt-1",
            event_name="federation.provider.registered",
            consumer_id="acl-1",
        )
    )
    b = await handle_ingest_inbox(
        IngestInboxCommand(
            tenant_id="tenant-a",
            event_id="evt-1",
            event_name="federation.provider.registered",
            consumer_id="acl-1",
        )
    )
    assert a["duplicate"] is False
    assert b["duplicate"] is True

    saga = await handle_start_federation_saga(
        StartFederationSagaCommand(
            tenant_id="tenant-a",
            saga_type="federation_trust_establishment",
            context={"partner_tenant_id": "tenant-b"},
        )
    )
    assert saga["status"] == "running"
    advanced = await handle_advance_federation_saga(
        AdvanceFederationSagaCommand(
            tenant_id="tenant-a", saga_ref=saga["saga_ref"], step_ok=True
        )
    )
    # 3 steps; first completed on start → advancing twice more completes
    advanced = await handle_advance_federation_saga(
        AdvanceFederationSagaCommand(
            tenant_id="tenant-a", saga_ref=saga["saga_ref"], step_ok=True
        )
    )
    assert advanced["status"] == "completed"

    failed = await handle_start_federation_saga(
        StartFederationSagaCommand(
            tenant_id="tenant-a",
            saga_type="identity_provider_activation",
        )
    )
    compensated = await handle_advance_federation_saga(
        AdvanceFederationSagaCommand(
            tenant_id="tenant-a", saga_ref=failed["saga_ref"], step_ok=False
        )
    )
    assert compensated["status"] == "compensated"


@pytest.mark.unit
def test_surface_and_no_sibling_bc():
    surface = handle_get_ohs_surface()
    assert surface["adr"] == 224
    assert surface["validation"]["passed"] is True
    assert "outbox" in surface["patterns"]
    assert not (REPO_ROOT / "backend/contexts/eiftp").exists()
