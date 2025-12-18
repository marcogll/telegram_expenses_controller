"""
Configuration loader.

Loads environment variables from a .env file and makes them available as a Config object.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file in the project root
# Note: The path is relative to the file's location in the final `app` directory
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

class Config:
    """
    Holds the application's configuration.
    """
    # Telegram Bot Token
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    # OpenAI API Key
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Supergroup ID for the bot
    SUPERGROUP_ID = os.getenv("SUPERGROUP_ID")
    
    # Database URL (e.g., "sqlite:///expenses.db")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///../database.db")

    # Log level
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


# Create a single instance of the configuration
config = Config()
