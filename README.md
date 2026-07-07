Personal Expense Tracker

A CLI-based personal expense tracker built with Python. Manage your daily expenses, view reports, and export data — all from the terminal.

Features

- **Dashboard** – Quick overview of total spending, entry count, average, top category, and recent entries.
- **Add Expense** – Record new expenses with amount, category, description, and date.
- **Edit Expense** – Update any field of an existing expense by ID.
- **Delete Expense** – Remove an expense after confirmation.
- **Search Expenses** – Filter by keyword, category, and date range.
- **Monthly Summary** – View total spent and a category breakdown for a given month and year.
- **Category Breakdown** – See what percentage of your spending goes to each category.
- **Export Report** – Save expenses as a CSV or text file.

Project Structure

```
expense-tracker/
├── main.py          # Entry point and interactive menu
├── utils.py         # CRUD operations, file I/O, validation
├── reports.py       # Monthly summary, category breakdown, export
├── expenses.json    # Data store (auto-created on first use)
└── README.md        # This file
```

Requirements

- Python 3.7+

No external dependencies — uses only the standard library (`json`, `csv`, `datetime`, `os`, `collections`).

Usage

```bash
cd expense-tracker/
python main.py
```

Menu Options

| Option |                  Description                  |
|--------|-----------------------------------------------|
|   `1`  | Dashboard – see financial overview            |
|   `2`  | Add a new expense                             |
|   `3`  | Edit an existing expense (by ID)              |
|   `4`  | Delete an expense (by ID)                     |
|   `5`  | Search expenses by keyword, category, or date |
|   `6`  | Monthly summary with category breakdown       |
|   `7`  | Full category breakdown with percentages      |
|   `8`  | Export expenses to CSV or text file           |
|   `0`  | Exit                                          |

Example Categories

- Food
- Transport
- Internet
- Entertainment
- Rent
- Utilities

Data Storage

All data is saved to `expenses.json` in JSON format:

```json
[
  {
    "id": 1,
    "amount": 25.50,
    "category": "Food",
    "description": "Lunch at cafe",
    "date": "2026-07-06"
  }
]
```

Error Handling

- Invalid amounts, dates, and IDs are caught with descriptive messages.
- Corrupted or missing JSON files are handled gracefully (returns empty list).
- All user-facing errors are displayed without crashing the app.

Concepts Demonstrated

- JSON file reading/writing
- `datetime` parsing and formatting
- Functions, modules, and imports
- Exception handling (`try`/`except`)
- Lists and dictionaries
- String formatting and alignment
- File management (CSV/text export)
- Project organization
