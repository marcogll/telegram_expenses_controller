"""
Lógica de coincidencia para proveedores y palabras clave.
"""
import logging
from typing import Optional, Dict, Any
from app.preprocessing.config_loader import load_providers, load_keywords

logger = logging.getLogger(__name__)

# Caché global para la configuración
_PROVIDERS = None
_KEYWORDS = None

def get_config():
    """
    Devuelve la configuración cargada, utilizando la caché si está disponible.
    """
    global _PROVIDERS, _KEYWORDS
    if _PROVIDERS is None:
        _PROVIDERS = load_providers()
    if _KEYWORDS is None:
        _KEYWORDS = load_keywords()
    return _PROVIDERS, _KEYWORDS

def match_provider(description: str) -> Optional[Dict[str, Any]]:
    """
    Busca un nombre de proveedor o alias en la descripción.
    """
    providers, _ = get_config()
    desc_lower = description.lower()
    
    for p in providers:
        name = p.get('provider_name', '').lower()
        aliases = p.get('aliases', [])
        
        # Verificar nombre
        if name and name in desc_lower:
            return p
        
        # Verificar alias
        for alias in aliases:
            if alias and alias in desc_lower:
                return p
                
    return None

def match_keywords(description: str) -> Optional[Dict[str, Any]]:
    """
    Busca palabras clave en la descripción.
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
    Intenta encontrar metadatos (categoría, subcategoría, etc.) para una descripción.
    Prioridad: Coincidencia de Proveedor > Coincidencia de Palabra Clave.
    """
    # 1. Intentar coincidencia de proveedor
    provider = match_provider(description)
    if provider:
        logger.info(f"Proveedor coincidente: {provider['provider_name']}")
        return {
            "category": provider.get('categoria_principal'),
            "subcategory": provider.get('subcategoria'),
            "expense_type": provider.get('tipo_gasto_default'),
            "match_type": "provider",
            "matched_name": provider['provider_name']
        }
    
    # 2. Intentar coincidencia de palabra clave
    keyword = match_keywords(description)
    if keyword:
        logger.info(f"Palabra clave coincidente: {keyword['keyword']}")
        return {
            "category": keyword.get('categoria_principal'),
            "subcategory": keyword.get('subcategoria'),
            "expense_type": keyword.get('tipo_gasto_default'),
            "match_type": "keyword",
            "matched_name": keyword['keyword']
        }
        
    return {}
