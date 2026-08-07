"""
Enterprise Product Analytics Platform
DuckDB Warehouse Loader
"""

from pathlib import Path

import duckdb
from loguru import logger

from src.data_processing.loaders.csv_loader import CSVLoader
from src.data_processing.cleaners.events_cleaner import EventsCleaner


DATABASE_PATH = Path("data/warehouse/analytics.duckdb")


class DuckDBLoader:

    def __init__(self):

        self.conn = duckdb.connect(str(DATABASE_PATH))

        self.loader = CSVLoader()

        self.cleaner = EventsCleaner()

    def load_events(self):

        logger.info("Loading Events...")

        events = self.loader.load_csv("events")

        events = self.cleaner.clean(events)

        self.conn.register("events_df", events)

        self.conn.execute("""
        DELETE FROM fact_events;
        """)

        self.conn.execute("""
        INSERT INTO fact_events

        SELECT

            row_number() OVER() AS event_id,

            visitorid,

            itemid,

            event,

            transactionid,

            event_datetime,

            year,

            month,

            day,

            hour,

            week,

            quarter,

            weekday,

            is_weekend

        FROM events_df
        """)

        logger.success("Events Loaded Successfully")

    def run(self):

        logger.info("=" * 80)
        logger.info("DuckDB Warehouse Loader")
        logger.info("=" * 80)

        self.load_events()

        self.conn.close()

        logger.success("Warehouse Load Completed")


if __name__ == "__main__":

    DuckDBLoader().run()