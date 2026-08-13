import pandas as pd
from collections import Counter


class RecommendationEngine:
    """
    Product recommendation engine based on user event history.

    Uses interaction frequency and event type to rank products
    for each user.
    """

    EVENT_WEIGHTS = {
        "purchase": 5,
        "addtocart": 4,
        "view": 2,
        "click": 1,
    }

    def __init__(self, top_n: int = 5):
        self.top_n = top_n
        self.user_product_scores = None

    def train(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Build user-product interaction scores.

        Required columns:
            visitor_id
            item_id
            event
        """
        required = {"visitor_id", "item_id", "event"}

        missing = required - set(df.columns)
        if missing:
            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )

        data = df.copy()

        data["event_weight"] = (
            data["event"]
            .map(self.EVENT_WEIGHTS)
            .fillna(0)
        )

        self.user_product_scores = (
            data.groupby(
                ["visitor_id", "item_id"],
                as_index=False
            )["event_weight"]
            .sum()
            .rename(columns={"event_weight": "score"})
        )

        return self.user_product_scores

    def recommend(
        self,
        visitor_id,
        n: int | None = None
    ) -> pd.DataFrame:
        """
        Return top product recommendations for a user.
        """
        if self.user_product_scores is None:
            raise ValueError(
                "Model has not been trained. Call train() first."
            )

        n = n or self.top_n

        recommendations = (
            self.user_product_scores[
                self.user_product_scores["visitor_id"] == visitor_id
            ]
            .sort_values("score", ascending=False)
            .head(n)
            .reset_index(drop=True)
        )

        return recommendations

    def popular_products(
        self,
        df: pd.DataFrame,
        n: int | None = None
    ) -> pd.DataFrame:
        """
        Return globally popular products based on interaction score.
        """
        n = n or self.top_n

        data = df.copy()

        data["event_weight"] = (
            data["event"]
            .map(self.EVENT_WEIGHTS)
            .fillna(0)
        )

        popular = (
            data.groupby("item_id", as_index=False)["event_weight"]
            .sum()
            .rename(columns={"event_weight": "score"})
            .sort_values("score", ascending=False)
            .head(n)
            .reset_index(drop=True)
        )

        return popular

    def summary(self) -> dict:
        """
        Return basic recommendation-engine statistics.
        """
        if self.user_product_scores is None:
            raise ValueError(
                "Model has not been trained. Call train() first."
            )

        return {
            "users": int(
                self.user_product_scores["visitor_id"].nunique()
            ),
            "products": int(
                self.user_product_scores["item_id"].nunique()
            ),
            "interactions": len(self.user_product_scores),
            "top_n": self.top_n,
        }