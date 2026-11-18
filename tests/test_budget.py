"""Tests for the budget manager. Run with: uv run python tests/test_budget.py"""
from budget_manager import services, storage
from budget_manager.validation import validate_row


def make_row() -> dict:
    """Return a valid row. Each test changes one field."""
    return {"id": "T1", "date": "2026-09-04", "kind": "expense",
            "category": "food", "amount": "18.5"}


# Test 1 (normal): a valid row becomes a Transaction
tx = validate_row(make_row())
assert tx.amount == 18.5
assert tx.signed_amount == -18.5
assert tx.currency == "EUR"
print("Test 1 passed: valid row accepted")

# Test 2 (boundary): amount 0 is rejected
row = make_row()
row["amount"] = "0"
try:
    validate_row(row)
    assert False, "amount 0 should raise ValueError"
except ValueError as e:
    assert "amount must be > 0" in str(e)
print("Test 2 passed: amount 0 rejected")

# Test 3 (malformed input): text instead of a number is rejected
row = make_row()
row["amount"] = "abc"
try:
    validate_row(row)
    assert False, "text amount should raise ValueError"
except ValueError as e:
    assert "amount must be a number" in str(e)
print("Test 3 passed: malformed amount rejected")

# Test 4 (boundary): unknown category is rejected, not silently accepted
row = make_row()
row["category"] = "party"
try:
    validate_row(row)
    assert False, "unknown category should raise ValueError"
except ValueError as e:
    assert "unknown category" in str(e)
print("Test 4 passed: unknown category rejected")

# Test 5 (boundary): impossible date (month 13) is rejected
row = make_row()
row["date"] = "2026-13-01"
try:
    validate_row(row)
    assert False, "month 13 should raise ValueError"
except ValueError as e:
    assert "date must be YYYY-MM-DD" in str(e)
print("Test 5 passed: invalid date rejected")

# Test 6 (boundary): summary of an empty list does not crash
assert services.summarize([])["balance"] == 0
print("Test 6 passed: empty summary is 0")

# Test 7 (boundary): duplicate id is rejected
items = [tx]
try:
    services.add_transaction(items, validate_row(make_row()))
    assert False, "duplicate id should raise ValueError"
except ValueError as e:
    assert "duplicate id" in str(e)
print("Test 7 passed: duplicate id rejected")

# Test 8 (persistence): save then load gives the same data
income_row = make_row()
income_row["id"] = "T2"
income_row["kind"] = "income"
income_row["category"] = "salary"
income_row["amount"] = "100"
items = [tx, validate_row(income_row)]
storage.save("tests/tmp_test.json", items)
loaded = storage.load("tests/tmp_test.json")
assert [t.to_dict() for t in loaded] == [t.to_dict() for t in items]
print("Test 8 passed: save/load round-trip")

print("All tests passed")