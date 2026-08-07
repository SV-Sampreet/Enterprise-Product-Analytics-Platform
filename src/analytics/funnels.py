"""
Enterprise Product Analytics Platform

Conversion Funnel Analytics
"""

from pathlib import Path

import duckdb
from loguru import logger

DATABASE_PATH = Path("data/warehouse/analytics.duckdb")


class FunnelAnalytics:

    def __init__(self):
        self.conn = duckdb.connect(str(DATABASE_PATH))

    def execute(self, query):
        return self.conn.sql(query).fetchone()[0]

    def views(self):
        return self.execute("""
            SELECT COUNT(*)
            FROM fact_events
            WHERE event='view'
        """)

    def add_to_cart(self):
        return self.execute("""
            SELECT COUNT(*)
            FROM fact_events
            WHERE event='addtocart'
        """)

    def purchases(self):
        return self.execute("""
            SELECT COUNT(*)
            FROM fact_events
            WHERE event='transaction'
        """)

    def report(self):

        views = self.views()
        carts = self.add_to_cart()
        purchases = self.purchases()

        view_cart = round(carts / views * 100, 2) if views else 0
        cart_purchase = round(purchases / carts * 100, 2) if carts else 0
        overall = round(purchases / views * 100, 2) if views else 0

        logger.info("=" * 80)
        logger.info("PRODUCT CONVERSION FUNNEL")
        logger.info("=" * 80)

        print(f"Views                 : {views:,}")
        print(f"Add To Cart           : {carts:,}")
        print(f"Purchases             : {purchases:,}")
        print()
        print(f"View → Cart (%)       : {view_cart}")
        print(f"Cart → Purchase (%)   : {cart_purchase}")
        print(f"Overall Conversion    : {overall}%")

        logger.success("Funnel Analysis Completed")

        self.conn.close()


if __name__ == "__main__":
    FunnelAnalytics().report()