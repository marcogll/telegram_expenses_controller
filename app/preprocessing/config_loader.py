"""
Cargador de configuración para proveedores y palabras clave.
"""
import csv
import os
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# Rutas a los archivos de configuración
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROVIDERS_PATH = os.path.join(BASE_DIR, 'config', 'providers.csv')
KEYWORDS_PATH = os.path.join(BASE_DIR, 'config', 'keywords.csv')

def load_providers() -> List[Dict[str, Any]]:
    """
    Carga la configuración de proveedores desde el archivo CSV.
    """
    providers = []
    if not os.path.exists(PROVIDERS_PATH):
        logger.warning(f"Archivo de proveedores no encontrado en {PROVIDERS_PATH}")
        return providers

    try:
        with open(PROVIDERS_PATH, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Procesar alias en una lista
                if 'aliases' in row and row['aliases']:
                    row['aliases'] = [a.strip().lower() for a in row['aliases'].split(',')]
                else:
                    row['aliases'] = []
                providers.append(row)
        logger.info(f"Se cargaron {len(providers)} proveedores desde {PROVIDERS_PATH}")
    except Exception as e:
        logger.error(f"Error al cargar proveedores: {e}")
    
    return providers

def load_keywords() -> List[Dict[str, Any]]:
    """
    Carga la configuración de palabras clave desde el archivo CSV.
    """
    keywords = []
    if not os.path.exists(KEYWORDS_PATH):
        logger.warning(f"Archivo de palabras clave no encontrado en {KEYWORDS_PATH}")
        return keywords

    try:
        with open(KEYWORDS_PATH, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'keyword' in row:
                    row['keyword'] = row['keyword'].strip().lower()
                keywords.append(row)
        logger.info(f"Se cargaron {len(keywords)} palabras clave desde {KEYWORDS_PATH}")
    except Exception as e:
        logger.error(f"Error al cargar palabras clave: {e}")
    
    return keywords
