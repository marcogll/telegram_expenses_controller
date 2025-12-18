# TASKS.md - To-Do List

Este documento define el plan de ejecución del proyecto.

Principio rector:

> *Cada fase deja el sistema en un estado funcional, testeable y estable.*

---

## Fase 1 – Base del Sistema (Infraestructura + Entrada)

**Objetivo:** Recibir datos de gastos y dejarlos listos para procesar.

- [x] **1.1 Bootstrap del Proyecto**
  - [x] Crear estructura de carpetas modular en `/app`.
  - [x] Configurar entorno virtual y `requirements.txt`.
  - [x] Dockerización con `docker-compose.yml`.
- [x] **1.2 Configuración y Base de Datos**
  - [x] Definir `.env.example` con variables para OpenAI, Telegram y MySQL.
  - [x] Configurar servicio de **MySQL 8.0** en Docker.
  - [x] Implementar `app/config.py` para carga de variables.
- [x] **1.3 Entrada de Datos (Multimodal)**
  - [x] Endpoint `/process-expense` para integración externa.
  - [x] Endpoint `/webhook/telegram` para recepción directa.
  - [x] Implementar módulos de ingestión inicial (`text.py`, `image.py`, `audio.py`).
- [x] **1.4 Orquestación Inicial**
  - [x] Implementar `router.py` para coordinar el pipeline.

---

## Fase 2 – Modelo de Datos y Estados

**Objetivo:** Tener claridad absoluta sobre qué es un gasto y en qué estado vive.

- [x] **2.1 Modelos Pydantic**
  - [x] Crear modelos en `app/schema/base.py`: `RawInput`, `ExtractedExpense`, `ProvisionalExpense`, `FinalExpense`.
- [x] **2.2 Estados del Gasto**
  - [x] Definir `ExpenseStatus` (RECEIVED, ANALYZED, CONFIRMED, etc.).
- [x] **2.3 Persistencia SQL**
  - [x] Implementar modelos SQLAlchemy y repositorios en `app/persistence`.

---

## Fase 3 – Configuración y Lógica de Negocio

**Objetivo:** Mover la inteligencia determinística fuera del código.

- [/] **3.1 Loader de Configuración**
  - [ ] Implementar carga dinámica de `config/providers.csv` y `keywords.csv`.
- [ ] **3.2 Matching de Proveedores**
  - [ ] Implementar matching por nombre y aliases.
- [ ] **3.3 Clasificación por Keywords**
  - [ ] Implementar búsqueda de keywords en descripciones para categorización automática.

---

## Fase 4 – The Analyst (Procesamiento Inteligente)

**Objetivo:** Convertir texto crudo en un gasto provisional estructurado mediante IA.

- [/] **4.1 Extracción Multimodal (Completa)**
  - [x] Texto -> Extracción con GPT.
  - [ ] Voz -> Transcripción (Whisper/OpenAI).
  - [ ] Imagen -> OCR + Extracción.
- [ ] **4.2 Validación y Score de Confianza**
  - [ ] Implementar `app/ai/confidence.py` para evaluar la calidad de la extracción.
- [ ] **4.3 Detección de Duplicados**
  - [ ] Evitar registrar el mismo gasto dos veces.

---

## Fase 5 – Interacción con el Usuario

**Objetivo:** Asegurar control humano y correcciones.

- [ ] **5.1 Flujo de Confirmación en Telegram**
  - [ ] Enviar botones de "Confirmar" / "Editar" tras procesar un gasto.
- [ ] **5.2 Parsing de Correcciones**
  - [ ] Capacidad de corregir campos específicos mediante mensajes de texto.
- [ ] **5.3 Comandos de Consulta**
  - [ ] Implementar `/status` y `/search` funcionales.

---

## Fase 6 – Exportación y Cierre

**Objetivo:** Facilitar el uso de los datos fuera del sistema.

- [ ] **6.1 Exportación a CSV/Excel**
  - [x] Implementar exportador básico a CSV.
- [ ] **6.2 Integración con Google Sheets (Opcional)**
  - [ ] Sincronización automática de gastos confirmados.

---

## Fase 7 – Hardening

**Objetivo:** Estabilidad y producción.

- [ ] **7.1 Manejo de Errores Robusto**
  - [ ] Reintentos en llamadas a API de IA.
  - [ ] Alertas de sistema.
- [ ] **7.2 Logs de Auditoría**
  - [ ] Registro detallado de quién cambió qué y cuándo.
