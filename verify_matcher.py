"""
Verification script for matching logic.
"""
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.preprocessing.matcher import get_metadata_from_match

def test_match(description: str):
    print(f"\nTesting: '{description}'")
    metadata = get_metadata_from_match(description)
    if metadata:
        print(f"  Match Found!")
        print(f"  Type: {metadata.get('match_type')}")
        print(f"  Name: {metadata.get('matched_name')}")
        print(f"  Category: {metadata.get('category')}")
        print(f"  Subcategory: {metadata.get('subcategory')}")
        print(f"  Expense Type: {metadata.get('expense_type')}")
    else:
        print("  No match found.")

if __name__ == "__main__":
    # Test providers
    test_match("Lunch at Amazon")
    test_match("Uber Eats dinner")
    test_match("Office Depot supplies")
    
    # Test keywords
    test_match("New monitor for work")
    test_match("Croquetas for the dog")
    
    # Test no match
    test_match("Random expense")
