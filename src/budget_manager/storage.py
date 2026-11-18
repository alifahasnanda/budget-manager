"""Save and load files."""
import csv
import json
from pathlib import Path

from .validation import validate_row


def save(path, transactions):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = [tx.to_dict() for tx in transactions]
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    tmp.replace(path)                      # safe write


def load(path):
    path = Path(path)
    if not path.exists():
        return []
    rows = json.loads(path.read_text(encoding="utf-8"))
    return [validate_row(row) for row in rows]


def load_csv(path):
    valid = []
    errors = []
    with open(path, encoding="utf-8", newline="") as f:
        for line_no, row in enumerate(csv.DictReader(f), start=2):
            try:
                valid.append(validate_row(row))
            except ValueError as e:
                errors.append(f"Row {line_no}: {e}")
    return valid, errors