"""
Enterprise Product Analytics Platform
CSV Loader

Loads the RetailRocket dataset safely with
logging, validation and reusable functions.
"""

from pathlib import Path
from typing import Dict

import pandas as pd
from loguru import logger


class CSVLoader:
    """
    Enterprise CSV Loader
    """

    def __init__(self, data_directory: str = "data/raw/retailrocket"):
        self.data_directory = Path(data_directory)

        self.files = {
            "events": self.data_directory / "events.csv",
            "item_properties_part1": self.data_directory / "item_properties_part1.csv",
            "item_properties_part2": self.data_directory / "item_properties_part2.csv",
            "category_tree": self.data_directory / "category_tree.csv",
        }

    def _check_file_exists(self, file_path: Path):
        """Check if file exists."""

        if not file_path.exists():
            raise FileNotFoundError(f"{file_path} not found.")

    def load_csv(self, name: str) -> pd.DataFrame:
        """
        Load a single csv file.
        """

        file_path = self.files[name]

        self._check_file_exists(file_path)

        logger.info(f"Loading {file_path.name}")

        dataframe = pd.read_csv(file_path)

        logger.success(
            f"{file_path.name} loaded successfully "
            f"({len(dataframe):,} rows)"
        )

        return dataframe

    def load_all(self) -> Dict[str, pd.DataFrame]:
        """
        Load all datasets.
        """

        datasets = {}

        for dataset in self.files:
            datasets[dataset] = self.load_csv(dataset)

        logger.success("All datasets loaded successfully.")

        return datasets


if __name__ == "__main__":

    loader = CSVLoader()

    datasets = loader.load_all()

    for name, dataframe in datasets.items():

        print("=" * 70)
        print(name.upper())
        print(dataframe.head())