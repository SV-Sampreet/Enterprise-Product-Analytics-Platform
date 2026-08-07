"""
Enterprise Product Analytics Platform
Warehouse Table Creator

Creates the DuckDB analytics warehouse.
"""

from pathlib import Path
import duckdb
from loguru import logger


DATABASE_PATH = Path("data/warehouse/analytics.duckdb")


class WarehouseBuilder:

    def __init__(self):

        DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

        self.conn = duckdb.connect(str(DATABASE_PATH))

    def create_fact_events(self):

        logger.info("Creating fact_events")

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS fact_events (

            event_id BIGINT,

            visitor_id BIGINT,

            item_id BIGINT,

            event VARCHAR,

            transaction_id BIGINT,

            timestamp TIMESTAMP,

            year INTEGER,

            month INTEGER,

            day INTEGER,

            hour INTEGER,

            week INTEGER,

            quarter INTEGER,

            weekday VARCHAR,

            is_weekend BOOLEAN

        );
        """)

    def create_dim_users(self):

        logger.info("Creating dim_users")

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS dim_users (

            visitor_id BIGINT PRIMARY KEY

        );
        """)

    def create_dim_items(self):

        logger.info("Creating dim_items")

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS dim_items (

            item_id BIGINT PRIMARY KEY

        );
        """)

    def create_dim_categories(self):

        logger.info("Creating dim_categories")

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS dim_categories (

            category_id BIGINT PRIMARY KEY,

            parent_id BIGINT

        );
        """)

    def create_dim_time(self):

        logger.info("Creating dim_time")

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS dim_time (

            timestamp TIMESTAMP PRIMARY KEY,

            year INTEGER,

            month INTEGER,

            day INTEGER,

            hour INTEGER,

            week INTEGER,

            quarter INTEGER,

            weekday VARCHAR,

            is_weekend BOOLEAN

        );
        """)

    def build(self):

        logger.info("=" * 80)
        logger.info("Building Analytics Warehouse")
        logger.info("=" * 80)

        self.create_fact_events()
        self.create_dim_users()
        self.create_dim_items()
        self.create_dim_categories()
        self.create_dim_time()

        logger.success("Warehouse Created Successfully")

        self.conn.close()


if __name__ == "__main__":

    WarehouseBuilder().build()