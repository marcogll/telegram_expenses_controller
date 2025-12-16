from fastapi import FastAPI, Request
from src.data_models import RawInput
from src.modules.input_handler import handle_input
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Expense Tracker API is running."}

@app.post("/process-expense")
async def process_expense(raw_input: RawInput):
    """
    Receives raw expense data, processes it using the input handler,
    and returns the normalized text.
    """
    logger.info(f"Received raw input: {raw_input.dict()}")

    # Convert RawInput to a dictionary suitable for handle_input
    input_data = raw_input.dict(by_alias=True)

    # Process the input to get normalized text
    normalized_text = handle_input(input_data)

    logger.info(f"Normalized text: '{normalized_text}'")

    # For now, just return the processed text.
    # In the future, this will trigger the analysis phase.
    return {"status": "processed", "normalized_text": normalized_text}
