"""Currency Exchange → General Ledger posting bridge (Financial Kernel side)."""
from __future__ import annotations

import logging

from contexts.financial_kernel.application.service import FinancialKernelApplicationService

logger = logging.getLogger(__name__)


class ExchangePostingBridge:
    """ACL bridge — FX deal/fee/remittance envelopes → kernel posting intents."""

    def __init__(self, kernel: FinancialKernelApplicationService) -> None:
        self._kernel = kernel

    async def handle_deal_settled(self, envelope: dict) -> None:
        if str(envelope.get("event_name") or "") != "currency_exchange.deal.settled":
            return
        logger.debug("exchange deal settled envelope received — posting deferred to FX ACL")

    async def handle_fee_charged(self, envelope: dict) -> None:
        if str(envelope.get("event_name") or "") != "currency_exchange.fee.charged":
            return
        logger.debug("exchange fee charged envelope received")

    async def handle_deal_reversed(self, envelope: dict) -> None:
        if str(envelope.get("event_name") or "") != "currency_exchange.deal.reversed":
            return
        logger.debug("exchange deal reversed envelope received")

    async def handle_remittance_settled(self, envelope: dict) -> None:
        if str(envelope.get("event_name") or "") != "currency_exchange.remittance.settled":
            return
        logger.debug("exchange remittance settled envelope received")
