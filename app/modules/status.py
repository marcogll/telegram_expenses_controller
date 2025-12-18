"""
Handler for the /status command.
"""
from telegram import Update
from telegram.ext import ContextTypes

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows the status of the last processed expense (stub)."""
    await update.message.reply_text("Status command is not yet implemented.")
