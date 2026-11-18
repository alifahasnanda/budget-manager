# AI disclosure

## AI-generated code
I used Claude (AI assistant) to explain the requirements step by step and to
provide code for:
- src/budget_manager/models.py
- src/budget_manager/validation.py
- src/budget_manager/services.py
- src/budget_manager/storage.py
- src/budget_manager/cli.py (based on the lecturer's cli.py example)
- tests/test_budget.py
- data/sample_transactions.csv

## Why I used it
I am new to Python and used it as a tutor to understand how to separate the
project into layers and how argparse, validation and file storage work together.

## What I did myself
- Set up the project with `uv init --package` and created the folder structure.
- Ran every step in the terminal and checked the results against the expected outputs.
- Read and checked the code in each file, and made sure claude explain each part so i can understand what it does:
  - models.py: the Transaction class, the signed_amount property and to_dict()
  - validation.py: the order of the checks and why bad data is rejected with clear messages
  - services.py: how IDs are created, how duplicates are blocked, and how totals are calculated
  - storage.py: how data is saved safely (.tmp file first) and loaded again
  - cli.py: how argparse reads commands, and how exit codes and stderr are used
- Tested normal and boundary cases (negative amount, unknown category, invalid date,
  empty list, duplicate ID) and recorded the evidence.