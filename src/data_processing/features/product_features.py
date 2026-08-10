"""
Enterprise Product Analytics Platform
Product Feature Engineering
"""

import pandas as pd


class ProductFeatures:

    def create(self, dataframe: pd.DataFrame) -> pd.DataFrame:

        df = dataframe.copy()

        required = {"item_id", "event"}

        if not required.issubset(df.columns):
            return df

        features = (
            df.groupby("item_id")
            .agg(
                total_events=("event", "count"),
                unique_users=("visitor_id", "nunique"),
                views=("event", lambda x: (x == "view").sum()),
                add_to_cart=("event", lambda x: (x == "addtocart").sum()),
                transactions=(
                    "event",
                    lambda x: (x == "transaction").sum(),
                ),
            )
            .reset_index()
        )

        features["view_to_cart_rate"] = (
            features["add_to_cart"]
            / features["views"].replace(0, pd.NA)
            * 100
        )

        features["cart_to_purchase_rate"] = (
            features["transactions"]
            / features["add_to_cart"].replace(0, pd.NA)
            * 100
        )

        features["view_to_purchase_rate"] = (
            features["transactions"]
            / features["views"].replace(0, pd.NA)
            * 100
        )

        return features