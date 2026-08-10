"""
Enterprise Product Analytics Platform
Application Settings
"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
WAREHOUSE_DIR = DATA_DIR / "warehouse"

DATABASE_PATH = WAREHOUSE_DIR / "analytics.duckdb"

LOG_DIR = PROJECT_ROOT / "logs"

APP_NAME = "Enterprise Product Analytics Platform"
APP_ENV = "development"
DEBUG = True