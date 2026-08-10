"""
Enterprise Product Analytics Platform
Generic Data Loader
"""

from pathlib import Path

import pandas as pd
from loguru import logger


class DataLoader:

    def __init__(self, data_directory="data/raw"):
        self.data_directory = Path(data_directory)

    def load_csv(self, filename):
        path = self.data_directory / filename

        if not path.exists():
            raise FileNotFoundError(f"Dataset not found: {path}")

        logger.info(f"Loading {filename}")

        dataframe = pd.read_csv(path)

        logger.success(
            f"{filename} loaded successfully ({len(dataframe):,} rows)"
        )

        return dataframe

    def load_multiple(self, filenames):
        datasets = {}

        for filename in filenames:
            datasets[filename] = self.load_csv(filename)

        return datasets