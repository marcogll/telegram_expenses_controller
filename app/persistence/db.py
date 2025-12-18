"""
Database connection and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

from app.config import config

logger = logging.getLogger(__name__)

try:
    # The 'check_same_thread' argument is specific to SQLite.
    engine_args = {"check_same_thread": False} if config.DATABASE_URL.startswith("sqlite") else {}
    
    engine = create_engine(
        config.DATABASE_URL,
        connect_args=engine_args
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()

    logger.info("Database engine created successfully.")

except Exception as e:
    logger.critical(f"Failed to connect to the database: {e}")
    # Exit or handle the critical error appropriately
    engine = None
    SessionLocal = None
    Base = None

def get_db():
    """
    Dependency for FastAPI routes to get a DB session.
    """
    if SessionLocal is None:
        raise Exception("Database is not configured. Cannot create session.")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
