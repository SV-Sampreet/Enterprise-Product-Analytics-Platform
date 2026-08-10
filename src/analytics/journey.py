"""
Enterprise Product Analytics Platform
User Journey Analytics Engine

Analyzes customer behavior and movement through the product journey.
"""

from pathlib import Path

import duckdb
from loguru import logger


DATABASE_PATH = Path("data/warehouse/analytics.duckdb")


class JourneyAnalytics:

    def __init__(self):
        self.conn = duckdb.connect(str(DATABASE_PATH))

    def journey_summary(self):
        """
        Summarize users and events across each journey stage.
        """

        query = """
        SELECT
            event AS journey_stage,
            COUNT(*) AS total_events,
            COUNT(DISTINCT visitor_id) AS unique_users,
            COUNT(DISTINCT item_id) AS unique_items
        FROM fact_events
        WHERE event IS NOT NULL
        GROUP BY event
        ORDER BY
            CASE
                WHEN event = 'view' THEN 1
                WHEN event = 'addtocart' THEN 2
                WHEN event = 'transaction' THEN 3
                ELSE 4
            END
        """

        return self.conn.sql(query).df()

    def user_journey_distribution(self):
        """
        Calculate the percentage of users reaching each journey stage.
        """

        query = """
        WITH total_users AS (
            SELECT COUNT(DISTINCT visitor_id) AS users
            FROM fact_events
            WHERE visitor_id IS NOT NULL
        ),

        journey_users AS (
            SELECT
                event AS journey_stage,
                COUNT(DISTINCT visitor_id) AS users
            FROM fact_events
            WHERE visitor_id IS NOT NULL
              AND event IS NOT NULL
            GROUP BY event
        )

        SELECT
            journey_stage,
            users,
            ROUND(
                100.0 * users / total_users.users,
                2
            ) AS user_reach_rate
        FROM journey_users
        CROSS JOIN total_users
        ORDER BY
            CASE
                WHEN journey_stage = 'view' THEN 1
                WHEN journey_stage = 'addtocart' THEN 2
                WHEN journey_stage = 'transaction' THEN 3
                ELSE 4
            END
        """

        return self.conn.sql(query).df()

    def journey_transitions(self):
        """
        Calculate high-level conversion between journey stages.
        """

        query = """
        WITH metrics AS (
            SELECT
                COUNT(DISTINCT CASE
                    WHEN event = 'view'
                    THEN visitor_id
                END) AS viewers,

                COUNT(DISTINCT CASE
                    WHEN event = 'addtocart'
                    THEN visitor_id
                END) AS cart_users,

                COUNT(DISTINCT CASE
                    WHEN event = 'transaction'
                    THEN visitor_id
                END) AS purchasers

            FROM fact_events
        )

        SELECT
            viewers,
            cart_users,
            purchasers,

            ROUND(
                100.0 * cart_users /
                NULLIF(viewers, 0),
                2
            ) AS view_to_cart_rate,

            ROUND(
                100.0 * purchasers /
                NULLIF(cart_users, 0),
                2
            ) AS cart_to_purchase_rate,

            ROUND(
                100.0 * purchasers /
                NULLIF(viewers, 0),
                2
            ) AS view_to_purchase_rate

        FROM metrics
        """

        return self.conn.sql(query).df()

    def report(self):

        logger.info("=" * 80)
        logger.info("USER JOURNEY ANALYTICS")
        logger.info("=" * 80)

        print("\nJOURNEY SUMMARY\n")
        print(self.journey_summary().to_string(index=False))

        print("\nUSER REACH BY JOURNEY STAGE\n")
        print(self.user_journey_distribution().to_string(index=False))

        print("\nJOURNEY CONVERSION\n")
        print(self.journey_transitions().to_string(index=False))

        logger.success("User Journey Analysis Completed")

        self.conn.close()


if __name__ == "__main__":
    JourneyAnalytics().report()