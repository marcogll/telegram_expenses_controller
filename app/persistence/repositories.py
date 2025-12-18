"""
Capa de acceso a datos para la persistencia.
Contiene funciones para interactuar con la base de datos.
"""
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text
from sqlalchemy.orm import Session
import logging

from app.persistence.db import Base, engine
from app.schema.base import FinalExpense

logger = logging.getLogger(__name__)

# --- Modelo ORM de Base de Datos ---
class ExpenseDB(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    
    provider_name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)
    expense_date = Column(Date, nullable=False)
    description = Column(Text, nullable=True)

    category = Column(String, nullable=False)
    subcategory = Column(String, nullable=True)
    expense_type = Column(String, nullable=False)

    confirmed_at = Column(DateTime, nullable=False)
    initial_processing_method = Column(String)

def create_tables():
    """
    Crea todas las tablas de la base de datos definidas por los modelos que heredan de Base.
    """
    if engine:
        logger.info("Creando tablas de base de datos si no existen...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas creadas con éxito.")
    else:
        logger.error("No se pueden crear las tablas, el motor de base de datos no está disponible.")

# --- Funciones del Repositorio ---
def save_final_expense(db: Session, expense: FinalExpense) -> ExpenseDB:
    """
    Guarda un gasto confirmado por el usuario en la base de datos.

    Args:
        db: La sesión de la base de datos.
        expense: El objeto FinalExpense a guardar.

    Returns:
        El objeto ExpenseDB creado.
    """
    logger.info(f"Guardando gasto final para el usuario {expense.user_id} en la base de datos.")
    
    db_expense = ExpenseDB(**expense.dict())
    
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    
    logger.info(f"Gasto guardado con éxito con ID {db_expense.id}.")
    return db_expense
