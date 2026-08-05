from fastapi import FastAPI
from app.database.init_db import init_db
from app.api.user import router as user_router
from app.api.transaction import router as transaction_router

app = FastAPI(
    title="StockInsight API",
    description="Production-ready Stock Portfolio & Analytics Platform",
    version="1.0.0"
)
app.include_router(user_router)
app.include_router(transaction_router)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def home():
    return {
        "message": "Welcome to StockInsight 🚀"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "StockInsight",
        "version": "1.0.0"
    }