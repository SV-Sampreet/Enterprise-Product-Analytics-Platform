"""
Enterprise Product Analytics Platform
Forecasting Service

High-level forecasting service built on the event forecasting model.
"""

import pandas as pd

from src.machine_learning.forecasting_model import EventForecaster


class ForecastingService:

    def __init__(self):
        self.model = EventForecaster()
        self.is_trained = False

    def train(self, events: pd.DataFrame):
        """
        Train the forecasting model using event timestamps.

        Parameters
        ----------
        events : pd.DataFrame
            DataFrame containing a timestamp column.

        Returns
        -------
        pd.DataFrame
            Daily aggregated event counts.
        """

        if events.empty:
            raise ValueError(
                "Cannot train forecasting model with empty data."
            )

        if "timestamp" not in events.columns:
            raise ValueError(
                "Input data must contain a 'timestamp' column."
            )

        daily_data = self.model.fit(events)

        self.is_trained = True

        return daily_data

    def forecast(self, periods=7):
        """
        Generate future event forecasts.

        Parameters
        ----------
        periods : int
            Number of future periods to forecast.

        Returns
        -------
        pd.DataFrame
            Forecasted event counts.
        """

        if not self.is_trained:
            raise RuntimeError(
                "Model must be trained before forecasting."
            )

        if periods <= 0:
            raise ValueError(
                "Forecast periods must be greater than zero."
            )

        return self.model.forecast(periods)

    def summary(self, forecast_data: pd.DataFrame):
        """
        Generate a business-friendly forecast summary.
        """

        if forecast_data.empty:
            return {
                "forecast_periods": 0,
                "total_forecast": 0,
                "average_daily_forecast": 0,
            }

        forecast_values = forecast_data["forecast"]

        return {
            "forecast_periods": len(forecast_data),
            "total_forecast": round(
                float(forecast_values.sum()),
                2,
            ),
            "average_daily_forecast": round(
                float(forecast_values.mean()),
                2,
            ),
            "minimum_daily_forecast": round(
                float(forecast_values.min()),
                2,
            ),
            "maximum_daily_forecast": round(
                float(forecast_values.max()),
                2,
            ),
        }