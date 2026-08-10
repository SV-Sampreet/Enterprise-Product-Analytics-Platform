"""
Enterprise Product Analytics Platform
Analytics API Layer

Provides a lightweight API service for accessing analytics results.
"""

from pathlib import Path

import duckdb
from loguru import logger


DATABASE_PATH = Path("data/warehouse/analytics.duckdb")


class AnalyticsAPI:

    def __init__(self):
        self.conn = duckdb.connect(str(DATABASE_PATH), read_only=True)

    def health(self):
        return {
            "status": "healthy",
            "database": str(DATABASE_PATH),
        }

    def get_kpis(self):
        query = """
        SELECT
            COUNT(*) AS total_events,
            COUNT(DISTINCT visitor_id) AS total_users,
            COUNT(CASE WHEN event = 'transaction' THEN 1 END) AS transactions,
            COUNT(CASE WHEN event = 'addtocart' THEN 1 END) AS add_to_cart,
            COUNT(CASE WHEN event = 'view' THEN 1 END) AS views
        FROM fact_events
        """

        return self.conn.sql(query).df().to_dict(orient="records")[0]

    def get_event_summary(self):
        query = """
        SELECT
            event,
            COUNT(*) AS event_count,
            COUNT(DISTINCT visitor_id) AS unique_users
        FROM fact_events
        GROUP BY event
        ORDER BY event_count DESC
        """

        return self.conn.sql(query).df().to_dict(orient="records")

    def close(self):
        self.conn.close()


def main():

    logger.info("=" * 80)
    logger.info("ANALYTICS API")
    logger.info("=" * 80)

    api = AnalyticsAPI()

    print("\nHEALTH")
    print(api.health())

    print("\nKPIs")
    print(api.get_kpis())

    print("\nEVENT SUMMARY")
    print(api.get_event_summary())

    api.close()

    logger.success("Analytics API Completed")


if __name__ == "__main__":
    main()