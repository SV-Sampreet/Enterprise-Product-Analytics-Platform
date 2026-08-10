"""
Enterprise Product Analytics Platform
Configuration Management
"""

from pathlib import Path

from src.config.settings import (
    APP_ENV,
    APP_NAME,
    DATABASE_PATH,
    DEBUG,
    LOG_DIR,
    PROJECT_ROOT,
)


class AppConfig:

    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.app_name = APP_NAME
        self.environment = APP_ENV
        self.debug = DEBUG
        self.database_path = Path(DATABASE_PATH)
        self.log_dir = Path(LOG_DIR)

    def ensure_directories(self):

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.log_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def summary(self):

        return {
            "app_name": self.app_name,
            "environment": self.environment,
            "debug": self.debug,
            "database": str(self.database_path),
            "log_directory": str(self.log_dir),
        }


config = AppConfig()