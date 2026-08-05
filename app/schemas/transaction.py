from pydantic import BaseModel, Field
from datetime import datetime


class TransactionCreate(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=20)
    
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)


class TransactionResponse(BaseModel):
    id: int
    user_id: int
    symbol: str
    transaction_type: str
    quantity: int
    price: float
    transaction_date: datetime

    class Config:
        from_attributes = True