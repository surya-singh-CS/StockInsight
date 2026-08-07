from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.auth import get_current_user
from app.auth.jwt import verify_access_token
from app.database.connection import get_db
from app.models.user import User
from app.schemas.transaction import (
    TransactionCreate,
    TransactionResponse,
)
from app.services.transaction import (
    create_transaction,
    get_transactions,
    get_current_quantity
    
)

from app.api.user import oauth2_scheme

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.post(
    "/buy",
    response_model=TransactionResponse,
    status_code=201
)
def buy_stock(
    transaction: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    

    return create_transaction(
        db=db,
        user_id=current_user.id,
        transaction=transaction,
        transaction_type="BUY"
    )

@router.post(
    "/sell",
    response_model=TransactionResponse,
    status_code=201
)
def sell_stock(
    transaction: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    

    current_quantity = get_current_quantity(
        db=db,
        user_id=current_user.id,
        symbol=transaction.symbol
    )

    if current_quantity < transaction.quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient shares"
        )

    return create_transaction(
        db=db,
        user_id=current_user.id,
        transaction=transaction,
        transaction_type="SELL"
    )

@router.get(
    "/",
    response_model=list[TransactionResponse]
)
def get_user_transactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    

    return get_transactions(
        db=db,
        user_id=current_user.id
    )

