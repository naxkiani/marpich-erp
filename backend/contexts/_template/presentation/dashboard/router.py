"""Dashboard read endpoints — query-only, no business rules."""
from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/module-id/dashboard", tags=["ModuleId Dashboard"])
