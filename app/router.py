"""
Enrutador principal de la aplicación.

Orquesta todo el flujo de trabajo de procesamiento de gastos, desde la entrada hasta la persistencia.
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
    Pipeline completo para procesar una entrada sin procesar.

    1. Ingestión: Convertir la entrada (texto, imagen, etc.) en texto sin procesar.
    2. Extracción por IA: Analizar el texto sin procesar en datos estructurados.
    3. Clasificación/Auditoría por IA: Validar y categorizar el gasto.
    4. Persistencia: Guardar el gasto final confirmado en la base de datos.
    """
    logger.info(f"El enrutador está procesando la entrada para el usuario {raw_input.user_id} de tipo {raw_input.input_type}")

    # 1. Ingestión
    raw_text = ""
    if raw_input.input_type == "text":
        raw_text = text.process_text_input(raw_input.data)
    elif raw_input.input_type == "image":
        # En una aplicación real, los datos serían bytes, no una ruta de cadena
        raw_text = image.process_image_input(raw_input.data.encode()) 
    elif raw_input.input_type == "audio":
        raw_text = audio.process_audio_input(raw_input.data.encode())
    elif raw_input.input_type == "document":
        raw_text = document.process_document_input(raw_input.data.encode())
    else:
        raise ValueError(f"Tipo de entrada no soportado: {raw_input.input_type}")

    if not raw_text:
        logger.error("La fase de ingestión resultó en un texto vacío. Abortando.")
        # Podríamos querer devolver un estado específico aquí
        return None

    # 2. Extracción por IA
    extracted_data = extractor.extract_expense_data(raw_text)
    if not extracted_data.amount or not extracted_data.description:
        logger.error("La extracción por IA no pudo encontrar detalles clave. Abortando.")
        return None

    # 3. Clasificación y Confirmación por IA (simplificado)
    # En un bot real, presentarías esto al usuario para su confirmación.
    provisional_expense = ProvisionalExpense(
        user_id=raw_input.user_id,
        extracted_data=extracted_data,
        confidence_score=0.0 # Será establecido por el clasificador
    )
    
    audited_expense = classifier.classify_and_audit(provisional_expense)
    
    # 3.5 Coincidencia Determinística (Fase 3)
    # Enriquecer los datos con categorías de proveedores/palabras clave si están disponibles
    match_metadata = matcher.get_metadata_from_match(extracted_data.description)
    
    # Por ahora, auto-confirmamos si la confianza es alta.
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
        
        # 4. Persistencia
        db_record = repositories.save_final_expense(db, final_expense)
        logger.info(f"Gasto procesado y guardado con éxito ID {db_record.id}")
        return db_record
    
    else:
        logger.warning(f"El gasto para el usuario {raw_input.user_id} tiene baja confianza. Esperando confirmación manual.")
        # Aquí guardarías el gasto provisional y notificarías al usuario
        return None
