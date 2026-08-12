"""
Enterprise Product Analytics Platform
ML Churn Prediction Service

High-level service layer built on the churn model.
"""

import pandas as pd

from src.machine_learning.churn_model import ChurnModel


class ChurnPredictionService:

    def __init__(self):
        self.model = ChurnModel()
        self.is_trained = False

    def train(self, events: pd.DataFrame):
        """
        Train the churn prediction model.

        Parameters
        ----------
        events : pd.DataFrame
            Event-level customer activity data.

        Returns
        -------
        dict
            Model evaluation metrics.
        """

        features = self.model.create_churn_target(
            events
        )

        metrics = self.model.train(
            features
        )

        self.is_trained = True

        return {
            "metrics": metrics,
            "features": features,
        }

    def predict(self, features: pd.DataFrame):
        """
        Generate churn probabilities for users.
        """

        if not self.is_trained:
            raise RuntimeError(
                "Model must be trained before prediction."
            )

        probabilities = self.model.predict(
            features
        )

        result = features.copy()

        result["churn_probability"] = probabilities

        result["risk_level"] = pd.cut(
            probabilities,
            bins=[
                -float("inf"),
                0.30,
                0.60,
                0.80,
                float("inf"),
            ],
            labels=[
                "Low",
                "Medium",
                "High",
                "Critical",
            ],
        )

        return result

    def summary(self, predictions: pd.DataFrame):
        """
        Return a business-friendly churn summary.
        """

        return {
            "total_users": len(predictions),
            "average_churn_probability": round(
                predictions[
                    "churn_probability"
                ].mean(),
                4,
            ),
            "high_risk_users": int(
                (
                    predictions[
                        "risk_level"
                    ].isin(
                        ["High", "Critical"]
                    )
                ).sum()
            ),
            "critical_users": int(
                (
                    predictions[
                        "risk_level"
                    ] == "Critical"
                ).sum()
            ),
        }