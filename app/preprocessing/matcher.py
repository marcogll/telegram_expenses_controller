"""
Matching logic for providers and keywords.
"""
import logging
from typing import Optional, Dict, Any
from app.preprocessing.config_loader import load_providers, load_keywords

logger = logging.getLogger(__name__)

# Global cache for configuration
_PROVIDERS = None
_KEYWORDS = None

def get_config():
    """
    Returns the loaded configuration, using cache if available.
    """
    global _PROVIDERS, _KEYWORDS
    if _PROVIDERS is None:
        _PROVIDERS = load_providers()
    if _KEYWORDS is None:
        _KEYWORDS = load_keywords()
    return _PROVIDERS, _KEYWORDS

def match_provider(description: str) -> Optional[Dict[str, Any]]:
    """
    Searches for a provider name or alias in the description.
    """
    providers, _ = get_config()
    desc_lower = description.lower()
    
    for p in providers:
        name = p.get('provider_name', '').lower()
        aliases = p.get('aliases', [])
        
        # Check name
        if name and name in desc_lower:
            return p
        
        # Check aliases
        for alias in aliases:
            if alias and alias in desc_lower:
                return p
                
    return None

def match_keywords(description: str) -> Optional[Dict[str, Any]]:
    """
    Searches for keywords in the description.
    """
    _, keywords = get_config()
    desc_lower = description.lower()
    
    for k in keywords:
        keyword = k.get('keyword', '').lower()
        if keyword and keyword in desc_lower:
            return k
            
    return None

def get_metadata_from_match(description: str) -> Dict[str, Any]:
    """
    Attempts to find metadata (category, subcategory, etc.) for a description.
    Priority: Provider Match > Keyword Match.
    """
    # 1. Try Provider Match
    provider = match_provider(description)
    if provider:
        logger.info(f"Matched provider: {provider['provider_name']}")
        return {
            "category": provider.get('categoria_principal'),
            "subcategory": provider.get('subcategoria'),
            "expense_type": provider.get('tipo_gasto_default'),
            "match_type": "provider",
            "matched_name": provider['provider_name']
        }
    
    # 2. Try Keyword Match
    keyword = match_keywords(description)
    if keyword:
        logger.info(f"Matched keyword: {keyword['keyword']}")
        return {
            "category": keyword.get('categoria_principal'),
            "subcategory": keyword.get('subcategoria'),
            "expense_type": keyword.get('tipo_gasto_default'),
            "match_type": "keyword",
            "matched_name": keyword['keyword']
        }
        
    return {}
