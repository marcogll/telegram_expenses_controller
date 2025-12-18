"""
Punto de entrada de la aplicación.

Inicializa la aplicación FastAPI, configura el registro, la base de datos
y define los principales endpoints de la API.
"""
import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# Es crucial configurar la configuración antes de otras importaciones
from app.config import config

# Ahora, configurar el registro basado en la configuración
logging.basicConfig(level=config.LOG_LEVEL.upper())
logger = logging.getLogger(__name__)

# Import other components
from app.schema.base import RawInput
from app.router import process_expense_input
from app.persistence import repositories, db

# Crear tablas de base de datos al inicio
# Esto es simple, pero para producción, usarías migraciones (ej. Alembic)
repositories.create_tables()

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="API del Bot de Gastos de Telegram",
    description="Procesa y gestiona datos de gastos de diversas fuentes.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    logger.info("Inicio de la aplicación completado.")
    logger.info(f"El nivel de registro está establecido en: {config.LOG_LEVEL.upper()}")

@app.get("/", tags=["Estado"])
async def root():
    """Endpoint de verificación de salud."""
    return {"message": "La API del Bot de Gastos de Telegram está en ejecución."}

@app.post("/webhook/telegram", tags=["Webhooks"])
async def process_telegram_update(request: dict):
    """
    Este endpoint recibiría actualizaciones directamente de un webhook de Telegram.
    Necesita ser implementado para analizar el objeto Update de Telegram y
    convertirlo en nuestro modelo RawInput interno.
    """
    logger.info(f"Actualización de Telegram recibida: {request}")
    # TODO: Implementar un analizador para el objeto Update de Telegram.
    # Por ahora, esto es un marcador de posición.
    return {"status": "received", "message": "El manejador de webhook de Telegram no está completamente implementado."}

@app.post("/process-expense", tags=["Procesamiento"])
async def process_expense(raw_input: RawInput, db_session: Session = Depends(db.get_db)):
    """
    Recibe datos de gastos sin procesar, los procesa a través del pipeline completo
    y devuelve el resultado.
    """
    logger.info(f"Entrada sin procesar recibida para procesamiento: {raw_input.dict()}")
    
    try:
        result = process_expense_input(db=db_session, raw_input=raw_input)
        
        if result:
            return {"status": "success", "expense_id": result.id}
        else:
            # Esto podría suceder si la confianza es baja o ocurrió un error
            raise HTTPException(
                status_code=400, 
                detail="Error al procesar el gasto. Puede requerir revisión manual o tenía datos inválidos."
            )

    except ValueError as e:
        logger.error(f"Error de validación: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.critical(f"Ocurrió un error inesperado en el pipeline de procesamiento: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Ocurrió un error interno del servidor.")

# Para ejecutar esta aplicación:
# uvicorn app.main:app --reload
