# Bot de Gastos de Telegram

Un bot modular impulsado por IA para rastrear y gestionar gastos a través de Telegram. Utiliza LLMs para extraer datos estructurados de texto, imágenes y audio, y los persiste para facilitar la generación de informes.

## Características Clave

- 🤖 **Extracción por IA**: Analiza automáticamente el monto, la moneda, la descripción y la fecha a partir del lenguaje natural.
- 🖼️ **Multimodal**: Soporta texto, imágenes (recibos) y audio (notas de voz) - *en progreso*.
- 📊 **Almacenamiento Estructurado**: Guarda los datos en una base de datos con soporte para exportar a CSV/Google Sheets.
- 🛡️ **Pista de Auditoría**: Realiza un seguimiento de las entradas sin procesar y las puntuaciones de confianza de la IA para mayor fiabilidad.
- 🐳 **Dockerizado**: Despliegue sencillo utilizando Docker y Docker Compose.

## Estructura del Proyecto

El proyecto ha transicionado a una arquitectura más robusta y orientada a servicios ubicada en el directorio `/app`.

- **/app**: Lógica central de la aplicación.
  - **/ai**: Integración con LLM, prompts y lógica de extracción.
  - **/audit**: Registro y almacenamiento de datos sin procesar para trazabilidad.
  - **/ingestion**: Manejadores para diferentes tipos de entrada (texto, imagen, audio, documento).
  - **/integrations**: Servicios externos (ej. exportadores, clientes de webhook).
  - **/modules**: Manejadores de comandos del bot de Telegram (`/start`, `/status`, etc.).
  - **/persistence**: Modelos de base de datos y repositorios (SQLAlchemy).
  - **/preprocessing**: Limpieza de datos, validación y detección de idioma.
  - **/schema**: Modelos Pydantic para validación de datos y documentación de la API.
  - **main.py**: Punto de entrada de FastAPI y manejadores de webhooks.
  - **router.py**: Orquesta el pipeline de procesamiento.
- **/config**: Archivos de configuración estática (palabras clave, proveedores).
- **/src**: Implementación heredada/inicial (Fases 1 y 2).
- **tasks.md**: Hoja de ruta detallada del proyecto y seguidor de progreso.

## Cómo Funciona (Flujo de Trabajo)

1.  **Entrada**: El usuario envía un mensaje al bot de Telegram (texto, imagen o voz).
2.  **Ingestión**: El bot recibe la actualización y la pasa a la capa `/app/ingestion` para extraer el texto sin procesar.
3.  **Enrutamiento**: `router.py` toma el texto sin procesar y coordina los siguientes pasos.
4.  **Extracción**: `/app/ai/extractor.py` utiliza los modelos GPT de OpenAI para analizar el texto en un `ExtractedExpense` estructurado.
5.  **Auditoría y Clasificación**: `/app/ai/classifier.py` asigna categorías y una puntuación de confianza.
6.  **Persistencia**: Si la confianza es alta, el gasto se guarda automáticamente a través de `/app/persistence/repositories.py`. Si es baja, espera confirmación manual.

## Estado del Proyecto

Fase Actual: **Fase 3/4 - Inteligencia y Procesamiento**

- [x] **Fase 1: Infraestructura**: FastAPI, Docker y manejo básico de entradas.
- [x] **Fase 2: Modelos de Datos**: Estados de gastos explícitos y esquemas Pydantic.
- [x] **Fase 3: Lógica**: Cargadores de configuración y coincidencia de proveedores (Completado).
- [/] **Fase 4: Analista de IA**: Extracción multimodal y puntuación de confianza (En Progreso).

## Configuración y Desarrollo

### 1. Variables de Entorno
Copia `.env.example` a `.env` y completa tus credenciales:
```bash
TELEGRAM_TOKEN=tu_token_de_bot
OPENAI_API_KEY=tu_clave_de_openai
DATABASE_URL=mysql+pymysql://usuario:contraseña@db:3306/expenses

# Específico de MySQL (para Docker)
MYSQL_ROOT_PASSWORD=contraseña_root
MYSQL_DATABASE=expenses
MYSQL_USER=usuario
MYSQL_PASSWORD=contraseña
```

### 2. Ejecutar con Docker
```bash
docker-compose up --build
```

### 3. Desarrollo Local (FastAPI)
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 4. Ejecutar el Bot (Polling)
Para pruebas locales sin webhooks, puedes ejecutar un script de polling que utilice los manejadores en `app/modules`.

---
*Mantenido por Marco Gallegos*
