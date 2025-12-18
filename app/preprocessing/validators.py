"""
Data validation functions.
"""

def is_valid_expense(data: dict) -> bool:
    """
    Validates if the extracted data for an expense is plausible.
    Stub function.
    """
    # Example validation: amount must be positive
    if "amount" in data and data["amount"] <= 0:
        return False
    return True
