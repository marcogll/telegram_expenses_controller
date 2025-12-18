# Telegram Expenses Bot

A modular, AI-powered bot to track and manage expenses via Telegram. It uses LLMs to extract structured data from text, images, and audio, and persists them for easy reporting.

## Key Features

- 🤖 **AI Extraction**: Automatically parses amount, currency, description, and date from natural language.
- 🖼️ **Multimodal**: Supports text, images (receipts), and audio (voice notes) - *in progress*.
- 📊 **Structured Storage**: Saves data to a database with support for exporting to CSV/Google Sheets.
- 🛡️ **Audit Trail**: Keeps track of raw inputs and AI confidence scores for reliability.
- 🐳 **Dockerized**: Easy deployment using Docker and Docker Compose.

## Project Structure

The project has transitioned to a more robust, service-oriented architecture located in the `/app` directory.

- **/app**: Core application logic.
  - **/ai**: LLM integration, prompts, and extraction logic.
  - **/audit**: Logging and raw data storage for traceability.
  - **/ingestion**: Handlers for different input types (text, image, audio, document).
  - **/integrations**: External services (e.g., exporters, webhook clients).
  - **/modules**: Telegram bot command handlers (`/start`, `/status`, etc.).
  - **/persistence**: Database models and repositories (SQLAlchemy).
  - **/preprocessing**: Data cleaning, validation, and language detection.
  - **/schema**: Pydantic models for data validation and API documentation.
  - **main.py**: FastAPI entry point and webhook handlers.
  - **router.py**: Orchestrates the processing pipeline.
- **/config**: Static configuration files (keywords, providers).
- **/src**: Legacy/Initial implementation (Phase 1 & 2).
- **tasks.md**: Detailed project roadmap and progress tracker.

## How It Works (Workflow)

1.  **Input**: The user sends a message to the Telegram bot (text, image, or voice).
2.  **Ingestion**: The bot receives the update and passes it to the `/app/ingestion` layer to extract raw text.
3.  **Routing**: `router.py` takes the raw text and coordinates the next steps.
4.  **Extraction**: The `/app/ai/extractor.py` uses OpenAI's GPT models to parse the text into a structured `ExtractedExpense`.
5.  **Audit & Classify**: The `/app/ai/classifier.py` assigns categories and a confidence score.
6.  **Persistence**: If confidence is high, the expense is automatically saved via `/app/persistence/repositories.py`. If low, it awaits manual confirmation.

## Project Status

Current Phase: **Phase 3/4 - Intelligence & Processing**

- [x] **Phase 1: Infrastructure**: FastAPI, Docker, and basic input handling.
- [x] **Phase 2: Data Models**: Explicit expense states and Pydantic schemas.
- [/] **Phase 3: Logic**: Configuration loaders and provider matching (In Progress).
- [/] **Phase 4: AI Analyst**: Multimodal extraction and confidence scoring (In Progress).

## Setup & Development

### 1. Environment Variables
Copy `.env.example` to `.env` and fill in your credentials:
```bash
TELEGRAM_TOKEN=your_bot_token
OPENAI_API_KEY=your_openai_key
DATABASE_URL=mysql+pymysql://user:password@db:3306/expenses

# MySQL specific (for Docker)
MYSQL_ROOT_PASSWORD=root_password
MYSQL_DATABASE=expenses
MYSQL_USER=user
MYSQL_PASSWORD=password
```

### 2. Run with Docker
```bash
docker-compose up --build
```

### 3. Local Development (FastAPI)
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 4. Running the Bot (Polling)
For local testing without webhooks, you can run a polling script that uses the handlers in `app/modules`.

---
*Maintained by Marco Gallegos*
