# Personal Budget Manager — Release 1

Command-line tool to add, list and summarize income and expenses. Data is saved to `data/transactions.json`.

## Setup
Requires [uv](https://docs.astral.sh/uv/). From the project folder:

```
uv sync
```

## Run
```
uv run python -m budget_manager.cli add 18.5 --category food --date 2026-09-04
uv run python -m budget_manager.cli add 1500 --kind income --category salary
uv run python -m budget_manager.cli list
uv run python -m budget_manager.cli list --month 2026-09
uv run python -m budget_manager.cli summary
uv run python -m budget_manager.cli import data/sample_transactions.csv
uv run python -m budget_manager.cli --help
```

## Example
```
$ uv run python -m budget_manager.cli add 18.5 --category food --date 2026-09-04
Added T001: expense 18.50 EUR (food)

$ uv run python -m budget_manager.cli add -5
error: amount must be > 0          (exit code 1)

$ uv run python -m budget_manager.cli summary
Transactions: 2
Income:   1500.00
Expenses: 18.50
Balance:  1481.50
```

Exit codes: `0` = success, `1` = invalid data or file error (message on stderr), `2` = wrong command usage.

## Test
```
uv run python tests/test_budget.py
```
Expected: `All tests passed` (1 normal case + 4 boundary cases + 1 save/load round-trip).

## Sample data
`data/sample_transactions.csv` has 3 valid rows and 3 invalid rows (negative amount, unknown category, invalid date) to show the validation rules.

## Known limitations
- Totals assume one currency (no conversion).
- Allowed categories are fixed: food, transport, rent, study, salary, other.
- No undo, and no protection against two runs at the same time (no lock file).