"""
Manejador para recibir y procesar mensajes de usuario (texto, audio, imágenes).
"""
from telegram import Update
from telegram.ext import ContextTypes
import logging

from app.schema.base import RawInput
# Esta es una integración simplificada. En una aplicación real, probablemente
# tendrías una cola o una forma más robusta de activar el pipeline de procesamiento.
from app.router import process_expense_input
from app.persistence.db import get_db

logger = logging.getLogger(__name__)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Maneja mensajes regulares y activa el pipeline de procesamiento de gastos.
    """
    user_id = str(update.effective_user.id)
    
    # Este es un ejemplo muy simplificado.
    # Una implementación real necesita manejar archivos, voz, etc.
    if update.message.text:
        raw_input = RawInput(
            user_id=user_id,
            type="text",
            data=update.message.text
        )

        try:
            # Obtener una sesión de BD
            db_session = next(get_db())
            
            # Ejecutar el pipeline de procesamiento
            result = process_expense_input(db=db_session, raw_input=raw_input)
            
            if result:
                await update.message.reply_text(f"¡Gasto guardado con éxito! ID: {result.id}")
            else:
                await update.message.reply_text("No pude procesar eso completamente. Podría necesitar revisión manual.")

        except Exception as e:
            logger.error(f"Error al manejar el mensaje: {e}", exc_info=True)
            await update.message.reply_text("Lo siento, ocurrió un error al procesar tu solicitud.")

    else:
        await update.message.reply_text("Actualmente solo puedo procesar mensajes de texto.")
