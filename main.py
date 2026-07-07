import os
from datetime import datetime

from utils import (
    add_expense,
    edit_expense,
    delete_expense,
    search_expenses,
    get_expense_by_id,
    load_expenses,
    validate_amount,
    validate_date,
)
from reports import monthly_summary, category_breakdown, export_report


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def print_header(title):
    clear()
    print("=" * 60)
    print(f"{title:^60}")
    print("=" * 60)


def print_expenses(expenses):
    if not expenses:
        print("\n  No expenses found.\n")
        return

    print(f"\n  {'ID':<4} {'Date':<12} {'Category':<16} {'Amount':<10} Description")
    print(f"  {'-'*4:<4} {'-'*12:<12} {'-'*16:<16} {'-'*10:<10} {'-'*30}")
    for e in expenses:
        print(f"  {e['id']:<4} {e['date']:<12} {e['category']:<16} ${e['amount']:<7.2f} {e['description']}")
    print()


def wait_for_enter():
    input("\n  Press Enter to continue...")


def dashboard():
    print_header("Personal Expense Tracker - Dashboard")
    expenses = load_expenses()

    total = sum(e["amount"] for e in expenses)
    count = len(expenses)
    avg = round(total / count, 2) if count else 0

    print(f"\n  Total Expenses : ${total:<8.2f}")
    print(f"  Number of Entries : {count:<8}")
    print(f"  Average Amount    : ${avg:<8.2f}")

    if count:
        cats = {}
        for e in expenses:
            cats[e["category"]] = cats.get(e["category"], 0) + e["amount"]
        top_cat = max(cats, key=cats.get)
        print(f"  Top Category     : {top_cat} (${cats[top_cat]:.2f})")

    print("\n  --- Recent Expenses ---")
    recent = sorted(expenses, key=lambda x: x["date"], reverse=True)[:5]
    print_expenses(recent)
    wait_for_enter()


def add_expense_menu():
    print_header("Add New Expense")
    try:
        amount = input("  Amount          : ")
        amount = validate_amount(amount)
        category = input("  Category        : ").strip().capitalize()
        description = input("  Description     : ").strip()
        date_str = input("  Date (YYYY-MM-DD, Enter for today): ").strip()

        if date_str:
            validate_date(date_str)
        else:
            date_str = None

        expense = add_expense(amount, category, description, date_str)
        print(f"\n  ✓ Expense added (ID: {expense['id']})")
    except ValueError as e:
        print(f"\n  ✗ Error: {e}")
    wait_for_enter()


def edit_expense_menu():
    print_header("Edit Expense")
    try:
        expense_id = int(input("  Enter Expense ID: "))
        expense = get_expense_by_id(expense_id)
        if not expense:
            print(f"\n  ✗ Expense with ID {expense_id} not found.")
            wait_for_enter()
            return

        print(f"\n  Current: ${expense['amount']} | {expense['category']} | {expense['description']} | {expense['date']}")
        print("\n  Fields: amount, category, description, date")
        field = input("  Field to edit   : ").strip().lower()
        value = input("  New value       : ").strip()

        result = edit_expense(expense_id, field, value)
        print(f"\n  ✓ Expense updated: ${result['amount']} | {result['category']} | {result['description']} | {result['date']}")
    except ValueError as e:
        print(f"\n  ✗ Error: {e}")
    wait_for_enter()


def delete_expense_menu():
    print_header("Delete Expense")
    try:
        expense_id = int(input("  Enter Expense ID: "))
        expense = get_expense_by_id(expense_id)
        if expense:
            print(f"  {expense['id']:<4} {expense['date']:<12} {expense['category']:<16} ${expense['amount']:<7.2f} {expense['description']}")
            confirm = input("\n  Delete this entry? (y/N): ").strip().lower()
            if confirm == "y":
                delete_expense(expense_id)
                print("  ✓ Expense deleted.")
            else:
                print("  Cancelled.")
        else:
            print(f"  ✗ Expense with ID {expense_id} not found.")
    except ValueError as e:
        print(f"\n  ✗ Error: {e}")
    wait_for_enter()


def search_expenses_menu():
    print_header("Search Expenses")
    keyword = input("  Keyword (description): ").strip() or None
    category = input("  Category filter      : ").strip() or None
    start = input("  Start date (YYYY-MM-DD): ").strip() or None
    end = input("  End date (YYYY-MM-DD)  : ").strip() or None

    if start:
        start = validate_date(start).isoformat()
    if end:
        end = validate_date(end).isoformat()

    results = search_expenses(keyword, category, start, end)
    print_expenses(results)
    print(f"  Found {len(results)} result(s).")
    wait_for_enter()


