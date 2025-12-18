"""
Manejador para el comando /start.
"""
from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envía un mensaje de bienvenida cuando se emite el comando /start."""
    user = update.effective_user
    await update.message.reply_html(
        rf"¡Hola {user.mention_html()}! Bienvenido al Bot de Gastos. "
        "Envíame un mensaje con un gasto (ej., 'comida 25 eur') "
        "o reenvía un mensaje de voz o una imagen de un recibo.",
    )
