from fastapi import FastAPI, Request
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Expense Tracker API is running."}

@app.post("/process-expense")
async def process_expense(request: Request):
    """
    Receives expense data from n8n, logs it, and returns a confirmation.
    """
    payload = await request.json()
    logger.info(f"Received expense data: {payload}")
    return {"status": "received", "data": payload}
