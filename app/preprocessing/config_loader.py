"""
Configuration loader for providers and keywords.
"""
import csv
import os
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# Paths to configuration files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROVIDERS_PATH = os.path.join(BASE_DIR, 'config', 'providers.csv')
KEYWORDS_PATH = os.path.join(BASE_DIR, 'config', 'keywords.csv')

def load_providers() -> List[Dict[str, Any]]:
    """
    Loads the providers configuration from CSV.
    """
    providers = []
    if not os.path.exists(PROVIDERS_PATH):
        logger.warning(f"Providers file not found at {PROVIDERS_PATH}")
        return providers

    try:
        with open(PROVIDERS_PATH, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Process aliases into a list
                if 'aliases' in row and row['aliases']:
                    row['aliases'] = [a.strip().lower() for a in row['aliases'].split(',')]
                else:
                    row['aliases'] = []
                providers.append(row)
        logger.info(f"Loaded {len(providers)} providers from {PROVIDERS_PATH}")
    except Exception as e:
        logger.error(f"Error loading providers: {e}")
    
    return providers

def load_keywords() -> List[Dict[str, Any]]:
    """
    Loads the keywords configuration from CSV.
    """
    keywords = []
    if not os.path.exists(KEYWORDS_PATH):
        logger.warning(f"Keywords file not found at {KEYWORDS_PATH}")
        return keywords

    try:
        with open(KEYWORDS_PATH, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'keyword' in row:
                    row['keyword'] = row['keyword'].strip().lower()
                keywords.append(row)
        logger.info(f"Loaded {len(keywords)} keywords from {KEYWORDS_PATH}")
    except Exception as e:
        logger.error(f"Error loading keywords: {e}")
    
    return keywords
