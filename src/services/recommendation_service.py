from src.ml.recommendation_engine import RecommendationEngine


class RecommendationService:
    def __init__(self, top_n=5):
        self.model = RecommendationEngine(top_n=top_n)

    def train(self, data):
        return self.model.train(data)

    def recommend(self, visitor_id):
        return self.model.recommend(visitor_id)

    def summary(self):
        return self.model.summary()
