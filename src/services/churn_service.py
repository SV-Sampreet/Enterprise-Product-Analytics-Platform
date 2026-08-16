from src.ml.churn_prediction import ChurnPredictionService


class ChurnService:
    def __init__(self):
        self.model = ChurnPredictionService()

    def train(self, data):
        return self.model.train(data)

    def predict(self, data):
        return self.model.predict(data)

    def summary(self):
        if hasattr(self.model, "summary"):
            return self.model.summary()
        return {"service": "churn", "status": "ready"}
