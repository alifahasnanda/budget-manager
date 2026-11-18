"""Boundary checks with clear error messages."""
from datetime import date

from .models import CATEGORIES, KINDS, Transaction

REQUIRED = ["id", "date", "kind", "category", "amount"]


def validate_row(row):
    """Turn one raw row (text values) into a Transaction, or raise ValueError."""
    # 1. required fields
    for field in REQUIRED:
        if str(row.get(field, "")).strip() == "":
            raise ValueError(f"missing required field '{field}'")

    # 2. date must be YYYY-MM-DD
    try:
        clean_date = date.fromisoformat(str(row["date"]).strip()).isoformat()
    except ValueError:
        raise ValueError(f"date must be YYYY-MM-DD, got '{row['date']}'")

    # 3. kind must be expense or income
    kind = str(row["kind"]).strip().lower()
    if kind not in KINDS:
        raise ValueError(f"kind must be 'expense' or 'income', got '{row['kind']}'")

    # 4. category must be in the allowed list (policy: reject, never guess)
    category = str(row["category"]).strip().lower()
    if category not in CATEGORIES:
        raise ValueError(f"unknown category '{row['category']}'")

    # 5. amount must be a number > 0
    try:
        amount = float(str(row["amount"]).strip())
    except ValueError:
        raise ValueError(f"amount must be a number, got '{row['amount']}'")
    if amount <= 0:
        raise ValueError("amount must be > 0")

    currency = str(row.get("currency") or "EUR").strip().upper()
    return Transaction(str(row["id"]).strip(), clean_date, kind, category, amount, currency)