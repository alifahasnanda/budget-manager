# Personal Budget Manager — Release 1

Command-line tool to add, list, summarize, import and back up income and expenses.
Data is saved to `data/transactions.json`.

## Setup
Requires [uv](https://docs.astral.sh/uv/). From the project folder:

```
uv sync
```

## Run
The date comes first, then the amount.

```
uv run budget-manager add 2026-09-04 18.5 --category food
uv run budget-manager add 2026-09-01 1500 --kind income --category salary
uv run budget-manager list
uv run budget-manager list --month 2026-09
uv run budget-manager summary
uv run budget-manager import data/sample_transactions.csv
uv run budget-manager backup data/backup.json
uv run budget-manager --help
```
(`uv run python -m budget_manager.cli ...` works the same way.)

## Example
```
$ uv run budget-manager add 2026-09-04 18.5 --category food
Added T1: expense 18.50 EUR (food)

$ uv run budget-manager add 2026-09-05 -5
error: amount must be > 0                       (exit code 1)

$ uv run budget-manager summary
Transactions: 2
Income: 1500.00
Expenses: 18.50
Balance: 1481.50

$ uv run budget-manager backup data/backup.json
Backup saved to data/backup.json
$ uv run budget-manager backup data/backup.json
error: [Errno 17] File exists: 'data/backup.json'   (old backup is never overwritten)
```

Exit codes: `0` = success, `1` = invalid data or file error (message on stderr),
`2` = wrong command usage (argparse).

## Requirements (acceptance criteria)
| # | Requirement | Example input | Expected result |
|---|---|---|---|
| R1 | Add a valid transaction | `add 2026-09-04 18.5 --category food` | `Added T1: expense 18.50 EUR (food)`, exit 0 |
| R2 | Amount must be a number greater than 0 | `add 2026-09-05 -5` / `0` / `abc` | `error: amount must be > 0` or `amount must be a number`, exit 1 |
| R3 | Category must be one of: food, transport, rent, study, salary, other | `add 2026-09-05 10 --category party` | `error: unknown category 'party'`, exit 1 (never changed to "other") |
| R4 | Kind must be expense or income | `add 2026-09-05 10 --kind gift` | `error: kind must be 'expense' or 'income'`, exit 1 |
| R5 | Date must be YYYY-MM-DD with month 01–12 and day 01–31 | `add 2026-13-01 10` | `error: date must be YYYY-MM-DD`, exit 1 |
| R6 | Currency is optional (default EUR) and must be a 3-letter code | CSV row with `EUROX` | row rejected with a clear message |
| R7 | Summary shows count, income, expenses and balance | `summary` after R1 + a 1500 income | `Balance: 1481.50` |
| R8 | Empty data does not crash | `list` / `summary` with no data | `No transactions yet.` / all totals 0.00 |
| R9 | CSV import keeps valid rows and reports invalid rows with their row number | `import data/sample_transactions.csv` | `Imported 3 rows` + `Row 5: amount must be > 0`, ..., exit 1 |
| R10 | Duplicate IDs are rejected | importing the same CSV twice | `error: duplicate id T101`, nothing imported |
| R11 | Data is saved and loaded again (persistence) | add, then run `list` again | the same transactions are shown |
| R12 | A backup never overwrites an existing backup | `backup data/backup.json` twice | second time: `File exists`, exit 1 |

## Test
```
uv run python tests/test_budget.py
```
Expected: `All tests passed` — 1 normal case, 6 boundary / malformed-input cases
(amount 0, amount "abc", unknown category, month 13, empty list, duplicate id)
and 1 save/load round-trip.

## Sample data
`data/sample_transactions.csv` has 3 valid rows and 3 invalid rows
(negative amount, unknown category, invalid date) to show the validation rules.

## Known limitations
- Totals assume one currency (no conversion).
- Allowed categories are fixed: food, transport, rent, study, salary, other.
- The date check does not know month lengths (e.g. 2026-02-31 is accepted).
- Importing the same CSV twice is rejected because of duplicate IDs.
- No undo, and no protection against two runs at the same time (no lock file).