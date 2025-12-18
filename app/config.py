"""
Cargador de configuración.

Carga las variables de entorno desde un archivo .env y las pone a disposición como un objeto Config.
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env en la raíz del proyecto
# Nota: La ruta es relativa a la ubicación del archivo en el directorio final `app`
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

class Config:
    """
    Contiene la configuración de la aplicación.
    """
    # Token del Bot de Telegram
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    # OpenAI API Key
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # ID del Supergrupo para el bot
    SUPERGROUP_ID = os.getenv("SUPERGROUP_ID")
    
    # URL de la Base de Datos (ej., "sqlite:///expenses.db")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///../database.db")

    # Nivel de registro
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


# Crear una única instancia de la configuración
config = Config()
