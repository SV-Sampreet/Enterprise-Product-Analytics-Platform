"""
Enterprise Product Analytics Platform
Product Feature Engineering

Creates behavioral features at the product level.
"""

import pandas as pd


class ProductFeatureEngineer:

    def create(self, events: pd.DataFrame) -> pd.DataFrame:

        required_columns = {
            "item_id",
            "event",
        }

        missing = required_columns - set(events.columns)

        if missing:
            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )

        features = (
            events
            .groupby("item_id")
            .agg(
                total_events=("event", "count"),
                views=("event", lambda x: (x == "view").sum()),
                add_to_cart=("event", lambda x: (x == "addtocart").sum()),
                transactions=(
                    "event",
                    lambda x: (x == "transaction").sum(),
                ),
            )
            .reset_index()
        )

        features["cart_conversion_rate"] = (
            features["add_to_cart"]
            / features["views"].replace(0, pd.NA)
            * 100
        ).fillna(0).round(2)

        features["purchase_conversion_rate"] = (
            features["transactions"]
            / features["views"].replace(0, pd.NA)
            * 100
        ).fillna(0).round(2)

        features["purchase_flag"] = (
            features["transactions"] > 0
        ).astype(int)

        return features