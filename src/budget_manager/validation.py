"""Boundary checks: turn raw text into a valid Transaction or raise ValueError."""
from budget_manager.models import CATEGORIES, KINDS, Transaction

REQUIRED = ["id", "date", "kind", "category", "amount"]


def check_date(text: str) -> str:
    """Return the date if it looks like YYYY-MM-DD.

    Raises:
        ValueError: If the format, month or day is not valid.
    """
    parts = text.split("-")
    if len(parts) != 3 or len(parts[0]) != 4 or len(parts[1]) != 2 or len(parts[2]) != 2:
        raise ValueError(f"date must be YYYY-MM-DD, got '{text}'")
    for part in parts:
        if not part.isdigit():
            raise ValueError(f"date must be YYYY-MM-DD, got '{text}'")
    month = int(parts[1])
    day = int(parts[2])
    if month < 1 or month > 12 or day < 1 or day > 31:
        raise ValueError(f"date must be YYYY-MM-DD, got '{text}'")
    return text


def validate_row(row: dict) -> Transaction:
    """Check one raw row (text values) and return a Transaction.

    Args:
        row: A dict with id, date, kind, category, amount and optional currency.
    Returns:
        A clean Transaction.
    Raises:
        ValueError: With a clear message if any field is missing or invalid.
    """
    # 1. required fields must be present and not empty
    for field in REQUIRED:
        if str(row.get(field, "")).strip() == "":
            raise ValueError(f"missing required field '{field}'")

    # 2. date must be YYYY-MM-DD
    date = check_date(str(row["date"]).strip())

    # 3. kind must be expense or income
    kind = str(row["kind"]).strip().lower()
    if kind not in KINDS:
        raise ValueError(f"kind must be 'expense' or 'income', got '{row['kind']}'")

    # 4. category must be in the allowed list (policy: reject, never guess)
    category = str(row["category"]).strip().lower()
    if category not in CATEGORIES:
        raise ValueError(f"unknown category '{row['category']}'")

    # 5. amount must be a number greater than 0
    try:
        amount = float(str(row["amount"]).strip())
    except ValueError:
        raise ValueError(f"amount must be a number, got '{row['amount']}'")
    if amount <= 0:
        raise ValueError("amount must be > 0")

    # 6. currency: optional, default EUR, must be 3 letters (ISO code)
    currency = str(row.get("currency", "")).strip().upper()
    if currency == "":
        currency = "EUR"
    if len(currency) != 3 or not currency.isalpha():
        raise ValueError(f"currency must be a 3-letter code, got '{row['currency']}'")

    return Transaction(str(row["id"]).strip(), date, kind, category, amount, currency)