"""
Enterprise Product Analytics Platform
Schema Validator

Validates RetailRocket datasets before preprocessing.
"""

from typing import Dict

import pandas as pd
from loguru import logger


class SchemaValidator:
    """
    Enterprise Dataset Validator
    """

    REQUIRED_COLUMNS = {
        "events": [
            "timestamp",
            "visitorid",
            "event",
            "itemid",
            "transactionid",
        ],
        "item_properties_part1": [
            "timestamp",
            "itemid",
            "property",
            "value",
        ],
        "item_properties_part2": [
            "timestamp",
            "itemid",
            "property",
            "value",
        ],
        "category_tree": [
            "categoryid",
            "parentid",
        ],
    }

    def validate(self, name: str, dataframe: pd.DataFrame) -> None:
        """
        Validate one dataset.
        """

        logger.info(f"Validating {name}")

        self.check_columns(name, dataframe)

        self.dataset_summary(name, dataframe)

        logger.success(f"{name} validation completed.\n")

    def check_columns(self, name: str, dataframe: pd.DataFrame):

        required = self.REQUIRED_COLUMNS[name]

        missing = []

        for column in required:
            if column not in dataframe.columns:
                missing.append(column)

        if missing:
            raise ValueError(f"{name} missing columns: {missing}")

        logger.success("Required columns verified.")

    def dataset_summary(self, name: str, dataframe: pd.DataFrame):

        print("=" * 80)
        print(name.upper())
        print("=" * 80)

        print(f"Rows              : {len(dataframe):,}")
        print(f"Columns           : {len(dataframe.columns)}")

        memory = dataframe.memory_usage(deep=True).sum() / 1024 / 1024

        print(f"Memory (MB)       : {memory:.2f}")

        print("\nData Types")
        print(dataframe.dtypes)

        print("\nMissing Values")
        print(dataframe.isnull().sum())

        print("\nDuplicate Rows")
        print(dataframe.duplicated().sum())

        print("\nUnique Values")
        print(dataframe.nunique())

        print("\nFirst Five Rows")
        print(dataframe.head())

        print()