"""Budget logic. No input(), no print(), no files."""
from budget_manager.models import Transaction


def next_id(transactions: list) -> str:
    """Return the next id: T1, T2, T3, ..."""
    return f"T{len(transactions) + 1}"


def add_transaction(transactions: list, new_tx: Transaction) -> None:
    """Add new_tx to the list.

    Raises:
        ValueError: If a transaction with the same id already exists.
    """
    for tx in transactions:
        if tx.id == new_tx.id:
            raise ValueError(f"duplicate id {new_tx.id}")
    transactions.append(new_tx)


def filter_by_month(transactions: list, month: str) -> list:
    """Return only the transactions whose date starts with month (YYYY-MM)."""
    return [tx for tx in transactions if tx.date.startswith(month)]


def summarize(transactions: list) -> dict:
    """Return count, total income, total expenses, balance and expenses per category."""
    income = 0
    expenses = 0
    by_category = {}
    for tx in transactions:
        if tx.kind == "income":
            income += tx.amount
        else:
            expenses += tx.amount
            by_category[tx.category] = by_category.get(tx.category, 0) + tx.amount
    return {
        "count": len(transactions),
        "income": round(income, 2),
        "expenses": round(expenses, 2),
        "balance": round(income - expenses, 2),
        "by_category": by_category,
    }