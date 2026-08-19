from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.services.market_data import get_current_price
from app.models.watchlist import Watchlist
from app.schemas.watchlist import WatchlistCreate


def add_to_watchlist(
    db: Session,
    user_id: int,
    watchlist: WatchlistCreate
):
    existing_stock = (
        db.query(Watchlist)
        .filter(
            Watchlist.user_id == user_id,
            Watchlist.symbol == watchlist.symbol.upper()
        )
        .first()
    )

    if existing_stock:
        raise HTTPException(
            status_code=400,
            detail="Stock already in watchlist"
        )

    db_watchlist = Watchlist(
        user_id=user_id,
        symbol=watchlist.symbol.upper()
    )

    db.add(db_watchlist)
    db.commit()
    db.refresh(db_watchlist)

    return db_watchlist

def get_watchlist(
    db: Session,
    user_id: int
):
    watchlist_items = (
        db.query(Watchlist)
        .filter(Watchlist.user_id == user_id)
        .order_by(Watchlist.created_at.desc())
        .all()
    )

    result = []

    for item in watchlist_items:
        current_price = round(get_current_price(item.symbol),2)

        result.append({
            "id": item.id,
            "user_id": item.user_id,
            "symbol": item.symbol,
            "created_at": item.created_at,
            "current_price": current_price
        })

    return result

def remove_from_watchlist(
    db: Session,
    user_id: int,
    symbol: str
):
    watchlist_item = (
        db.query(Watchlist)
        .filter(
            Watchlist.user_id == user_id,
            Watchlist.symbol == symbol.upper()
        )
        .first()
    )

    if not watchlist_item:
        raise HTTPException(
            status_code=404,
            detail="Stock not found in watchlist"
        )

    db.delete(watchlist_item)
    db.commit()

    return {
        "message": f"{symbol.upper()} removed from watchlist"
    }