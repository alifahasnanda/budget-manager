"""Save, load, import and back up files."""
import csv
import json
from pathlib import Path

from budget_manager.validation import validate_row


def save(path: str, transactions: list) -> None:
    """Save all transactions to a JSON file (write to .tmp first, then replace)."""
    path = Path(path)
    path.parent.mkdir(exist_ok=True)
    data = [tx.to_dict() for tx in transactions]
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    tmp.replace(path)


def load(path: str) -> list:
    """Load transactions from a JSON file. A missing file gives an empty list."""
    path = Path(path)
    if not path.exists():
        return []
    rows = json.loads(path.read_text(encoding="utf-8"))
    return [validate_row(row) for row in rows]


def load_csv(path: str) -> tuple:
    """Read a CSV file and return (valid transactions, error messages with row numbers)."""
    valid = []
    errors = []
    with Path(path).open("r", encoding="utf-8", newline="") as f:
        for line_no, row in enumerate(csv.DictReader(f), start=2):
            try:
                valid.append(validate_row(row))
            except ValueError as e:
                errors.append(f"Row {line_no}: {e}")
    return valid, errors


def backup(transactions: list, destination: str) -> None:
    """Write a backup file. Mode "x" refuses to overwrite an existing backup.

    Raises:
        FileExistsError: If the destination file already exists.
    """
    with open(destination, "x", encoding="utf-8") as output:
        json.dump([tx.to_dict() for tx in transactions], output, indent=2)