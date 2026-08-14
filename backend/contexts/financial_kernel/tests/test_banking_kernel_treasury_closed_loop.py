"""P1 — banking deposit + treasury transfer post through Financial Kernel (beyond document smoke)."""
from __future__ import annotations

import pytest

from contexts.financial_kernel.application.banking_posting_bridge import BankingPostingBridge
from contexts.financial_kernel.application.treasury_posting_bridge import TreasuryPostingBridge
from contexts.financial_kernel.container import (
    get_financial_kernel_service,
    reset_financial_kernel_service,
)


@pytest.fixture(autouse=True)
def _reset_kernel(monkeypatch):
    monkeypatch.setattr("contexts.financial_kernel.container.use_postgres", lambda: False)
    monkeypatch.setattr(
        "shared.infrastructure.messaging.idempotency.use_postgres",
        lambda: False,
    )
    from shared.infrastructure.messaging.event_fabric import EventFabric
    from shared.infrastructure.messaging.idempotency import InMemoryProcessedEventStore

    monkeypatch.setattr(
        "shared.infrastructure.messaging.event_bus.get_processed_event_store",
        lambda: InMemoryProcessedEventStore(),
    )

    EventFabric.reset_dev_state()
    reset_financial_kernel_service()
    yield
    reset_financial_kernel_service()
    EventFabric.reset_dev_state()


@pytest.mark.asyncio
async def test_banking_deposit_and_treasury_transfer_post_kernel_journals():
    kernel = get_financial_kernel_service()
    await kernel.handle_tenant_provisioned(
        {"tenant_id": "p1-money", "payload": {"industry_pack": "bank"}}
    )
    deposits = await kernel.resolve_account_code("p1-money", "customer_deposits")
    cash = await kernel.resolve_account_code("p1-money", "cash_reserves")
    assert deposits.succeeded
    assert cash.succeeded

    banking = BankingPostingBridge(kernel)
    await banking.handle_deposit_posted(
        {
            "tenant_id": "p1-money",
            "correlation_id": "c-dep-1",
            "payload": {
                "account_id": "acc-1",
                "account_number": "1001",
                "amount": 250,
                "currency": "USD",
                "transaction_ref": "txn-1",
            },
        }
    )
    journals = (await kernel.list_journals("p1-money")).unwrap()
    bank_posted = [j for j in journals if j.get("source_context") == "banking"]
    assert len(bank_posted) >= 1
    assert any(j.get("source_document_id") == "acc-1" for j in bank_posted)

    treasury = TreasuryPostingBridge(kernel)
    await treasury.handle_transfer_executed(
        {
            "tenant_id": "p1-money",
            "correlation_id": "c-tr-1",
            "payload": {
                "transfer_id": "tr-1",
                "amount": 50,
                "currency": "USD",
                "from_account_type": "cash",
                "to_account_type": "bank",
            },
        }
    )
    journals = (await kernel.list_journals("p1-money")).unwrap()
    treasury_posted = [j for j in journals if j.get("source_context") == "treasury"]
    assert len(treasury_posted) >= 1
    assert any(j.get("source_document_id") == "tr-1" for j in treasury_posted)
