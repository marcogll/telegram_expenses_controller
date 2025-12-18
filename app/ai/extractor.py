"""
Extracción de datos impulsada por IA a partir de texto sin procesar.
"""
import openai
import json
import logging
from typing import Dict, Any

from app.config import config
from app.ai.prompts import EXTRACTOR_PROMPT
from app.schema.base import ExtractedExpense

# Configure the OpenAI client
openai.api_key = config.OPENAI_API_KEY

logger = logging.getLogger(__name__)

def extract_expense_data(text: str) -> ExtractedExpense:
    """
    Utiliza un modelo de IA para extraer datos de gastos estructurados de una cadena de texto sin procesar.

    Args:
        text: El texto sin procesar de la entrada del usuario, OCR o transcripción.

    Returns:
        Un objeto ExtractedExpense con los datos encontrados por la IA.
    """
    logger.info(f"Iniciando extracción por IA para el texto: '{text[:100]}...'")
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or another suitable model
            messages=[
                {"role": "system", "content": EXTRACTOR_PROMPT},
                {"role": "user", "content": text}
            ],
            temperature=0.0,
            response_format={"type": "json_object"}
        )

        # La respuesta de OpenAI debería ser una cadena JSON en el contenido del mensaje
        json_response = response.choices[0].message['content']
        extracted_data = json.loads(json_response)
        
        logger.info(f"Extracción por IA exitosa. JSON sin procesar: {extracted_data}")

        # Añadir el texto original al modelo para fines de auditoría
        extracted_data['raw_text'] = text

        return ExtractedExpense(**extracted_data)

    except json.JSONDecodeError as e:
        logger.error(f"Error al decodificar JSON de la respuesta de la IA: {e}")
        # Devolver un modelo con solo el texto sin procesar para revisión manual
        return ExtractedExpense(raw_text=text)
    except Exception as e:
        logger.error(f"Ocurrió un error inesperado durante la extracción por IA: {e}")
        # Devolver un modelo con solo el texto sin procesar
        return ExtractedExpense(raw_text=text)

