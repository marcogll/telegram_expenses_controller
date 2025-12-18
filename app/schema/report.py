"""
Pydantic schemas for reports or summaries.
"""
from pydantic import BaseModel
from typing import List
from datetime import date

class ExpenseReport(BaseModel):
    """
    Represents a summary or report of multiple expenses.
    """
    report_name: str
    start_date: date
    end_date: date
    total_amount: float
    expense_count: int
    # In a real app, you'd link to the actual expense models
    expenses: List[int] 
