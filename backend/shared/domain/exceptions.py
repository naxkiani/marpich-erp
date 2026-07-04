"""Common domain and application exceptions."""
from __future__ import annotations


class MarpichError(Exception):
    """Base kernel exception."""


class DomainValidationError(MarpichError):
  """Value object or invariant violation."""


class NotFoundError(MarpichError):
    def __init__(self, code: str, message: str | None = None) -> None:
        self.code = code
        super().__init__(message or code)


class ConflictError(MarpichError):
    def __init__(self, code: str, message: str | None = None) -> None:
        self.code = code
        super().__init__(message or code)


class ForbiddenError(MarpichError):
    def __init__(self, code: str = "forbidden", message: str | None = None) -> None:
        self.code = code
        super().__init__(message or code)


class UnauthorizedError(MarpichError):
    def __init__(self, code: str = "unauthorized", message: str | None = None) -> None:
        self.code = code
        super().__init__(message or code)
