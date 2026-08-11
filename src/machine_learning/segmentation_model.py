"""
Enterprise Product Analytics Platform
Customer Segmentation

Segments users based on behavioral activity using K-Means.
"""

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class CustomerSegmentation:

    def __init__(
        self,
        n_clusters=4,
        random_state=42,
    ):

        self.n_clusters = n_clusters

        self.scaler = StandardScaler()

        self.model = KMeans(
            n_clusters=n_clusters,
            random_state=random_state,
            n_init=10,
        )

        self.feature_columns = None

    def prepare_features(
        self,
        features: pd.DataFrame,
    ):

        self.feature_columns = [
            column
            for column in features.columns
            if column != "visitor_id"
            and pd.api.types.is_numeric_dtype(
                features[column]
            )
        ]

        if not self.feature_columns:
            raise ValueError(
                "No numeric features available"
            )

        return features[
            self.feature_columns
        ].fillna(0)

    def fit_predict(
        self,
        features: pd.DataFrame,
    ):

        X = self.prepare_features(features)

        X_scaled = self.scaler.fit_transform(X)

        labels = self.model.fit_predict(
            X_scaled
        )

        result = features.copy()

        result["segment"] = labels

        return result

    def segment_summary(
        self,
        segmented_data: pd.DataFrame,
    ):

        if "segment" not in segmented_data.columns:
            raise ValueError(
                "Run fit_predict() before creating summary"
            )

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
            / summary["users"].sum()
            * 100
        ).round(2)

        return summary.sort_values(
            "users",
            ascending=False,
        )