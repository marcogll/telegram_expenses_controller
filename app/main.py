"""
Application entry point.

Initializes the FastAPI application, sets up logging, database, 
and defines the main API endpoints.
"""
import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# It's crucial to set up the config before other imports
from app.config import config

# Now, set up logging based on the config
logging.basicConfig(level=config.LOG_LEVEL.upper())
logger = logging.getLogger(__name__)

# Import other components
from app.schema.base import RawInput
from app.router import process_expense_input
from app.persistence import repositories, db

# Create database tables on startup
# This is simple, but for production, you'd use migrations (e.g., Alembic)
repositories.create_tables()

# Initialize the FastAPI app
app = FastAPI(
    title="Telegram Expenses Bot API",
    description="Processes and manages expense data from various sources.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup complete.")
    logger.info(f"Log level is set to: {config.LOG_LEVEL.upper()}")

@app.get("/", tags=["Status"])
async def root():
    """Health check endpoint."""
    return {"message": "Telegram Expenses Bot API is running."}

@app.post("/webhook/telegram", tags=["Webhooks"])
async def process_telegram_update(request: dict):
    """
    This endpoint would receive updates directly from a Telegram webhook.
    It needs to be implemented to parse the Telegram Update object and
    convert it into our internal RawInput model.
    """
    logger.info(f"Received Telegram update: {request}")
    # TODO: Implement a parser for the Telegram Update object.
    # For now, this is a placeholder.
    return {"status": "received", "message": "Telegram webhook handler not fully implemented."}

@app.post("/process-expense", tags=["Processing"])
async def process_expense(raw_input: RawInput, db_session: Session = Depends(db.get_db)):
    """
    Receives raw expense data, processes it through the full pipeline,
    and returns the result.
    """
    logger.info(f"Received raw input for processing: {raw_input.dict()}")
    
    try:
        result = process_expense_input(db=db_session, raw_input=raw_input)
        
        if result:
            return {"status": "success", "expense_id": result.id}
        else:
            # This could happen if confidence is low or an error occurred
            raise HTTPException(
                status_code=400, 
                detail="Failed to process expense. It may require manual review or had invalid data."
            )

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.critical(f"An unexpected error occurred in the processing pipeline: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

# To run this app:
# uvicorn app.main:app --reload
