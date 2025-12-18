"""
Handlers for admin-only commands.
"""
from telegram import Update
from telegram.ext import ContextTypes

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles an admin-specific command (stub)."""
    # You would add a permission check here
    await update.message.reply_text("Admin command is not yet implemented.")
