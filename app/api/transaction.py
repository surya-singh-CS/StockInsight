from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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
    get_current_quantity,
    get_portfolio
)
from app.schemas.portfolio import PortfolioResponse
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
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    email = verify_access_token(token)

    user = db.query(User).filter(
        User.email == email
    ).first()

    return create_transaction(
        db=db,
        user_id=user.id,
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
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    email = verify_access_token(token)

    user = db.query(User).filter(
        User.email == email
    ).first()

    current_quantity = get_current_quantity(
        db=db,
        user_id=user.id,
        symbol=transaction.symbol
    )

    if current_quantity < transaction.quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient shares"
        )

    return create_transaction(
        db=db,
        user_id=user.id,
        transaction=transaction,
        transaction_type="SELL"
    )

@router.get(
    "/",
    response_model=list[TransactionResponse]
)
def get_user_transactions(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    email = verify_access_token(token)

    user = db.query(User).filter(
        User.email == email
    ).first()

    return get_transactions(
        db=db,
        user_id=user.id
    )

@router.get(
    "/portfolio",
    response_model=list[PortfolioResponse]
)
def get_user_portfolio(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    email = verify_access_token(token)

    user = db.query(User).filter(
        User.email == email
    ).first()

    return get_portfolio(
        db=db,
        user_id=user.id
    )