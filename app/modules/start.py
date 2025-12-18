"""
Handler for the /start command.
"""
from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message when the /start command is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! Welcome to the Expense Bot. "
        "Send me a message with an expense (e.g., 'lunch 25 eur') "
        "or forward a voice message or receipt image.",
    )
