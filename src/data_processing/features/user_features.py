"""
Enterprise Product Analytics Platform
User Feature Engineering
"""

import pandas as pd


class UserFeatures:

    def create(self, dataframe: pd.DataFrame) -> pd.DataFrame:

        df = dataframe.copy()

        if "visitor_id" not in df.columns:
            return df

        features = (
            df.groupby("visitor_id")
            .agg(
                total_events=("event", "count"),
                unique_items=("item_id", "nunique"),
                views=(
                    "event",
                    lambda x: (x == "view").sum(),
                ),
                add_to_cart=(
                    "event",
                    lambda x: (x == "addtocart").sum(),
                ),
                transactions=(
                    "event",
                    lambda x: (x == "transaction").sum(),
                ),
            )
            .reset_index()
        )

        features["conversion_rate"] = (
            features["transactions"]
            / features["views"].replace(0, pd.NA)
            * 100
        )

        features["cart_rate"] = (
            features["add_to_cart"]
            / features["views"].replace(0, pd.NA)
            * 100
        )

        features["purchase_rate"] = (
            features["transactions"]
            / features["add_to_cart"].replace(0, pd.NA)
            * 100
        )

        return features