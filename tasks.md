# TASKS.md - To-Do List

Este documento define el plan de ejecución del proyecto.

Principio rector:

> *Cada fase deja el sistema en un estado funcional, testeable y estable.*

---

## Fase 1 – Base del Sistema (Infraestructura + Entrada)

**Objetivo:** Recibir datos de gastos y dejarlos listos para procesar.

- [x] **1.1 Bootstrap del Proyecto**
  - [x] Crear estructura de carpetas según README.
  - [x] Configurar entorno virtual.
  - [x] Instalar dependencias.
  - [x] FastAPI levantando correctamente.
- [x] **1.2 Variables de Entorno**
  - [x] Definir `.env.example` con las variables necesarias.
- [x] **1.3 Webhook y Entrada de Datos**
  - **NOTA:** Se ha modificado el enfoque. En lugar de un webhook directo de Telegram, se utiliza **n8n** para manejar la recepción de datos. La aplicación expone un endpoint genérico `/process-expense` para este propósito.
  - [x] Endpoint `/process-expense` implementado en FastAPI.
  - [x] El endpoint recibe y loguea el payload.
- [ ] **1.4 Input Handler**
  - [ ] Implementar `input_handler.py`.
  - [ ] Normalizar texto.
  - [ ] Implementar stubs para voz, imagen y PDF.

---

## Fase 2 – Modelo de Datos y Estados

**Objetivo:** Tener claridad absoluta sobre qué es un gasto y en qué estado vive.

- [ ] **2.1 Modelos Pydantic**
  - [ ] Crear modelos: `RawInput`, `ExtractedExpense`, `ProvisionalExpense`, `FinalExpense`.
- [ ] **2.2 Estados del Gasto**
  - [ ] Definir estados explícitos: `RECEIVED`, `ANALYZED`, `AWAITING_CONFIRMATION`, `CONFIRMED`, `CORRECTED`, `STORED`.

---

## Fase 3 – Configuración como Lógica

**Objetivo:** Mover la inteligencia determinística fuera del código.

- [ ] **3.1 Loader de Configuración**
  - [ ] Implementar `config_loader.py`.
- [ ] **3.2 Matching de Proveedores**
  - [ ] Implementar matching por nombre y aliases.
- [ ] **3.3 Matching de Keywords**
  - [ ] Implementar búsqueda de keywords en descripciones.

---

## Fase 4 – The Analyst (Procesamiento Inteligente)

**Objetivo:** Convertir texto crudo en un gasto provisional estructurado.

- [ ] **4.1 Extracción Multimodal (Completa)**
  - [ ] Voz → transcripción IA.
  - [ ] Imagen → OCR IA.
  - [ ] PDF → extracción semiestructurada.
- [ ] **4.2 Clasificación en Cascada**
  - [ ] Implementar pipeline: Proveedores → Keywords → IA.
- [ ] **4.3 Validación Fiscal Básica**
  - [ ] Implementar detección de CFDI y validación de RFC.
- [ ] **4.4 Score de Confianza**
  - [ ] Calcular y persistir el score de confianza del análisis.

---

## Fase 5 – Interacción y Auditoría

**Objetivo:** Asegurar control humano y trazabilidad.

- [ ] **5.1 Mensaje de Confirmación**
  - [ ] Enviar resumen del gasto procesado al usuario.
- [ ] **5.2 Parsing de Correcciones**
  - [ ] Implementar la capacidad de aceptar correcciones en lenguaje natural.
- [ ] **5.3 The Auditor**
  - [ ] Implementar el agente "Auditor" para registrar todos los cambios.

---

## Fase 6 – Persistencia y Cierre

**Objetivo:** Guardar datos finales de forma segura y limpia.

- [ ] **6.1 Google Sheets**
  - [ ] Implementar la escritura de datos en Google Sheets.
- [ ] **6.2 Limpieza de Estados Temporales**
  - [ ] Asegurar la limpieza de datos temporales tras el procesamiento.

---

## Fase 7 – Hardening y Preparación a Futuro

**Objetivo:** Fortalecer el sistema y prepararlo para escalar.

- [ ] **7.1 Logs y Errores**
  - [ ] Implementar logs estructurados y un manejo de errores robusto.
- [ ] **7.2 Preparación para Escalar**
  - [ ] Diseñar el sistema para soportar múltiples usuarios en el futuro.
