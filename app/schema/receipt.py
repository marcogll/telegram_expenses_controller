"""
Pydantic schemas for structured receipts.
"""
from app.schema.base import FinalExpense

class Receipt(FinalExpense):
    """
    A specialized expense model for receipts, could include line items in the future.
    """
    pass
