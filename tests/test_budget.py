"""Tests for the budget manager. Run with: uv run python tests/test_budget.py"""
from pathlib import Path

from budget_manager import services, storage
from budget_manager.validation import validate_row


def make_row(**changes):
    """A valid row; change one field per test."""
    row = {"id": "T1", "date": "2026-09-04", "kind": "expense",
           "category": "food", "amount": "18.5"}
    row.update(changes)
    return row


# Test 1 (normal): a valid row becomes a Transaction
tx = validate_row(make_row())
assert tx.amount == 18.5
assert tx.signed_amount == -18.5
print("Test 1 passed: valid row accepted")

# Test 2 (boundary): amount 0 is rejected
try:
    validate_row(make_row(amount="0"))
    assert False, "amount 0 should raise ValueError"
except ValueError as e:
    assert "amount must be > 0" in str(e)
print("Test 2 passed: amount 0 rejected")

# Test 3 (boundary): unknown category is rejected, not silently accepted
try:
    validate_row(make_row(category="party"))
    assert False, "unknown category should raise ValueError"
except ValueError as e:
    assert "unknown category" in str(e)
print("Test 3 passed: unknown category rejected")

# Test 4 (boundary): summary of an empty list does not crash
assert services.summarize([])["balance"] == 0
print("Test 4 passed: empty summary is 0")

# Test 5 (boundary): duplicate id is rejected
items = [tx]
try:
    services.add_transaction(items, validate_row(make_row()))
    assert False, "duplicate id should raise ValueError"
except ValueError as e:
    assert "duplicate id" in str(e)
print("Test 5 passed: duplicate id rejected")

# Test 6 (persistence): save then load gives the same data
items = [tx, validate_row(make_row(id="T2", kind="income", category="salary", amount="100"))]
path = Path("tests/tmp_test.json")
storage.save(path, items)
loaded = storage.load(path)
assert [t.to_dict() for t in loaded] == [t.to_dict() for t in items]
path.unlink()
print("Test 6 passed: save/load round-trip")

print("All tests passed")