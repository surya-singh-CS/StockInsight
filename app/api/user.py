from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.services.user import create_user, authenticate_user
from app.auth.jwt import create_access_token

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register", response_model=UserResponse, status_code=201)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user(db, user)

@router.post("/login", response_model=Token)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    db_user = authenticate_user(db, user)

    access_token = create_access_token(
        data={"sub": db_user.email}
)

    return {
    "access_token": access_token,
    "token_type": "bearer"
}