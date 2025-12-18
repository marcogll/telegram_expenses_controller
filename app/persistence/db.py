"""
Conexión a la base de datos y gestión de sesiones.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

from app.config import config

logger = logging.getLogger(__name__)

try:
    # El argumento 'check_same_thread' es específico de SQLite.
    engine_args = {"check_same_thread": False} if config.DATABASE_URL.startswith("sqlite") else {}
    
    engine = create_engine(
        config.DATABASE_URL,
        connect_args=engine_args
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()

    logger.info("Motor de base de datos creado con éxito.")

except Exception as e:
    logger.critical(f"Error al conectar con la base de datos: {e}")
    # Salir o manejar el error crítico apropiadamente
    engine = None
    SessionLocal = None
    Base = None

def get_db():
    """
    Dependencia para que las rutas de FastAPI obtengan una sesión de BD.
    """
    if SessionLocal is None:
        raise Exception("Database is not configured. Cannot create session.")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
