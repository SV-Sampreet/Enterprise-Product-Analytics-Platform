"""
Enterprise Product Analytics Platform
Retention Analytics Engine

Calculates monthly user retention from the analytics warehouse.
"""

from pathlib import Path

import duckdb
from loguru import logger


DATABASE_PATH = Path("data/warehouse/analytics.duckdb")


class RetentionAnalytics:

    def __init__(self):
        self.conn = duckdb.connect(str(DATABASE_PATH))

    def monthly_retention(self):
        """
        Calculate monthly retention based on each user's
        first active month.
        """

        query = """
        WITH user_activity AS (
            SELECT DISTINCT
                visitor_id,
                DATE_TRUNC('month', timestamp) AS activity_month
            FROM fact_events
            WHERE visitor_id IS NOT NULL
        ),

        user_cohorts AS (
            SELECT
                visitor_id,
                MIN(activity_month) AS cohort_month
            FROM user_activity
            GROUP BY visitor_id
        ),

        cohort_activity AS (
            SELECT
                c.cohort_month,
                a.activity_month,
                COUNT(DISTINCT a.visitor_id) AS active_users
            FROM user_cohorts c
            JOIN user_activity a
                ON c.visitor_id = a.visitor_id
            GROUP BY
                c.cohort_month,
                a.activity_month
        ),

        cohort_sizes AS (
            SELECT
                cohort_month,
                COUNT(DISTINCT visitor_id) AS cohort_users
            FROM user_cohorts
            GROUP BY cohort_month
        )

        SELECT
            ca.cohort_month,
            ca.activity_month,
            ca.active_users,
            cs.cohort_users,
            ROUND(
                100.0 * ca.active_users / cs.cohort_users,
                2
            ) AS retention_rate
        FROM cohort_activity ca
        JOIN cohort_sizes cs
            ON ca.cohort_month = cs.cohort_month
        ORDER BY
            ca.cohort_month,
            ca.activity_month
        """

        return self.conn.sql(query).df()

    def report(self):

        logger.info("=" * 80)
        logger.info("USER RETENTION ANALYTICS")
        logger.info("=" * 80)

        df = self.monthly_retention()

        print(df.head(20).to_string(index=False))

        logger.success("Retention Analysis Completed")

        self.conn.close()


if __name__ == "__main__":
    RetentionAnalytics().report()