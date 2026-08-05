from pydantic import BaseModel


class PortfolioResponse(BaseModel):
    symbol: str
    quantity: int