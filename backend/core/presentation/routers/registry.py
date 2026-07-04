"""
Dynamic router registry — mounts module presentation layers.

Each module exposes a FastAPI APIRouter from its presentation layer.
Never import application/domain across module boundaries.
"""
from fastapi import FastAPI

# from modules.platform.identity.presentation.router import router as identity_router
# from modules.platform.tenant.presentation.router import router as tenant_router


def register_module_routers(app: FastAPI) -> None:
    """Mount all enabled module routers. Filter by tenant industry pack at runtime."""
    # app.include_router(identity_router, prefix="/api/v1", tags=["Identity"])
    # app.include_router(tenant_router, prefix="/api/v1", tags=["Tenant"])
    pass
