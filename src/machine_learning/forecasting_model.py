"""
Enterprise Product Analytics Platform
Event Forecasting

Provides a lightweight time-series forecasting model
using historical event counts.
"""

import pandas as pd
from sklearn.linear_model import LinearRegression


class EventForecaster:

    def __init__(self):

        self.model = LinearRegression()

        self.is_fitted = False

    def prepare_data(
        self,
        events: pd.DataFrame,
        date_column: str = "timestamp",
    ):

        if date_column not in events.columns:
            raise ValueError(
                f"Column '{date_column}' not found"
            )

        data = events.copy()

        data[date_column] = pd.to_datetime(
            data[date_column],
            errors="coerce",
        )

        data = data.dropna(
            subset=[date_column]
        )

        daily = (
            data
            .set_index(date_column)
            .resample("D")
            .size()
            .reset_index(
                name="event_count"
            )
        )

        daily["day_number"] = range(
            len(daily)
        )

        return daily

    def fit(
        self,
        events: pd.DataFrame,
        date_column: str = "timestamp",
    ):

        daily = self.prepare_data(
            events,
            date_column,
        )

        if len(daily) < 2:
            raise ValueError(
                "At least two days of data are required"
            )

        X = daily[
            ["day_number"]
        ]

        y = daily[
            "event_count"
        ]

        self.model.fit(
            X,
            y,
        )

        self.is_fitted = True

        return daily

    def forecast(
        self,
        periods: int = 7,
    ):

        if not self.is_fitted:
            raise RuntimeError(
                "Model must be fitted before forecasting"
            )

        if periods <= 0:
            raise ValueError(
                "periods must be greater than zero"
            )

        last_day = (
            self.model
            .coef_
        )

        start = 0

        future = pd.DataFrame(
            {
                "day_number": range(
                    start,
                    start + periods,
                )
            }
        )

        future["forecast"] = (
            self.model.predict(
                future[
                    ["day_number"]
                ]
            )
            .round(2)
        )

        return future