
"""
Enterprise Product Analytics Platform
KPI Analytics Engine

Calculates executive KPIs from the analytics warehouse.
"""

from pathlib import Path

import duckdb
from loguru import logger


DATABASE_PATH = Path("data/warehouse/analytics.duckdb")


class KPIEngine:

    def __init__(self):

        self.conn = duckdb.connect(str(DATABASE_PATH))

    def execute(self, query: str):

        return self.conn.sql(query).fetchone()[0]

    def total_events(self):

        return self.execute("""
        SELECT COUNT(*)
        FROM fact_events
        """)

    def total_users(self):

        return self.execute("""
        SELECT COUNT(DISTINCT visitor_id)
        FROM fact_events
        """)

    def total_transactions(self):

        return self.execute("""
        SELECT COUNT(*)
        FROM fact_events
        WHERE event='transaction'
        """)

    def total_add_to_cart(self):

        return self.execute("""
        SELECT COUNT(*)
        FROM fact_events
        WHERE event='addtocart'
        """)

    def total_views(self):

        return self.execute("""
        SELECT COUNT(*)
        FROM fact_events
        WHERE event='view'
        """)

    def conversion_rate(self):

        return self.execute("""
        SELECT
            ROUND(
                100.0 *
                COUNT(CASE WHEN event='transaction' THEN 1 END)
                /
                COUNT(*),
                2
            )
        FROM fact_events
        """)

    def average_events_per_user(self):

        return self.execute("""
        SELECT ROUND(
            COUNT(*) * 1.0 /
            COUNT(DISTINCT visitor_id),
            2
        )
        FROM fact_events
        """)

    def dashboard(self):

        logger.info("=" * 80)
        logger.info("EXECUTIVE KPI DASHBOARD")
        logger.info("=" * 80)

        print(f"Total Events           : {self.total_events():,}")
        print(f"Total Users            : {self.total_users():,}")
        print(f"Transactions           : {self.total_transactions():,}")
        print(f"Add To Cart            : {self.total_add_to_cart():,}")
        print(f"Views                  : {self.total_views():,}")
        print(f"Conversion Rate (%)    : {self.conversion_rate()}")
        print(f"Events / User          : {self.average_events_per_user()}")

        logger.success("KPI Dashboard Generated")

        self.conn.close()


if __name__ == "__main__":

    KPIEngine().dashboard()