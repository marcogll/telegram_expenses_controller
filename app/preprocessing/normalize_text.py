"""
Text normalization functions.
"""

def normalize_text(text: str) -> str:
    """
    Normalizes a string by converting it to lowercase and stripping whitespace.
    """
    if not text:
        return ""
    return text.lower().strip()
