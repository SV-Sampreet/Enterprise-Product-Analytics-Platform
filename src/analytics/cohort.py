"""
Enterprise Product Analytics Platform

Cohort Analytics
"""

from pathlib import Path

import duckdb
from loguru import logger

DATABASE_PATH = Path("data/warehouse/analytics.duckdb")


class CohortAnalytics:

    def __init__(self):
        self.conn = duckdb.connect(str(DATABASE_PATH))

    def acquisition_cohorts(self):

        query = """
        WITH first_visit AS (
            SELECT
                visitor_id,
                DATE_TRUNC('month', MIN(timestamp)) AS cohort_month
            FROM fact_events
            GROUP BY visitor_id
        )

        SELECT
            cohort_month,
            COUNT(*) AS users
        FROM first_visit
        GROUP BY cohort_month
        ORDER BY cohort_month
        """

        return self.conn.sql(query).df()

    def report(self):

        logger.info("=" * 80)
        logger.info("USER ACQUISITION COHORTS")
        logger.info("=" * 80)

        df = self.acquisition_cohorts()

        print(df)

        logger.success("Cohort Analysis Completed")

        self.conn.close()


if __name__ == "__main__":
    CohortAnalytics().report()