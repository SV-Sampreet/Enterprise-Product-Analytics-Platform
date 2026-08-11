"""
Enterprise Product Analytics Platform
Customer Churn Prediction

Builds a user-level churn model using historical activity.
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


class ChurnModel:

    def __init__(self, n_estimators=100, random_state=42):

        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=random_state,
            class_weight="balanced",
        )

        self.feature_columns = None

    def create_churn_target(
        self,
        events: pd.DataFrame,
        observation_days=30,
        churn_window_days=30,
    ):

        required = {
            "visitor_id",
            "timestamp",
            "event",
        }

        missing = required - set(events.columns)

        if missing:
            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )

        data = events[
            [
                "visitor_id",
                "timestamp",
                "event",
            ]
            + (
                ["item_id"]
                if "item_id" in events.columns
                else []
            )
        ].copy()

        data["timestamp"] = pd.to_datetime(
            data["timestamp"],
            errors="coerce",
        )

        data = data.dropna(
            subset=["timestamp"]
        )

        if data.empty:
            raise ValueError(
                "No valid timestamp records found"
            )

        max_date = data["timestamp"].max()

        observation_cutoff = (
            max_date
            - pd.Timedelta(
                days=churn_window_days
            )
        )

        feature_start = (
            observation_cutoff
            - pd.Timedelta(
                days=observation_days
            )
        )

        historical = data[
            data["timestamp"] <= observation_cutoff
        ].copy()

        future = data[
            data["timestamp"] > observation_cutoff
        ].copy()

        if historical.empty or future.empty:
            raise ValueError(
                "Insufficient historical/future data "
                "to create churn labels"
            )

        # -------------------------------
        # USER BEHAVIOR FEATURES
        # -------------------------------

        observed = historical[
            historical["timestamp"] >= feature_start
        ].copy()

        observed["views"] = (
            observed["event"] == "view"
        ).astype("int8")

        observed["add_to_cart"] = (
            observed["event"] == "addtocart"
        ).astype("int8")

        observed["transactions"] = (
            observed["event"] == "transaction"
        ).astype("int8")

        aggregation = {
            "event": "count",
            "views": "sum",
            "add_to_cart": "sum",
            "transactions": "sum",
            "timestamp": "max",
        }

        if "item_id" in observed.columns:
            aggregation["item_id"] = "nunique"

        features = (
            observed
            .groupby("visitor_id", sort=False)
            .agg(aggregation)
            .reset_index()
        )

        features = features.rename(
            columns={
                "event": "total_events",
                "timestamp": "last_activity",
                "item_id": "unique_items",
            }
        )

        # -------------------------------
        # FUTURE CHURN LABEL
        # -------------------------------

        future_users = set(
            future["visitor_id"].unique()
        )

        features["churned"] = (
            ~features["visitor_id"].isin(
                future_users
            )
        ).astype("int8")

        return features

    def train(
        self,
        features: pd.DataFrame,
        target_column="churned",
        test_size=0.2,
    ):

        if target_column not in features.columns:
            raise ValueError(
                f"Target column '{target_column}' not found"
            )

        excluded = {
            "visitor_id",
            "last_activity",
            target_column,
        }

        self.feature_columns = [
            column
            for column in features.columns
            if column not in excluded
            and pd.api.types.is_numeric_dtype(
                features[column]
            )
        ]

        X = features[
            self.feature_columns
        ].fillna(0)

        y = features[
            target_column
        ]

        if y.nunique() < 2:
            raise ValueError(
                "Churn target contains only one class. "
                "Use a dataset with enough historical "
                "and future activity."
            )

        X_train, X_test, y_train, y_test = (
            train_test_split(
                X,
                y,
                test_size=test_size,
                random_state=42,
                stratify=y,
            )
        )

        self.model.fit(
            X_train,
            y_train,
        )

        predictions = self.model.predict(
            X_test
        )

        return {
            "accuracy": round(
                accuracy_score(
                    y_test,
                    predictions,
                ),
                4,
            ),
            "classification_report": classification_report(
                y_test,
                predictions,
                zero_division=0,
            ),
        }

    def predict(self, features):

        if self.feature_columns is None:
            raise RuntimeError(
                "Model must be trained before prediction"
            )

        X = features[
            self.feature_columns
        ].fillna(0)

        return self.model.predict_proba(X)[:, 1]