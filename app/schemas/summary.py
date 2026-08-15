from pydantic import BaseModel


class PortfolioSummaryResponse(BaseModel):
    total_stocks: int
    total_quantity: int
    total_transactions: int
    total_investment: float
    average_buy_price: float
    current_portfolio_value: float
    realized_profit_loss: float
    unrealized_profit_loss: float
    total_profit_loss: float