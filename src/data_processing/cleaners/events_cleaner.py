"""
Enterprise Product Analytics Platform
Events Cleaner

Cleans and standardizes the RetailRocket events dataset.
"""

from __future__ import annotations

import pandas as pd
from loguru import logger


class EventsCleaner:
    """
    Cleans the events dataset and prepares it
    for feature engineering and warehouse loading.
    """

    VALID_EVENTS = {
        "view",
        "addtocart",
        "transaction",
    }

    def clean(self, dataframe: pd.DataFrame) -> pd.DataFrame:

        logger.info("Starting Events Cleaning Pipeline")

        df = dataframe.copy()

        df = self.remove_duplicates(df)
        df = self.convert_timestamp(df)
        df = self.validate_events(df)
        df = self.handle_missing_values(df)
        df = self.create_time_features(df)

        logger.success("Events cleaning completed.")

        return df

    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:

        before = len(df)

        df = df.drop_duplicates()

        removed = before - len(df)

        logger.info(f"Removed {removed:,} duplicate rows")

        return df

    def convert_timestamp(self, df: pd.DataFrame) -> pd.DataFrame:

        logger.info("Converting timestamps")

        df["event_datetime"] = pd.to_datetime(
            df["timestamp"],
            unit="ms",
        )

        return df

    def validate_events(self, df: pd.DataFrame) -> pd.DataFrame:

        logger.info("Validating event types")

        before = len(df)

        df = df[df["event"].isin(self.VALID_EVENTS)]

        removed = before - len(df)

        logger.info(f"Removed {removed:,} invalid events")

        return df

    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:

        logger.info("Checking missing values")

        # transactionid is allowed to be null
        # for non-purchase events.

        return df

    def create_time_features(self, df: pd.DataFrame) -> pd.DataFrame:

        logger.info("Creating time features")

        dt = df["event_datetime"]

        df["year"] = dt.dt.year
        df["month"] = dt.dt.month
        df["day"] = dt.dt.day

        df["hour"] = dt.dt.hour

        df["weekday"] = dt.dt.day_name()

        df["week"] = dt.dt.isocalendar().week.astype(int)

        df["quarter"] = dt.dt.quarter

        df["is_weekend"] = dt.dt.weekday >= 5

        return df

    def report(self, df: pd.DataFrame):

        print("\n" + "=" * 80)
        print("EVENTS CLEANING REPORT")
        print("=" * 80)

        print(f"Rows          : {len(df):,}")
        print(f"Columns       : {len(df.columns)}")

        print("\nColumns")

        for column in df.columns:
            print(f"• {column}")

        print("\nMissing Values")

        print(df.isnull().sum())

        print("=" * 80)


if __name__ == "__main__":

    from src.data_processing.loaders.csv_loader import CSVLoader

    loader = CSVLoader()

    events = loader.load_csv("events")

    cleaner = EventsCleaner()

    clean_events = cleaner.clean(events)

    cleaner.report(clean_events)

    print(clean_events.head())