from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate


def create_transaction(
    db: Session,
    user_id: int,
    transaction: TransactionCreate,
    transaction_type: str
):
    db_transaction = Transaction(
        user_id=user_id,
        symbol=transaction.symbol.upper(),
        transaction_type= transaction_type,
        quantity=transaction.quantity,
        price=transaction.price
    )

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction

def get_transactions(
    db: Session,
    user_id: int
):
    return (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id)
        .order_by(Transaction.transaction_date.desc())
        .all()
    )

def get_current_quantity(
    db: Session,
    user_id: int,
    symbol: str
):
    transactions = (
        db.query(Transaction)
        .filter(
            Transaction.user_id == user_id,
            Transaction.symbol == symbol.upper()
        )
        .all()
    )

    quantity = 0

    for transaction in transactions:
        if transaction.transaction_type == "BUY":
            quantity += transaction.quantity
        else:
            quantity -= transaction.quantity

    return quantity

def get_portfolio(
    db: Session,
    user_id: int
):
    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id)
        .all()
    )

    portfolio = {}

    for transaction in transactions:

        symbol = transaction.symbol

        if symbol not in portfolio:
            portfolio[symbol] = 0

        if transaction.transaction_type == "BUY":
            portfolio[symbol] += transaction.quantity
        else:
            portfolio[symbol] -= transaction.quantity

    result = []

    for symbol, quantity in portfolio.items():
        if quantity > 0:
            result.append({
                "symbol": symbol,
                "quantity": quantity
            })

    return result