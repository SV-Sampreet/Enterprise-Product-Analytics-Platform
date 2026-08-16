from src.ml.customer_segmentation import CustomerSegmentationService


class SegmentationService:
    def __init__(self, n_clusters=4):
        self.model = CustomerSegmentationService(n_clusters=n_clusters)

    def train(self, data):
        return self.model.fit(data)

    def predict(self, data):
        return self.model.predict(data)

    def summary(self, data=None):
        if data is not None and hasattr(self.model, "segment_summary"):
            return self.model.segment_summary(data)
        return {"service": "segmentation", "status": "ready"}
