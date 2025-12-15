# TASKS.md

Este documento define un **plan de ejecución secuencial**, con **menos fases pero más coherentes**, pensadas para ejecutarse **una tras otra sin ambigüedad**, ideal para un agente de IA desarrollador o un equipo técnico.

Principio rector:

> *Cada fase deja el sistema en un estado funcional, testeable y estable.*

---

## Fase 1 – Base del Sistema (Infraestructura + Entrada)

**Objetivo:** recibir mensajes de Telegram y dejarlos listos para procesar.

### 1.1 Bootstrap del Proyecto

* Crear estructura de carpetas según README.
* Configurar entorno virtual.
* Instalar dependencias.
* FastAPI levantando correctamente.

Resultado: API viva sin lógica de negocio.

---

### 1.2 Variables de Entorno

Definir `.env` con:

* TELEGRAM_BOT_TOKEN
* OPENAI_API_KEY
* GOOGLE_APPLICATION_CREDENTIALS
* SPREADSHEET_ID
* ENV (dev / prod)

El sistema **no debe arrancar** si falta alguna.

---

### 1.3 Webhook de Telegram

* Endpoint `/telegram/webhook`.
* Validar origen del mensaje.
* Log completo del payload en modo dev.

Resultado: mensajes entran y se registran.

---

### 1.4 Input Handler

Implementar `input_handler.py`:

* Texto.
* Voz (solo stub inicialmente).
* Imagen (solo stub inicialmente).
* PDF (solo stub).

Todo debe normalizarse a texto crudo.

Resultado: cualquier input termina como texto limpio.

---

## Fase 2 – Modelo de Datos y Estados

**Objetivo:** tener claridad absoluta sobre qué es un gasto y en qué estado vive.

### 2.1 Modelos Pydantic

Crear modelos:

* RawInput
* ExtractedExpense
* ProvisionalExpense
* FinalExpense

Cada modelo debe validar su propio dominio.

---

### 2.2 Estados del Gasto

Definir estados explícitos:

* RECEIVED
* ANALYZED
* AWAITING_CONFIRMATION
* CONFIRMED
* CORRECTED
* STORED

No se permiten saltos implícitos.

Resultado: máquina de estados clara.

---

## Fase 3 – Configuración como Lógica

**Objetivo:** mover la inteligencia determinística fuera del código.

### 3.1 Loader de Configuración

Implementar `config_loader.py`:

* Cargar CSV y JSON.
* Normalizar texto.
* Cachear en memoria.
* Validar esquema mínimo.

Fallar rápido si algo está mal configurado.

---

### 3.2 Matching de Proveedores

* Matching por nombre y aliases.
* Coincidencia parcial, case-insensitive.
* Retornar score de match.

Regla dura: si hay match fuerte, **no usar IA**.

---

### 3.3 Matching de Keywords

* Buscar keywords en descripciones.
* Permitir múltiples matches.
* Resolver conflictos por prioridad.

Resultado: clasificación determinística siempre que sea posible.

---

## Fase 4 – The Analyst (Procesamiento Inteligente)

**Objetivo:** convertir texto crudo en un gasto provisional estructurado.

### 4.1 Extracción Multimodal (Completa)

* Voz → transcripción IA.
* Imagen → OCR IA.
* PDF → extracción semiestructurada.

Unificar todo en texto limpio.

---

### 4.2 Clasificación en Cascada

Pipeline obligatorio:

1. Proveedores
2. Keywords
3. Inferencia IA (último recurso)

Registrar siempre **por qué camino** se tomó la decisión.

---

### 4.3 Validación Fiscal Básica

* Detectar CFDI.
* Extraer RFC receptor.
* Comparar con `user_config.json`.
* Anotar observaciones, no bloquear.

---

### 4.4 Score de Confianza

* Regla directa → alta.
* Keywords → media.
* IA pura → baja.

Persistir el score.

Resultado: gasto provisional listo para revisión humana.

---

## Fase 5 – Interacción y Auditoría

**Objetivo:** asegurar control humano y trazabilidad.

### 5.1 Mensaje de Confirmación

Enviar al usuario:

* Proveedor
* Monto
* Categoría
* Tipo (personal / negocio)
* Observaciones
* Score de confianza

Formato corto, claro y editable.

---

### 5.2 Parsing de Correcciones

Aceptar lenguaje natural:

* "el monto es 180"
* "es personal"
* "la fecha fue ayer"

No asumir intención: solo cambios explícitos.

---

### 5.3 The Auditor

* Comparar estado previo vs nuevo.
* Aplicar solo cambios solicitados.
* Registrar auditoría:

```
AUDITORÍA: campo X cambió de A a B (timestamp)
```

Nada se sobreescribe silenciosamente.

---

## Fase 6 – Persistencia y Cierre

**Objetivo:** guardar datos finales de forma segura y limpia.

### 6.1 Google Sheets

* Hojas separadas: personal / negocio.
* Append-only.
* Manejo de errores de red.

---

### 6.2 Limpieza de Estados Temporales

* Eliminar colas provisionales.
* Asegurar idempotencia.

Resultado: gasto almacenado y ciclo cerrado.

---

## Fase 7 – Hardening y Preparación a Futuro

### 7.1 Logs y Errores

* Logs estructurados.
* DEBUG solo en dev.
* Mensajes claros al usuario.

Nunca perder un gasto silenciosamente.

---

### 7.2 Preparación para Escalar

* Aislar config por `user_id`.
* Preparar soporte multiusuario.
* Dejar hooks para reportes futuros.

---

## Regla Final para el Agente

* Ejecutar fases en orden.
* No adelantar optimizaciones.
* Si una decisión no es obvia, documentarla.

El sistema debe sentirse **confiable, explicable y humano**, antes que impresionante.
