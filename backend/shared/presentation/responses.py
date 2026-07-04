"""Standard API response envelope."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    code: str
    message: str
    field: str | None = None
    details: dict[str, Any] = Field(default_factory=dict)


class ResponseMeta(BaseModel):
    correlation_id: str | None = None
    request_id: str | None = None
    locale: str | None = None
    direction: str | None = None
    page: int | None = None
    page_size: int | None = None
    total: int | None = None


class ApiResponse(BaseModel):
    data: Any | None = None
    meta: ResponseMeta = Field(default_factory=ResponseMeta)
    errors: list[ErrorDetail] | None = None


def success_response(data: Any, **meta: Any) -> dict:
    return ApiResponse(data=data, meta=ResponseMeta(**meta)).model_dump(exclude_none=True)


def error_response(code: str, message: str, field: str | None = None, **meta: Any) -> dict:
    return ApiResponse(
        data=None,
        meta=ResponseMeta(**meta),
        errors=[ErrorDetail(code=code, message=message, field=field)],
    ).model_dump(exclude_none=True)
