"""
Enterprise Product Analytics Platform
Session Feature Engineering
"""

import pandas as pd


class SessionFeatures:

    def create(self, dataframe: pd.DataFrame) -> pd.DataFrame:

        df = dataframe.copy()

        if "visitor_id" not in df.columns:
            return df

        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(
                df["timestamp"],
                errors="coerce",
            )

        df = df.sort_values(
            ["visitor_id", "timestamp"]
            if "timestamp" in df.columns
            else ["visitor_id"]
        )

        df["previous_timestamp"] = (
            df.groupby("visitor_id")["timestamp"]
            .shift(1)
            if "timestamp" in df.columns
            else pd.NaT
        )

        if "timestamp" in df.columns:

            time_gap = (
                df["timestamp"] - df["previous_timestamp"]
            ).dt.total_seconds() / 60

            new_session = (
                df["previous_timestamp"].isna()
                | (time_gap > 30)
            )

            df["session_number"] = (
                new_session.groupby(df["visitor_id"]).cumsum()
            )

            df["session_id"] = (
                df["visitor_id"].astype(str)
                + "_"
                + df["session_number"].astype(str)
            )

        else:

            df["session_id"] = (
                df["visitor_id"].astype(str)
                + "_1"
            )

        return df.drop(
            columns=["previous_timestamp"],
            errors="ignore",
        )