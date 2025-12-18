"""
Handles processing of raw text inputs.
"""
import logging

logger = logging.getLogger(__name__)

def process_text_input(text: str) -> str:
    """
    Takes raw text, normalizes it, and prepares it for AI extraction.

    In the future, this could include more complex preprocessing like
    language detection or PII removal.

    Args:
        text: The raw input text.

    Returns:
        The processed text.
    """
    logger.info("Processing text input.")
    # For now, normalization is simple. It will be moved to the preprocessing module.
    normalized_text = text.lower().strip()
    return normalized_text
