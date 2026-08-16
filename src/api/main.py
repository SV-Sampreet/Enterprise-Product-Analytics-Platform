from fastapi import FastAPI

from src.api.routes.analytics import router as analytics_router
from src.api.routes.customers import router as customers_router
from src.api.routes.ml import router as ml_router


app = FastAPI(
    title="Enterprise Product Analytics Intelligence Platform",
    description="Enterprise analytics, machine learning and product intelligence API",
    version="1.0.0",
)

app.include_router(analytics_router)
app.include_router(customers_router)
app.include_router(ml_router)


@app.get("/")
def root():
    return {
        "name": "Enterprise Product Analytics Intelligence Platform",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "enterprise-product-analytics",
    }
