"""
Functions for calculating confidence scores.
"""

def calculate_confidence(extracted_data: dict) -> float:
    """
    Calculates a confidence score based on the quality of the extracted data.
    Stub function.
    """
    score = 1.0
    # Lower score if key fields are missing
    if not extracted_data.get("amount"):
        score -= 0.5
    if not extracted_data.get("description"):
        score -= 0.3
    return max(0.0, score)
