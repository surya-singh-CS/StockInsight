from pydantic import BaseModel
from datetime import datetime


class WatchlistCreate(BaseModel):
    symbol: str


class WatchlistResponse(BaseModel):
    id: int
    user_id: int
    symbol: str
    created_at: datetime
    current_price: float

    class Config:
        from_attributes = True