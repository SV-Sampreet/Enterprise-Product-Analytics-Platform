"""
Enterprise Product Analytics Platform
A/B Testing Analytics Engine
"""

from pathlib import Path

import duckdb
from loguru import logger


DATABASE_PATH = Path("data/warehouse/analytics.duckdb")


class ABTestingAnalytics:

    def __init__(self):
        self.conn = duckdb.connect(str(DATABASE_PATH))

    def experiment_summary(self):
        query = """
        SELECT
            event,
            COUNT(*) AS events,
            COUNT(DISTINCT visitor_id) AS users
        FROM fact_events
        GROUP BY event
        ORDER BY events DESC
        """

        return self.conn.sql(query).df()

    def report(self):
        logger.info("=" * 80)
        logger.info("A/B TESTING ANALYTICS")
        logger.info("=" * 80)

        df = self.experiment_summary()

        print(df.to_string(index=False))

        logger.success("A/B Testing Analysis Completed")

        self.conn.close()


if __name__ == "__main__":
    ABTestingAnalytics().report()
