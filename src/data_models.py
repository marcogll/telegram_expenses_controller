from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date

class RawInput(BaseModel):
    """
    Represents the raw data received from the input source (e.g., n8n).
    """
    user_id: str
    input_type: str = Field(..., alias="type", description="The type of input, e.g., 'text', 'voice', 'image', 'pdf'")
    data: str

class ExtractedExpense(BaseModel):
    """
    Represents an expense after initial data extraction (e.g., from OCR or transcription).
    Fields are mostly optional as extraction may not be perfect.
    """
    provider_name: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = "MXN"
    expense_date: Optional[date] = None
    description: Optional[str] = None
    raw_text: str

class ProvisionalExpense(BaseModel):
    """
    Represents a fully processed but unconfirmed expense.
    This is the state before the user validates the data.
    """
    user_id: str
    extracted_data: ExtractedExpense

    # Classified fields
    category: Optional[str] = "Por Determinar"
    subcategory: Optional[str] = None
    expense_type: Optional[str] = Field(None, alias="tipo_gasto_default", description="e.g., 'personal' or 'negocio'")

    # Metadata
    confidence_score: float
    processing_method: str = Field(..., description="How the expense was classified, e.g., 'provider_match', 'keyword_match', 'ai_inference'")
    validation_notes: List[str] = []
    status: str = "AWAITING_CONFIRMATION"
    timestamp: datetime = Field(default_factory=datetime.now)

class FinalExpense(BaseModel):
    """
    Represents a final, user-confirmed expense record.
    This is the data that will be stored permanently.
    """
    user_id: str
    provider_name: str
    amount: float
    currency: str
    expense_date: date
    description: Optional[str] = None

    category: str
    subcategory: Optional[str] = None
    expense_type: str

    # Audit trail
    initial_processing_method: str
    confirmed_by: str
    confirmed_at: datetime = Field(default_factory=datetime.now)
    audit_log: List[str] = []

    status: str = "CONFIRMED"
