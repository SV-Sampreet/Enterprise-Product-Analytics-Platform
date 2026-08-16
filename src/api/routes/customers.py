from fastapi import APIRouter

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/health")
def customer_health():
    return {
        "service": "customers",
        "status": "ready",
    }


@router.get("/{visitor_id}")
def customer(visitor_id: int):
    return {
        "visitor_id": visitor_id,
        "status": "available",
    }
