import csv
import os
from collections import defaultdict
from datetime import datetime

from utils import load_expenses, get_expenses_by_month


def monthly_summary(month, year):
    expenses = get_expenses_by_month(month, year)
    if not expenses:
        return {"total": 0, "count": 0, "category_totals": {}}

    total = sum(e["amount"] for e in expenses)
    category_totals = defaultdict(float)
    for e in expenses:
        category_totals[e["category"]] += e["amount"]

    return {
        "total": round(total, 2),
        "count": len(expenses),
        "category_totals": dict(category_totals),
    }


def category_breakdown(month=None, year=None):
    expenses = load_expenses()
    if month and year:
        expenses = get_expenses_by_month(month, year)

    breakdown = defaultdict(lambda: {"total": 0.0, "count": 0})
    for e in expenses:
        breakdown[e["category"]]["total"] += e["amount"]
        breakdown[e["category"]]["count"] += 1

    for cat in breakdown:
        breakdown[cat]["total"] = round(breakdown[cat]["total"], 2)

    return expenses, dict(breakdown)


def export_report(filepath, month=None, year=None):
    if month and year:
        expenses = get_expenses_by_month(month, year)
    else:
        expenses = load_expenses()

    if not expenses:
        return False

    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".csv":
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "date", "category", "amount", "description"])
            writer.writeheader()
            for e in expenses:
                writer.writerow(e)
    else:
        with open(filepath, "w") as f:
            f.write(f"{'ID':<4} {'Date':<12} {'Category':<16} {'Amount':<10} Description\n")
            f.write("-" * 70 + "\n")
            for e in expenses:
                f.write(f"{e['id']:<4} {e['date']:<12} {e['category']:<16} ${e['amount']:<7.2f} {e['description']}\n")

    return True
