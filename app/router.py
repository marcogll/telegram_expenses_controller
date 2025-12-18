"""
Main application router.

Orchestrates the entire expense processing workflow, from input to persistence.
"""
import logging

from app.schema.base import RawInput, ProvisionalExpense, FinalExpense, ExpenseStatus
from app.ingestion import text, image, audio, document
from app.ai import extractor, classifier
from app.preprocessing import matcher
from app.persistence import repositories
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

def process_expense_input(db: Session, raw_input: RawInput) -> FinalExpense:
    """
    Full pipeline for processing a raw input.

    1. Ingestion: Convert input (text, image, etc.) to raw text.
    2. AI Extraction: Parse the raw text into structured data.
    3. AI Classification/Audit: Validate and categorize the expense.
    4. Persistence: Save the final, confirmed expense to the database.
    """
    logger.info(f"Router processing input for user {raw_input.user_id} of type {raw_input.input_type}")

    # 1. Ingestion
    raw_text = ""
    if raw_input.input_type == "text":
        raw_text = text.process_text_input(raw_input.data)
    elif raw_input.input_type == "image":
        # In a real app, data would be bytes, not a string path
        raw_text = image.process_image_input(raw_input.data.encode()) 
    elif raw_input.input_type == "audio":
        raw_text = audio.process_audio_input(raw_input.data.encode())
    elif raw_input.input_type == "document":
        raw_text = document.process_document_input(raw_input.data.encode())
    else:
        raise ValueError(f"Unsupported input type: {raw_input.input_type}")

    if not raw_text:
        logger.error("Ingestion phase resulted in empty text. Aborting.")
        # We might want to return a specific status here
        return None

    # 2. AI Extraction
    extracted_data = extractor.extract_expense_data(raw_text)
    if not extracted_data.amount or not extracted_data.description:
        logger.error("AI extraction failed to find key details. Aborting.")
        return None

    # 3. AI Classification & Confirmation (simplified)
    # In a real bot, you would present this to the user for confirmation.
    provisional_expense = ProvisionalExpense(
        user_id=raw_input.user_id,
        extracted_data=extracted_data,
        confidence_score=0.0 # Will be set by classifier
    )
    
    audited_expense = classifier.classify_and_audit(provisional_expense)
    
    # 3.5 Deterministic Matching (Phase 3)
    # Enrich data with categories from providers/keywords if available
    match_metadata = matcher.get_metadata_from_match(extracted_data.description)
    
    # For now, we auto-confirm if confidence is high.
    if audited_expense.confidence_score > 0.7:
        final_expense = FinalExpense(
            user_id=audited_expense.user_id,
            provider_name=match_metadata.get("matched_name") or audited_expense.extracted_data.description,
            amount=audited_expense.extracted_data.amount,
            currency=audited_expense.extracted_data.currency,
            expense_date=audited_expense.extracted_data.expense_date,
            description=audited_expense.extracted_data.description,
            category=match_metadata.get("category") or audited_expense.category,
            expense_type=match_metadata.get("expense_type") or "personal",
            initial_processing_method=match_metadata.get("match_type") or audited_expense.processing_method,
            confirmed_by="auto-confirm"
        )
        
        # 4. Persistence
        db_record = repositories.save_final_expense(db, final_expense)
        logger.info(f"Successfully processed and saved expense ID {db_record.id}")
        return db_record
    
    else:
        logger.warning(f"Expense for user {raw_input.user_id} has low confidence. Awaiting manual confirmation.")
        # Here you would store the provisional expense and notify the user
        return None
