# Telegram Expenses Bot

A bot to track expenses via Telegram messages, using AI for data extraction.

## Project Structure

This project follows a modular, service-oriented architecture.

- **/app**: Main application source code.
  - **/ai**: AI models, prompts, and logic.
  - **/audit**: Logging and raw data storage for traceability.
  - **/ingestion**: Handlers for different input types (text, image, audio).
  - **/integrations**: Connections to external services.
  - **/modules**: Telegram command handlers.
  - **/persistence**: Database models and data access layer.
  - **/preprocessing**: Data cleaning and normalization.
  - **/schema**: Pydantic data models.
  - **main.py**: FastAPI application entry point.
  - **router.py**: Main workflow orchestrator.
  - **config.py**: Configuration loader.
- **/raw_storage**: (Created automatically) Stores original uploaded files.
- **Dockerfile**: Defines the container for the application.
- **docker-compose.yml**: Orchestrates the application and database services.
- **requirements.txt**: Python dependencies.
- **.env.example**: Example environment variables.

## How to Run

1.  **Set up environment variables:**
    ```bash
    cp .env.example .env
    ```
    Fill in the values in the `.env` file (Telegram token, OpenAI key, etc.).

2.  **Build and run with Docker Compose:**
    ```bash
    docker-compose up --build
    ```

3.  **Access the API:**
    The API will be available at `http://localhost:8000`. The interactive documentation can be found at `http://localhost:8000/docs`.

## Running the Telegram Bot

This setup provides the backend API. To connect it to Telegram, you have two main options:

1.  **Webhook**: Set a webhook with Telegram to point to your deployed API's `/webhook/telegram` endpoint. This is the recommended production approach.
2.  **Polling**: Modify the application to use polling instead of a webhook. This involves creating a separate script or modifying `main.py` to start the `python-telegram-bot` `Application` and add the handlers from the `modules` directory. This is simpler for local development.

### Example: Adding Polling for Development

You could add this to a new file, `run_bot.py`, in the root directory:

```python
import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from app.config import config
from app.modules import start, upload, status, search, admin

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(config.TELEGRAM_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start.start))
    application.add_handler(CommandHandler("status", status.status))
    application.add_handler(CommandHandler("search", search.search))
    application.add_handler(CommandHandler("admin", admin.admin_command))

    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, upload.handle_message))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
```
You would then run `python run_bot.py` locally.
