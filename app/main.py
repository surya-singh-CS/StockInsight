from fastapi import FastAPI

app = FastAPI(
    title="StockInsight API",
    description="Production-ready Stock Portfolio & Analytics Platform",
    version="1.0.0"
)

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