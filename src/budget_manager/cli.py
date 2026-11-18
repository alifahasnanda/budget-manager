"""Command-line interface: read the command, call services, print results."""
import argparse
import sys
from datetime import date

from . import services, storage
from .validation import validate_row

DATA_FILE = "data/transactions.json"


def build_parser():
    parser = argparse.ArgumentParser(prog="budget")
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="add a transaction")
    add.add_argument("amount")
    add.add_argument("--category", default="other")
    add.add_argument("--kind", choices=["expense", "income"], default="expense")
    add.add_argument("--date", default=date.today().isoformat())

    lst = commands.add_parser("list", help="list transactions")
    lst.add_argument("--month", help="YYYY-MM")

    commands.add_parser("summary", help="show totals")

    imp = commands.add_parser("import", help="import a CSV file")
    imp.add_argument("csv_path")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
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
            for tx in rows:
                print(f"{tx.id}  {tx.date}  {tx.kind:<7}  {tx.category:<9}  {tx.amount:>8.2f}")

        elif args.command == "summary":
            s = services.summarize(transactions)
            print(f"Transactions: {s['count']}")
            print(f"Income:   {s['income']:.2f}")
            print(f"Expenses: {s['expenses']:.2f}")
            print(f"Balance:  {s['balance']:.2f}")

        elif args.command == "import":
            new, errors = storage.load_csv(args.csv_path)
            for tx in new:
                services.add_transaction(transactions, tx)
            storage.save(DATA_FILE, transactions)
            print(f"Imported {len(new)} rows")
            for err in errors:
                print(err, file=sys.stderr)
            if errors:
                return 1

    except (ValueError, OSError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())