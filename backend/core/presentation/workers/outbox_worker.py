"""Dedicated outbox dispatcher process for production worker replicas."""
from __future__ import annotations

import asyncio
import logging

from shared.infrastructure.messaging.dispatcher import get_outbox_dispatcher

logger = logging.getLogger("marpich.outbox_worker")


async def _run() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    dispatcher = get_outbox_dispatcher()
    await dispatcher.start()
    logger.info("outbox worker started")
    try:
        while True:
            await asyncio.sleep(60)
    finally:
        await dispatcher.stop()
        logger.info("outbox worker stopped")


def main() -> None:
    asyncio.run(_run())


if __name__ == "__main__":
    main()
