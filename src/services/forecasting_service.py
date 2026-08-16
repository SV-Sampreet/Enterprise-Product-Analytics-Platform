from src.ml.forecasting import ForecastingService as MLForecastingService


class ForecastingService:
    def __init__(self):
        self.model = MLForecastingService()

    def train(self, data):
        return self.model.train(data)

    def forecast(self, periods=7):
        return self.model.forecast(periods)

    def summary(self, forecast=None):
        if hasattr(self.model, "summary"):
            return self.model.summary(forecast)
        return {"service": "forecasting", "status": "ready"}
