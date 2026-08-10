"""
Enterprise Product Analytics Platform
Application Constants
"""

APP_NAME = "Enterprise Product Analytics Platform"
APP_VERSION = "1.0.0"

DATABASE_PATH = "data/warehouse/analytics.duckdb"

EVENT_VIEW = "view"
EVENT_ADD_TO_CART = "addtocart"
EVENT_TRANSACTION = "transaction"

VALID_EVENTS = (
    EVENT_VIEW,
    EVENT_ADD_TO_CART,
    EVENT_TRANSACTION,
)

DEFAULT_TOP_N = 10
DEFAULT_RETENTION_MONTHS = 6