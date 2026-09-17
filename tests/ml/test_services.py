import numpy as np
import pandas as pd
import pytest

from src.ml.churn_prediction import ChurnPredictionService
from src.ml.forecasting import ForecastingService
from src.ml.customer_segmentation import CustomerSegmentationService
from src.ml.recommendation_engine import RecommendationEngine


def test_churn_service_requires_training_before_prediction():
    service = ChurnPredictionService()

    features = pd.DataFrame(
        {
            "recency": [1, 2],
            "frequency": [5, 3],
            "monetary": [100.0, 50.0],
        }
    )

    with pytest.raises(RuntimeError, match="Model must be trained"):
        service.predict(features)


def make_churn_test_events():
    records = []

    # Active users:
    # Activity inside the observation window
    # AND activity after the churn cutoff.
    for user_id in range(1, 21):
        records.append(
            {
                "visitor_id": user_id,
                "item_id": 100 + (user_id % 5),
                "event": "view",
                "timestamp": pd.Timestamp("2025-03-01"),
            }
        )

        records.append(
            {
                "visitor_id": user_id,
                "item_id": 100 + (user_id % 5),
                "event": "transaction",
                "timestamp": pd.Timestamp("2025-04-01"),
            }
        )

    # Churned users:
    # Activity inside the observation window,
    # but no activity after the cutoff.
    for user_id in range(21, 41):
        records.append(
            {
                "visitor_id": user_id,
                "item_id": 100 + (user_id % 5),
                "event": "view",
                "timestamp": pd.Timestamp("2025-03-01"),
            }
        )

    # Establish the maximum date and therefore
    # the 30-day churn cutoff.
    records.append(
        {
            "visitor_id": 999,
            "item_id": 199,
            "event": "view",
            "timestamp": pd.Timestamp("2025-04-15"),
        }
    )

    return pd.DataFrame(records)


def test_churn_service_training_produces_metrics():
    events = make_churn_test_events()

    service = ChurnPredictionService()

    result = service.train(events)

    assert "metrics" in result
    assert "features" in result
    assert isinstance(result["features"], pd.DataFrame)
    assert service.is_trained is True


def test_churn_prediction_returns_probability_and_risk():
    events = make_churn_test_events()

    service = ChurnPredictionService()

    trained = service.train(events)
    features = trained["features"]

    predictions = service.predict(features)

    assert "churn_probability" in predictions.columns
    assert "risk_level" in predictions.columns

    assert predictions["churn_probability"].between(0, 1).all()

    valid_levels = {"Low", "Medium", "High", "Critical"}

    assert set(
        predictions["risk_level"].dropna()
    ).issubset(valid_levels)


def test_segmentation_service_creates_expected_number_of_clusters():
    service = CustomerSegmentationService(n_clusters=2)

    data = pd.DataFrame(
        {
            "recency": [1, 2, 3, 20, 21, 22],
            "frequency": [10, 11, 9, 2, 3, 1],
            "monetary": [100, 110, 90, 20, 25, 15],
        }
    )

    result = service.train(data)

    assert result is not None
    assert service.is_trained is True
    assert len(result) == len(data)


def test_forecasting_service_generates_requested_periods():
    service = ForecastingService()

    data = pd.DataFrame(
        {
            "timestamp": pd.date_range(
                "2025-01-01",
                periods=30,
                freq="D",
            ),
            "revenue": np.linspace(100, 200, 30),
        }
    )

    service.train(data)

    forecast = service.forecast(periods=7)

    assert forecast is not None
    assert len(forecast) == 7


def test_recommendation_engine_training():
    data = pd.DataFrame(
        {
            "visitor_id": [1, 1, 1, 2, 2, 3],
            "item_id": [101, 102, 103, 101, 104, 105],
            "event": [
                "view",
                "addtocart",
                "transaction",
                "view",
                "transaction",
                "view",
            ],
        }
    )

    engine = RecommendationEngine(top_n=3)

    result = engine.train(data)

    assert result is not None
    assert engine.top_n == 3


def test_recommendation_engine_summary_contains_counts():
    data = pd.DataFrame(
        {
            "visitor_id": [1, 1, 2, 2, 3],
            "item_id": [101, 102, 101, 103, 104],
            "event": ["view", "transaction", "view", "view", "transaction"],
        }
    )

    engine = RecommendationEngine(top_n=3)
    engine.train(data)

    summary = engine.summary()

    assert isinstance(summary, dict)
    assert "users" in summary
    assert "products" in summary
    assert "interactions" in summary
