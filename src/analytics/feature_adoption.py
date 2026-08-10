"""
Enterprise Product Analytics Platform
Feature Adoption Analytics Engine

Analyzes product feature usage from the analytics warehouse.
"""

from pathlib import Path

import duckdb
from loguru import logger


DATABASE_PATH = Path("data/warehouse/analytics.duckdb")


class FeatureAdoptionAnalytics:

    def __init__(self):
        self.conn = duckdb.connect(str(DATABASE_PATH))

    def event_adoption(self):
        """
        Measure adoption of available product actions.

        Since the current RetailRocket event data does not contain
        explicit product-feature identifiers, event types are used
        as behavioral features.
        """

        query = """
        WITH total_users AS (
            SELECT COUNT(DISTINCT visitor_id) AS users
            FROM fact_events
            WHERE visitor_id IS NOT NULL
        ),

        feature_usage AS (
            SELECT
                event AS feature,
                COUNT(*) AS event_count,
                COUNT(DISTINCT visitor_id) AS active_users
            FROM fact_events
            WHERE visitor_id IS NOT NULL
            GROUP BY event
        )

        SELECT
            feature,
            event_count,
            active_users,
            ROUND(
                100.0 * active_users / total_users.users,
                2
            ) AS adoption_rate
        FROM feature_usage
        CROSS JOIN total_users
        ORDER BY adoption_rate DESC
        """

        return self.conn.sql(query).df()

    def top_features(self, limit=10):
        """
        Return the most adopted behavioral features.
        """

        df = self.event_adoption()

        return df.head(limit)

    def report(self):

        logger.info("=" * 80)
        logger.info("FEATURE ADOPTION ANALYTICS")
        logger.info("=" * 80)

        df = self.event_adoption()

        print(df.to_string(index=False))

        logger.info("=" * 80)
        logger.info("TOP ADOPTED FEATURES")
        logger.info("=" * 80)

        print(self.top_features().to_string(index=False))

        logger.success("Feature Adoption Analysis Completed")

        self.conn.close()


if __name__ == "__main__":
    FeatureAdoptionAnalytics().report()