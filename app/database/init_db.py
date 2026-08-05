from app.database.connection import engine
from app.database.base import Base

# Import all models here
from app.models.user import User
from app.models.transaction import Transaction


def init_db():
    Base.metadata.create_all(bind=engine)