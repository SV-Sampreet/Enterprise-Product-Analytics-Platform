"""
Enterprise Product Analytics Platform
Dashboard Data Layer
"""

from pathlib import Path

import duckdb


DATABASE_PATH = Path("data/warehouse/analytics.duckdb")


class DashboardData:

    def __init__(self):
        self.conn = duckdb.connect(str(DATABASE_PATH), read_only=True)

    def kpis(self):
        query = """
        SELECT
            COUNT(*) AS total_events,
            COUNT(DISTINCT visitor_id) AS total_users,
            COUNT(CASE WHEN event = 'view' THEN 1 END) AS views,
            COUNT(CASE WHEN event = 'addtocart' THEN 1 END) AS add_to_cart,
            COUNT(CASE WHEN event = 'transaction' THEN 1 END) AS transactions
        FROM fact_events
        """

        return self.conn.sql(query).df()

    def event_summary(self):
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

    def daily_activity(self):
        query = """
        SELECT
            DATE_TRUNC('day', timestamp) AS activity_date,
            COUNT(*) AS events,
            COUNT(DISTINCT visitor_id) AS users
        FROM fact_events
        GROUP BY activity_date
        ORDER BY activity_date
        """

        return self.conn.sql(query).df()

    def close(self):
        self.conn.close()