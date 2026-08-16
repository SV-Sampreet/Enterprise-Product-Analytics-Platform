from fastapi import APIRouter

router = APIRouter(prefix="/ml", tags=["Machine Learning"])


@router.get("/health")
def ml_health():
    return {
        "service": "machine-learning",
        "status": "ready",
        "models": [
            "churn",
            "segmentation",
            "forecasting",
            "recommendation",
        ],
    }
