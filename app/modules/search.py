"""
Handler for the /search command.
"""
from telegram import Update
from telegram.ext import ContextTypes

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Searches the expense database (stub)."""
    await update.message.reply_text("Search command is not yet implemented.")
