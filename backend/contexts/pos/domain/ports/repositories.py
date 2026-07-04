"""POS repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.pos.domain.aggregates.pos_sale import PosSale
from contexts.pos.domain.aggregates.receipt import Receipt
from contexts.pos.domain.aggregates.shift import Shift
from contexts.pos.domain.aggregates.terminal import Terminal
from shared.domain.value_objects.unique_id import UniqueId


class ITerminalRepository(ABC):
    @abstractmethod
    async def save(self, terminal: Terminal) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, terminal_id: UniqueId) -> Terminal | None: ...

    @abstractmethod
    async def find_by_code(self, tenant_id: str, terminal_code: str) -> Terminal | None: ...


class IShiftRepository(ABC):
    @abstractmethod
    async def save(self, shift: Shift) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, shift_id: UniqueId) -> Shift | None: ...

    @abstractmethod
    async def find_open_by_terminal(self, tenant_id: str, terminal_id: UniqueId) -> Shift | None: ...


class IPosSaleRepository(ABC):
    @abstractmethod
    async def save(self, sale: PosSale) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, sale_id: UniqueId) -> PosSale | None: ...


class IReceiptRepository(ABC):
    @abstractmethod
    async def save(self, receipt: Receipt) -> None: ...

    @abstractmethod
    async def find_by_sale(self, tenant_id: str, sale_id: UniqueId) -> Receipt | None: ...
