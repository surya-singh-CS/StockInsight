from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.auth.password import hash_password
from app.schemas.user import UserLogin
from app.auth.password import verify_password

# check duplicate emails from db/user table 
def create_user(db: Session, user: UserCreate):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:  # http exception used so fastapi understands it
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    db_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )
        
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def authenticate_user(db: Session, user: UserLogin):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return db_user