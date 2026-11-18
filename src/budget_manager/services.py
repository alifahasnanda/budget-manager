"""Budget logic. No input(), no print(), no files."""


def next_id(transactions):
    return f"T{len(transactions) + 1:03d}"


def add_transaction(transactions, new_tx):
    for tx in transactions:
        if tx.id == new_tx.id:
            raise ValueError(f"duplicate id {new_tx.id}")
    transactions.append(new_tx)


def filter_by_month(transactions, month):
    return [tx for tx in transactions if tx.date.startswith(month)]


def summarize(transactions):
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