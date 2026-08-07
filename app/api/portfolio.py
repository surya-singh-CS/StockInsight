from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.portfolio import PortfolioResponse
from app.schemas.summary import PortfolioSummaryResponse

from app.services.transaction import (
    get_portfolio,
    get_portfolio_summary
)

router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"]
)


@router.get(
    "/",
    response_model=list[PortfolioResponse]
)
def get_user_portfolio(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_portfolio(
        db=db,
        user_id=current_user.id
    )


@router.get(
    "/summary",
    response_model=PortfolioSummaryResponse
)
def get_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_portfolio_summary(
        db=db,
        user_id=current_user.id
    )