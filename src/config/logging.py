"""
Enterprise Product Analytics Platform
Logging Configuration
"""

import sys
from pathlib import Path

from loguru import logger


def configure_logging(log_directory="logs"):

    log_directory = Path(log_directory)
    log_directory.mkdir(parents=True, exist_ok=True)

    logger.remove()

    logger.add(
        sys.stderr,
        level="INFO",
        enqueue=True,
    )

    logger.add(
        log_directory / "application.log",
        level="INFO",
        rotation="10 MB",
        retention="30 days",
        enqueue=True,
    )

    return logger