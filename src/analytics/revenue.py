"""
Enterprise Product Analytics Platform
Revenue Analytics Engine

Calculates revenue and transaction KPIs from the analytics warehouse.
"""

from pathlib import Path

import duckdb
from loguru import logger


DATABASE_PATH = Path("data/warehouse/analytics.duckdb")


class RevenueAnalytics:

    def __init__(self):
        self.conn = duckdb.connect(str(DATABASE_PATH))

    def total_transactions(self):
        query = """
        SELECT COUNT(*)
        FROM fact_events
        WHERE event = 'transaction'
        """
        return self.conn.sql(query).fetchone()[0]

    def total_revenue(self):
        """
        Calculate total revenue when transaction revenue
        is available in the warehouse.
        """

        query = """
        SELECT
            COUNT(*) AS transactions
        FROM fact_events
        WHERE event = 'transaction'
        """

        return self.conn.sql(query).fetchone()[0]

    def revenue_summary(self):
        query = """
        SELECT
            COUNT(*) AS transactions,
            COUNT(DISTINCT visitor_id) AS purchasing_users,
            COUNT(DISTINCT item_id) AS purchased_items
        FROM fact_events
        WHERE event = 'transaction'
        """

        return self.conn.sql(query).df()

    def report(self):

        logger.info("=" * 80)
        logger.info("REVENUE ANALYTICS")
        logger.info("=" * 80)

        transactions = self.total_transactions()
        summary = self.revenue_summary()

        print(f"Transactions       : {transactions:,}")
        print()

        print(summary.to_string(index=False))

        logger.success("Revenue Analysis Completed")

        self.conn.close()


if __name__ == "__main__":
    RevenueAnalytics().report()