def monthly_summary_menu():
    print_header("Monthly Summary")
    now = datetime.now()
    month_str = input(f"  Month (1-12, Enter for {now.month}): ").strip()
    year_str = input(f"  Year (Enter for {now.year}): ").strip()

    month = int(month_str) if month_str else now.month
    year = int(year_str) if year_str else now.year

    try:
        report = monthly_summary(month, year)
        print(f"\n  Summary for {month:02d}/{year}")
        print(f"  {'─' * 40}")
        print(f"  Total spent  : ${report['total']:<8.2f}")
        print(f"  Entries      : {report['count']:<8}")
        print(f"\n  Category Breakdown:")
        for cat, amt in sorted(report["category_totals"].items(), key=lambda x: x[1], reverse=True):
            print(f"    {cat:<20} ${amt:<8.2f}")
    except ValueError as e:
        print(f"\n  ✗ Error: {e}")
    wait_for_enter()


def category_breakdown_menu():
    print_header("Category Breakdown")
    now = datetime.now()
    month_str = input(f"  Month (1-12, Enter for all time): ").strip()
    year_str = input(f"  Year (Enter for all time): ").strip()

    month = int(month_str) if month_str else None
    year = int(year_str) if year_str else None

    raw_expenses, breakdown = category_breakdown(month, year)

    if not breakdown:
        print("\n  No expenses to show.")
    else:
        total_spent = sum(v["total"] for v in breakdown.values())
        print(f"\n  {'Category':<20} {'Count':<8} {'Total':<12} {'%':<8}")
        print(f"  {'─' * 48}")
        for cat, data in sorted(breakdown.items(), key=lambda x: x[1]["total"], reverse=True):
            pct = (data["total"] / total_spent * 100) if total_spent else 0
            print(f"  {cat:<20} {data['count']:<8} ${data['total']:<9.2f} {pct:<7.1f}%")
        print(f"  {'─' * 48}")
        print(f"  {'TOTAL':<20} {sum(v['count'] for v in breakdown.values()):<8} ${total_spent:<9.2f} 100.0%")
    wait_for_enter()


def export_menu():
    print_header("Export Report")
    now = datetime.now()
    month_str = input(f"  Month (1-12, Enter for all): ").strip()
    year_str = input(f"  Year (Enter for all): ").strip()

    month = int(month_str) if month_str else None
    year = int(year_str) if year_str else None

    default_name = f"expenses-{year or 'all'}-{month or 'all'}"
    filename = input(f"  Output file (default: {default_name}.csv): ").strip()
    if not filename:
        filename = f"{default_name}.csv"

    try:
        success = export_report(filename, month, year)
        if success:
            abs_path = os.path.abspath(filename)
            print(f"\n  ✓ Report exported to: {abs_path}")
        else:
            print("\n  No expenses to export.")
    except Exception as e:
        print(f"\n  ✗ Error: {e}")
    wait_for_enter()


def main():
    while True:
        clear()
        print("=" * 60)
        print("          Personal Expense Tracker")
        print("=" * 60)
        expenses = load_expenses()
        total = sum(e["amount"] for e in expenses)
        print(f"\n  Balance: ${total:.2f} across {len(expenses)} entries\n")
        print("  [1] Dashboard")
        print("  [2] Add Expense")
        print("  [3] Edit Expense")
        print("  [4] Delete Expense")
        print("  [5] Search Expenses")
        print("  [6] Monthly Summary")
        print("  [7] Category Breakdown")
        print("  [8] Export Report")
        print("  [0] Exit")
        print("\n" + "=" * 60)
        choice = input("  Choose an option: ").strip()

        menu_map = {
            "1": dashboard,
            "2": add_expense_menu,
            "3": edit_expense_menu,
            "4": delete_expense_menu,
            "5": search_expenses_menu,
            "6": monthly_summary_menu,
            "7": category_breakdown_menu,
            "8": export_menu,
            "0": lambda: (print("  Goodbye!"), exit(0)),
        }

        action = menu_map.get(choice)
        if action:
            try:
                action()
            except Exception as e:
                print(f"\n  ✗ Unexpected error: {e}")
                wait_for_enter()
        else:
            print("\n  ✗ Invalid choice.")
            wait_for_enter()


if __name__ == "__main__":
    main()
