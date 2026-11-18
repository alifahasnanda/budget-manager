"""Transaction schema."""

KINDS = {"expense", "income"}
CATEGORIES = {"food", "transport", "rent", "study", "salary", "other"}


class Transaction:
    def __init__(self, id, date, kind, category, amount, currency="EUR"):
        self.id = id
        self.date = date
        self.kind = kind
        self.category = category
        self.amount = amount
        self.currency = currency

    @property
    def signed_amount(self):
        """Expenses are negative, income is positive."""
        if self.kind == "expense":
            return -self.amount
        return self.amount

    def to_dict(self):
        return {"id": self.id, "date": self.date, "kind": self.kind,
                "category": self.category, "amount": self.amount,
                "currency": self.currency}