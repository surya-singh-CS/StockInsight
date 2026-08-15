from app.services.market_data import get_current_price
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

def calculate_cost_basis(transactions):
    current_quantity = 0
    current_cost = 0

    realized_profit_loss = 0

    for transaction in transactions:
        if transaction.transaction_type == "BUY":
            current_quantity += transaction.quantity

            current_cost += (
                transaction.quantity * transaction.price
            )

        elif transaction.transaction_type == "SELL":
            if current_quantity <= 0:
                continue

            average_cost = current_cost / current_quantity

            sale_value = (
                transaction.quantity * transaction.price
            )

            cost_of_sold_shares = (
                transaction.quantity * average_cost
            )

            realized_profit_loss += (
                sale_value - cost_of_sold_shares
            )

            current_quantity -= transaction.quantity

            current_cost -= cost_of_sold_shares

    return {
        "quantity": current_quantity,
        "cost_basis": current_cost,
        "realized_profit_loss": realized_profit_loss
    }

def get_portfolio_summary(
    db: Session,
    user_id: int
):
    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id)
        .order_by(
            Transaction.transaction_date,
            Transaction.id
    )
        .all()
)
    total_investment = 0
    total_buy_quantity = 0

    portfolio = get_portfolio(db, user_id)
    current_portfolio_value = 0
    realized_profit_loss = 0
    remaining_cost_basis = 0

    total_stocks = len(portfolio)
    total_quantity = sum(
        stock["quantity"] for stock in portfolio
    )
    total_transactions = len(transactions)

    for stock in portfolio:
        symbol = stock["symbol"]

        current_price = get_current_price(symbol)

        current_portfolio_value += (
            stock["quantity"] * current_price
    )

        symbol_transactions = [
            transaction
            for transaction in transactions
            if transaction.symbol == symbol
    ]

        cost_basis = calculate_cost_basis(
            symbol_transactions
    )

        realized_profit_loss += (
            cost_basis["realized_profit_loss"]
    )

        remaining_cost_basis += (
            cost_basis["cost_basis"]
    )

    unrealized_profit_loss = (
        current_portfolio_value - remaining_cost_basis
)
    total_profit_loss = (
        realized_profit_loss + unrealized_profit_loss
)

    for transaction in transactions:
        if transaction.transaction_type == "BUY":
            total_investment += (
                transaction.quantity * transaction.price
        )
            total_buy_quantity += transaction.quantity

    if total_buy_quantity > 0:
        average_buy_price = (
            total_investment / total_buy_quantity
    )
    else:
        average_buy_price = 0

    return {
        "total_stocks": total_stocks,
        "total_quantity": total_quantity,
        "total_transactions": total_transactions,
        "total_investment": total_investment,
        "average_buy_price": average_buy_price,
        "current_portfolio_value": current_portfolio_value,
        "realized_profit_loss": realized_profit_loss,
        "unrealized_profit_loss": unrealized_profit_loss,
        "total_profit_loss": total_profit_loss
    }