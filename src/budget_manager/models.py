"""Transaction schema: what one transaction looks like."""

KINDS = {"expense", "income"}
CATEGORIES = {"food", "transport", "rent", "study", "salary", "other"}


class Transaction:
    """One money movement (an expense or an income)."""

    def __init__(self, id: str, date: str, kind: str, category: str,
                 amount: float, currency: str = "EUR") -> None:
        self.id = id
        self.date = date
        self.kind = kind
        self.category = category
        self.amount = amount
        self.currency = currency

    @property
    def signed_amount(self) -> float:
        """Return the amount as negative for an expense, positive for an income."""
        if self.kind == "expense":
            return -self.amount
        return self.amount

    def to_dict(self) -> dict:
        """Return the transaction as a dict, so it can be saved as JSON."""
        return {"id": self.id, "date": self.date, "kind": self.kind,
                "category": self.category, "amount": self.amount,
                "currency": self.currency}