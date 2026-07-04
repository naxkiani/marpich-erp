"""Base application service — marker for use-case layer."""
from __future__ import annotations

from abc import ABC


class BaseApplicationService(ABC):
    """Subclass in bounded contexts; kernel provides no business use cases."""
