from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.watchlist import (
    WatchlistCreate,
    WatchlistResponse
)

from app.services.watchlist import (
    add_to_watchlist,
    get_watchlist,
    remove_from_watchlist
)


router = APIRouter(
    prefix="/watchlist",
    tags=["Watchlist"]
)


@router.post(
    "/",
    response_model=WatchlistResponse,
    status_code=201
)
def add_stock(
    watchlist: WatchlistCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return add_to_watchlist(
        db=db,
        user_id=current_user.id,
        watchlist=watchlist
    )


@router.get(
    "/",
    response_model=list[WatchlistResponse]
)
def get_user_watchlist(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_watchlist(
        db=db,
        user_id=current_user.id
    )


@router.delete("/{symbol}")
def remove_stock(
    symbol: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return remove_from_watchlist(
        db=db,
        user_id=current_user.id,
        symbol=symbol
    )