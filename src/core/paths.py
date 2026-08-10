"""
Enterprise Product Analytics Platform
Centralized Project Paths
"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
WAREHOUSE_DIR = DATA_DIR / "warehouse"

SOURCE_DIR = PROJECT_ROOT / "src"
TESTS_DIR = PROJECT_ROOT / "tests"
CONFIG_DIR = PROJECT_ROOT / "configs"
LOG_DIR = PROJECT_ROOT / "logs"
REPORTS_DIR = PROJECT_ROOT / "reports"
MODELS_DIR = PROJECT_ROOT / "models"


DATABASE_PATH = WAREHOUSE_DIR / "analytics.duckdb"


def ensure_project_directories():
    directories = [
        DATA_DIR,
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        WAREHOUSE_DIR,
        LOG_DIR,
        REPORTS_DIR,
        MODELS_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def get_database_path():
    return DATABASE_PATH