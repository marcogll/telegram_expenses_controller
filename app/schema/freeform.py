"""
Pydantic schemas for unstructured or freeform text entries.
"""
from pydantic import BaseModel
from datetime import datetime

class FreeformEntry(BaseModel):
    """
    Represents a piece of text that could not be structured into an expense.
    """
    user_id: str
    text: str
    timestamp: datetime
    notes: str = "Could not be automatically categorized."
