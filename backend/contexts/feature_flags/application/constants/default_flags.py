"""Default feature flags seeded on tenant provision."""
from __future__ import annotations

DEFAULT_FLAGS: tuple[tuple[str, str, bool, dict[str, bool] | None], ...] = (
    ("saved_listings", "Saved Listings", False, None),
    ("image_attachments", "Image Attachments", True, None),
    ("multi_org", "Multi Organization", False, {"bank": True}),
    (
        "advanced_analytics",
        "Advanced Analytics",
        False,
        {"hospital": True, "bank": True, "university": True},
    ),
    ("digital_exchange.enabled", "Digital Exchange Layer (Master)", False, None),
    ("digital_exchange.digital_wallets", "Digital Wallets Extension", False, None),
    ("digital_exchange.open_banking", "Open Banking APIs Extension", False, None),
    ("digital_exchange.cross_border_payments", "Cross-Border Payments Extension", False, None),
    ("digital_exchange.cbdc", "CBDC Extension", False, None),
    ("digital_exchange.stablecoins", "Stablecoins Extension", False, None),
    ("digital_exchange.tokenized_assets", "Tokenized Assets Extension", False, None),
    (
        "digital_exchange.licensed_digital_asset_services",
        "Licensed Digital Asset Services Extension",
        False,
        None,
    ),
    ("digital_exchange.real_time_settlement", "Real-Time Settlement Extension", False, None),
    ("digital_exchange.iso_20022", "ISO 20022 Messaging Extension", False, None),
)
