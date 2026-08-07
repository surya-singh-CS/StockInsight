from pydantic import BaseModel


class PortfolioSummaryResponse(BaseModel):
    total_stocks: int
    total_quantity: int
    total_transactions: int