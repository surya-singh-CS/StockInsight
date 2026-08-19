from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.base import Base


class Watchlist(Base):
    __tablename__ = "watchlist"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    symbol = Column(
        String(20),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user = relationship(
        "User",
        back_populates="watchlist"
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "symbol",
            name="unique_user_watchlist_symbol"
        ),
    )