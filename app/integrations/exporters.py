"""
Functions for exporting data to other formats or systems (e.g., CSV, Google Sheets).
"""
import csv
import io
from typing import List
from app.schema.base import FinalExpense

def export_to_csv(expenses: List[FinalExpense]) -> str:
    """
    Exports a list of expenses to a CSV formatted string.
    """
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(FinalExpense.__fields__.keys())

    # Write data
    for expense in expenses:
        writer.writerow(expense.dict().values())

    return output.getvalue()
