from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.jwt import verify_access_token
from app.api.user import oauth2_scheme
from app.database.connection import get_db
from app.models.user import User


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    email = verify_access_token(token)

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user