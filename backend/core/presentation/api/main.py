"""
Marpich ERP — FastAPI composition root.

Default export uses full profile. Use create_app(profile=...) for subsets.
"""
from core.presentation.api.app_factory import create_app

app = create_app()
