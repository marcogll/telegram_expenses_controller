"""
Logging configuration and handlers.
"""
import logging
import sys
from app.config import config

def setup_logging():
    """
    Sets up a centralized logging configuration for the application.
    """
    log_level = config.LOG_LEVEL.upper()
    
    # Remove any existing handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout
    )
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured with level {log_level}")

