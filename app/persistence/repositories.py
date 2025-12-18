"""
Data access layer for persistence.
Contains functions to interact with the database.
"""
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text
from sqlalchemy.orm import Session
import logging

from app.persistence.db import Base, engine
from app.schema.base import FinalExpense

logger = logging.getLogger(__name__)

# --- Database ORM Model ---
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
    Creates all database tables defined by models inheriting from Base.
    """
    if engine:
        logger.info("Creating database tables if they don't exist...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully.")
    else:
        logger.error("Cannot create tables, database engine is not available.")

# --- Repository Functions ---
def save_final_expense(db: Session, expense: FinalExpense) -> ExpenseDB:
    """
    Saves a user-confirmed expense to the database.

    Args:
        db: The database session.
        expense: The FinalExpense object to save.

    Returns:
        The created ExpenseDB object.
    """
    logger.info(f"Saving final expense for user {expense.user_id} to the database.")
    
    db_expense = ExpenseDB(**expense.dict())
    
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    
    logger.info(f"Successfully saved expense with ID {db_expense.id}.")
    return db_expense
