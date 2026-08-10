"""
Enterprise Product Analytics Platform
Data Quality Validator
"""

import pandas as pd


class DataValidator:

    def validate_not_empty(self, dataframe: pd.DataFrame):

        if dataframe.empty:
            raise ValueError("DataFrame is empty")

        return True

    def validate_required_columns(
        self,
        dataframe: pd.DataFrame,
        required_columns,
    ):

        missing = [
            column
            for column in required_columns
            if column not in dataframe.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required columns: {missing}"
            )

        return True

    def validate_no_duplicate_columns(
        self,
        dataframe: pd.DataFrame,
    ):

        duplicated = dataframe.columns[
            dataframe.columns.duplicated()
        ].tolist()

        if duplicated:
            raise ValueError(
                f"Duplicate columns detected: {duplicated}"
            )

        return True

    def validate(
        self,
        dataframe,
        required_columns=None,
    ):

        self.validate_not_empty(dataframe)

        self.validate_no_duplicate_columns(dataframe)

        if required_columns:
            self.validate_required_columns(
                dataframe,
                required_columns,
            )

        return True