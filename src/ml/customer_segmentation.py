"""
Enterprise Product Analytics Platform
Customer Segmentation Service
"""

import pandas as pd

from src.machine_learning.segmentation_model import (
    CustomerSegmentation,
)


class CustomerSegmentationService:

    def __init__(self, n_clusters=4):
        self.model = CustomerSegmentation(
            n_clusters=n_clusters
        )
        self.is_trained = False

    def train(self, features: pd.DataFrame):
        """
        Train customer segmentation model.
        """

        result = self.model.fit_predict(
            features
        )

        self.is_trained = True

        return result

    def segment_summary(
        self,
        segmented_data: pd.DataFrame,
    ):
        """
        Generate business-friendly segment summary.
        """

        summary = (
            segmented_data
            .groupby("segment")
            .size()
            .reset_index(
                name="users"
            )
        )

        summary["percentage"] = (
            summary["users"]
            / len(segmented_data)
            * 100
        ).round(2)

        return summary.sort_values(
            "users",
            ascending=False,
        ).reset_index(drop=True)

    def predict(
        self,
        features: pd.DataFrame,
    ):
        """
        Assign users to existing segments.
        """

        if not self.is_trained:
            raise RuntimeError(
                "Model must be trained before prediction."
            )

        return self.model.fit_predict(
            features
        )