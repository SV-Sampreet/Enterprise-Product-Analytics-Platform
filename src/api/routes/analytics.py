from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/health")
def analytics_health():
    return {
        "service": "analytics",
        "status": "ready",
    }


@router.get("/metrics")
def metrics():
    return {
        "metrics": [
            "users",
            "revenue",
            "transactions",
            "retention",
            "conversion",
            "feature_adoption",
        ]
    }
