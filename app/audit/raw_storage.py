"""
Handles storage of raw, original input files for audit purposes.
"""
import logging
import os
from uuid import uuid4

logger = logging.getLogger(__name__)

# A simple file-based storage. In production, you'd use S3 or a similar service.
RAW_STORAGE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "raw_storage")
os.makedirs(RAW_STORAGE_PATH, exist_ok=True)


def save_raw_input(data: bytes, input_type: str) -> str:
    """
    Saves the original input data to a file.

    Args:
        data: The raw bytes of the input.
        input_type: The type of input (e.g., 'image', 'audio').

    Returns:
        The path to the saved file.
    """
    try:
        file_extension = input_type # e.g., 'jpg', 'mp3'
        file_name = f"{uuid4()}.{file_extension}"
        file_path = os.path.join(RAW_STORAGE_PATH, file_name)

        with open(file_path, "wb") as f:
            f.write(data)
        
        logger.info(f"Saved raw input to {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Failed to save raw input: {e}")
        return ""
