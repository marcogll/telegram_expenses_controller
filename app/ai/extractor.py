"""
AI-powered data extraction from raw text.
"""
import openai
import json
import logging
from typing import Dict, Any

from app.config import config
from app.ai.prompts import EXTRACTOR_PROMPT
from app.schema.base import ExtractedExpense

# Configure the OpenAI client
openai.api_key = config.OPENAI_API_KEY

logger = logging.getLogger(__name__)

def extract_expense_data(text: str) -> ExtractedExpense:
    """
    Uses an AI model to extract structured expense data from a raw text string.

    Args:
        text: The raw text from user input, OCR, or transcription.

    Returns:
        An ExtractedExpense object with the data found by the AI.
    """
    logger.info(f"Starting AI extraction for text: '{text[:100]}...'")
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or another suitable model
            messages=[
                {"role": "system", "content": EXTRACTOR_PROMPT},
                {"role": "user", "content": text}
            ],
            temperature=0.0,
            response_format={"type": "json_object"}
        )

        # The response from OpenAI should be a JSON string in the message content
        json_response = response.choices[0].message['content']
        extracted_data = json.loads(json_response)
        
        logger.info(f"AI extraction successful. Raw JSON: {extracted_data}")

        # Add the original text to the model for audit purposes
        extracted_data['raw_text'] = text

        return ExtractedExpense(**extracted_data)

    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON from AI response: {e}")
        # Return a model with only the raw text for manual review
        return ExtractedExpense(raw_text=text)
    except Exception as e:
        logger.error(f"An unexpected error occurred during AI extraction: {e}")
        # Return a model with only the raw text
        return ExtractedExpense(raw_text=text)

