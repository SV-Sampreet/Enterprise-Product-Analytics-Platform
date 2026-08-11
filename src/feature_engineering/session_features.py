"""
Enterprise Product Analytics Platform
Session Feature Engineering

Creates session-level behavioral features.
"""

import pandas as pd


class SessionFeatureEngineer:

    def create(self, events: pd.DataFrame) -> pd.DataFrame:

        required_columns = {
            "visitor_id",
            "event",
            "timestamp",
        }

        missing = required_columns - set(events.columns)

        if missing:
            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )

        data = events.copy()

        data["timestamp"] = pd.to_datetime(
            data["timestamp"],
            errors="coerce",
        )

        data = data.dropna(
            subset=["timestamp"]
        )

        data["session_date"] = (
            data["timestamp"].dt.date
        )

        data["session_id"] = (
            data["visitor_id"].astype(str)
            + "_"
            + data["session_date"].astype(str)
        )

        features = (
            data
            .groupby("session_id")
            .agg(
                visitor_id=("visitor_id", "first"),
                session_start=("timestamp", "min"),
                session_end=("timestamp", "max"),
                total_events=("event", "count"),
                views=("event", lambda x: (x == "view").sum()),
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

        features["session_duration_minutes"] = (
            (
                features["session_end"]
                - features["session_start"]
            )
            .dt.total_seconds()
            / 60
        ).round(2)

        features["converted"] = (
            features["transactions"] > 0
        ).astype(int)

        return features