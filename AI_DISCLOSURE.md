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
- Set up the project with uv, created the files and published it to GitHub with Git.
- Ran every step in the terminal and compared the results with the expected outputs.
- Read the code in each file and asked Claude to explain each part so I can
  understand what it does.
- Ran the normal and boundary cases myself and checked them against the Requirements table in README.md.