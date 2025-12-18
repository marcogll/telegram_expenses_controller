"""
Handler for receiving and processing user messages (text, audio, images).
"""
from telegram import Update
from telegram.ext import ContextTypes
import logging

from app.schema.base import RawInput
# This is a simplified integration. In a real app, you would likely
# have a queue or a more robust way to trigger the processing pipeline.
from app.router import process_expense_input
from app.persistence.db import get_db

logger = logging.getLogger(__name__)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles regular messages and triggers the expense processing pipeline.
    """
    user_id = str(update.effective_user.id)
    
    # This is a very simplified example.
    # A real implementation needs to handle files, voice, etc.
    if update.message.text:
        raw_input = RawInput(
            user_id=user_id,
            type="text",
            data=update.message.text
        )

        try:
            # Get a DB session
            db_session = next(get_db())
            
            # Run the processing pipeline
            result = process_expense_input(db=db_session, raw_input=raw_input)
            
            if result:
                await update.message.reply_text(f"Expense saved successfully! ID: {result.id}")
            else:
                await update.message.reply_text("I couldn't fully process that. It might need manual review.")

        except Exception as e:
            logger.error(f"Error handling message: {e}", exc_info=True)
            await update.message.reply_text("Sorry, an error occurred while processing your request.")

    else:
        await update.message.reply_text("I can currently only process text messages.")
