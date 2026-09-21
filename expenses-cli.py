import csv
import os
import argparse
import shlex
from datetime import date


class MyArgumentParser(argparse.ArgumentParser):

    def error(self, message):
        print("Invalid command. Type 'expense-cli help' for available commands.")
        self.exit(2)


def getid():
    try:
        with open("expenses.csv", "r") as file:
            reader = csv.reader(file)
            rows = list(reader)

            if len(rows) > 1:
                last_row = rows[-1]
                return int(last_row[0]) + 1
            else:
                return 1

    except FileNotFoundError:
        return 1


def addExpense(description, amount, id):
    file_exists = os.path.exists("expenses.csv")

    with open("expenses.csv", "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["ID", "Date", "Description", "Amount"])

        writer.writerow([
            id,
            date.today().strftime("%Y-%m-%d"),
            description,
            amount
        ])

    print(f"Expense added successfully (ID: {id})")


def updateExpense(id, description, amount):

    with open("expenses.csv", "r") as file:
        reader = csv.reader(file)
        rows = list(reader)

    if len(rows) <= 1:
        print("No expenses found.")
        return

    found = False

    for row in rows[1:]:

        if int(row[0]) == id:

            if description is not None:
                row[2] = description

            if amount is not None:
                row[3] = amount

            found = True
            break

    if not found:
        print(f"Expense with ID {id} not found.")
        return

    with open("expenses.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print(f"Expense with ID {id} updated successfully.")


def deleteExpense(id):

    with open("expenses.csv", "r") as file:
        reader = csv.reader(file)
        rows = list(reader)

    if len(rows) <= 1:
        print("No expenses found.")
        return

    found = False

    with open("expenses.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(rows[0])

        for row in rows[1:]:

            if int(row[0]) == id:
                found = True
            else:
                writer.writerow(row)

    if found:
        print(f"Expense with ID {id} deleted successfully.")
    else:
        print(f"Expense with ID {id} not found.")


def viewExpenses():

    try:
        with open("expenses.csv", "r") as file:
            reader = csv.reader(file)
            rows = list(reader)

    except FileNotFoundError:
        print("No expenses found.")
        return

    if len(rows) <= 1:
        print("No expenses found.")
        return

    print("ID | Date | Description | Amount")

    for row in rows[1:]:
        print(" | ".join(row))


def summaryExpenses(month, year):

    if month is not None and year is None:
        year = date.today().year

    try:
        with open("expenses.csv", "r") as file:
            reader = csv.reader(file)
            rows = list(reader)

    except FileNotFoundError:
        print("No expenses found.")
        return

    if len(rows) <= 1:
        print("No expenses found.")
        return

    total_amount = 0
    found = False

    for row in rows[1:]:

        expense_date = row[1]

        expense_year, expense_month, _ = expense_date.split("-")

        if (
            (month is None or expense_month == f"{month:02d}")
            and
            (year is None or expense_year == str(year))
        ):
            total_amount += float(row[3])
            found = True

    if not found:
        print("No expenses found for the specified period.")
        return

    if month is not None and year is not None:
        print(f"Total Expenses for {month:02d}/{year}: {total_amount}")

    elif year is not None:
        print(f"Total Expenses for year {year}: {total_amount}")
    elif month is not None:
        print(f"Total Expenses for month {month:02d}: {total_amount}")
    else:
        print(f"Total Expenses: {total_amount}")




parser = MyArgumentParser(
    prog="expense-cli",
    description="Expense Tracker CLI"
)

subparsers = parser.add_subparsers(
    dest="command",
    parser_class=MyArgumentParser
)


# ADD
add_parser = subparsers.add_parser("add")

add_parser.add_argument(
    "--description",
    required=True
)

add_parser.add_argument(
    "--amount",
    required=True,
    type=float
)


# UPDATE
update_parser = subparsers.add_parser("update")

update_parser.add_argument(
    "--id",
    required=True,
    type=int
)

update_parser.add_argument(
    "--description"
)

update_parser.add_argument(
    "--amount",
    type=float
)


# DELETE
delete_parser = subparsers.add_parser("delete")

delete_parser.add_argument(
    "--id",
    required=True,
    type=int
)


# LIST
list_parser = subparsers.add_parser("list")


# SUMMARY
summary_parser = subparsers.add_parser("summary")

summary_parser.add_argument(
    "--month",
    type=int
)

summary_parser.add_argument(
    "--year",
    type=int
)


# =========================
# MAIN PROGRAM
# =========================

id = getid()
print(
        "Welcome to the Expense Tracker! "
        "Type 'help' for available commands."
    )
while True:

    

    try:
        user = input(">> expense-cli ")

    except KeyboardInterrupt:
        print("\nExiting Expense Tracker.")
        break

    if user.lower() == "exit":
        print("Exiting Expense Tracker.")
        break

    if user.lower() == "clear":
        os.system("cls" if os.name == "nt" else "clear")
        continue

    if user.lower() == "help":
        parser.print_help()
        print("\nCommands:")
        print("  add")
        print("  update")
        print("  delete")
        print("  list")
        print("  summary")
        print("  help")
        print("  clear")
        print("  exit")
        continue

    try:
        args = parser.parse_args(shlex.split(user))

        if args.command == "add":

            addExpense(
                args.description,
                args.amount,
                id
            )

            id += 1

        elif args.command == "update":

            if args.description is None and args.amount is None:
                print(
                    "Please provide --description or --amount."
                )
                continue

            updateExpense(
                args.id,
                args.description,
                args.amount
            )

        elif args.command == "delete":

            deleteExpense(args.id)

        elif args.command == "list":

            viewExpenses()

        elif args.command == "summary":

            if args.month is not None:
                if args.month < 1 or args.month > 12:
                    print("Month must be between 1 and 12.")
                    continue

            summaryExpenses(
                args.month,
                args.year
            )

        else:
            print(
                "Invalid command. "
                "Type 'expense-cli help' for available commands."
            )

    except SystemExit:
        continue

    except ValueError:
        print("Invalid value. Please check your input.")

    except Exception as e:
        print(f"Error: {e}")