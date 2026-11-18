"""Command-line interface: read the command, call the other modules, print results."""
import argparse
import sys

from budget_manager import services, storage
from budget_manager.validation import validate_row

DATA_FILE = "data/transactions.json"


def build_parser() -> argparse.ArgumentParser:
    """Define the commands: add, list, summary, import, backup."""
    parser = argparse.ArgumentParser(prog="budget")
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="add a transaction")
    add.add_argument("date", help="YYYY-MM-DD, e.g. 2026-09-04")
    add.add_argument("amount", help="a number greater than 0, e.g. 18.5")
    add.add_argument("--category", default="other", help="e.g. food, rent, salary")
    add.add_argument("--kind", default="expense", help="expense or income")

    show = commands.add_parser("list", help="list transactions")
    show.add_argument("--month", help="only this month, YYYY-MM")

    commands.add_parser("summary", help="show totals and balance")

    imp = commands.add_parser("import", help="import a CSV file")
    imp.add_argument("csv_path")

    backup = commands.add_parser("backup", help="save a copy of all transactions")
    backup.add_argument("destination")
    return parser


def main() -> int:
    """Run one command. Return 0 on success, 1 on error."""
    args = build_parser().parse_args()
    try:
        transactions = storage.load(DATA_FILE)

        if args.command == "add":
            tx = validate_row({"id": services.next_id(transactions), "date": args.date,
                               "kind": args.kind, "category": args.category,
                               "amount": args.amount})
            services.add_transaction(transactions, tx)
            storage.save(DATA_FILE, transactions)
            print(f"Added {tx.id}: {tx.kind} {tx.amount:.2f} {tx.currency} ({tx.category})")

        elif args.command == "list":
            rows = transactions
            if args.month:
                rows = services.filter_by_month(transactions, args.month)
            if len(rows) == 0:
                print("No transactions yet.")
            for tx in rows:
                print(f"{tx.id} | {tx.date} | {tx.kind} | {tx.category} | {tx.amount:.2f} {tx.currency}")

        elif args.command == "summary":
            s = services.summarize(transactions)
            print(f"Transactions: {s['count']}")
            print(f"Income: {s['income']:.2f}")
            print(f"Expenses: {s['expenses']:.2f}")
            print(f"Balance: {s['balance']:.2f}")

        elif args.command == "import":
            new, errors = storage.load_csv(args.csv_path)
            for tx in new:
                services.add_transaction(transactions, tx)
            storage.save(DATA_FILE, transactions)
            print(f"Imported {len(new)} rows")
            for err in errors:
                print(err, file=sys.stderr)
            if len(errors) > 0:
                return 1

        elif args.command == "backup":
            storage.backup(transactions, args.destination)
            print(f"Backup saved to {args.destination}")

    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except FileExistsError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())