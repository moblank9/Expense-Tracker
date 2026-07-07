import json
import os
from datetime import datetime


DATA_FILE = os.path.join(os.path.dirname(__file__), "expenses.json")


def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def validate_amount(amount_str):
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        return round(amount, 2)
    except ValueError:
        raise ValueError("Invalid amount. Enter a positive number.")


def validate_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date. Use YYYY-MM-DD format.")


def add_expense(amount, category, description, date_str=None):
    expenses = load_expenses()
    amount = validate_amount(amount)
    category = category.strip().capitalize()
    description = description.strip()
    date = validate_date(date_str) if date_str else datetime.today().date()

    expense = {
        "id": max((e["id"] for e in expenses), default=0) + 1,
        "amount": amount,
        "category": category,
        "description": description,
        "date": date.isoformat(),
    }
    expenses.append(expense)
    save_expenses(expenses)
    return expense


def get_expense_by_id(expense_id):
    expenses = load_expenses()
    for e in expenses:
        if e["id"] == expense_id:
            return e
    return None


def edit_expense(expense_id, field, value):
    expenses = load_expenses()
    for e in expenses:
        if e["id"] == expense_id:
            if field == "amount":
                e["amount"] = validate_amount(value)
            elif field == "category":
                e["category"] = value.strip().capitalize()
            elif field == "description":
                e["description"] = value.strip()
            elif field == "date":
                e["date"] = validate_date(value).isoformat()
            else:
                raise ValueError(f"Unknown field: {field}")
            save_expenses(expenses)
            return e
    raise ValueError(f"Expense with id {expense_id} not found.")


def delete_expense(expense_id):
    expenses = load_expenses()
    new_expenses = [e for e in expenses if e["id"] != expense_id]
    if len(new_expenses) == len(expenses):
        raise ValueError(f"Expense with id {expense_id} not found.")
    save_expenses(new_expenses)
    return True


def search_expenses(keyword=None, category=None, start_date=None, end_date=None):
    expenses = load_expenses()
    results = []

    for e in expenses:
        if keyword and keyword.lower() not in e["description"].lower():
            continue
        if category and category.lower() != e["category"].lower():
            continue
        if start_date and e["date"] < start_date:
            continue
        if end_date and e["date"] > end_date:
            continue
        results.append(e)

    return results


def get_expenses_by_month(month, year):
    expenses = load_expenses()
    return [
        e for e in expenses
        if datetime.fromisoformat(e["date"]).month == month
        and datetime.fromisoformat(e["date"]).year == year
    ]
