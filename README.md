# Sistema de Gestión de Gastos Personalizable con Python y Telegram

Este proyecto implementa un **sistema de gestión de gastos modular, auditable y altamente personalizable**, construido en Python y operado a través de un bot de Telegram. El objetivo no es solo registrar gastos, sino **entenderlos, clasificarlos y validarlos** con un equilibrio deliberado entre reglas explícitas (configuración humana) e inferencia asistida por IA.

El sistema permite registrar gastos usando **texto, notas de voz, imágenes (tickets) y documentos PDF (facturas)**. La IA se utiliza únicamente para interpretar datos no estructurados (OCR, transcripción, extracción semántica), mientras que **la lógica de negocio vive fuera del código**, en archivos CSV y JSON que el usuario controla.

La filosofía central es simple pero potente:

> *La IA sugiere, las reglas deciden, el usuario confirma.*

---

## Objetivos del Sistema

* Eliminar fricción en el registro diario de gastos.
* Evitar dependencias rígidas de lógica hardcodeada.
* Mantener trazabilidad y control fiscal (especialmente en México).
* Permitir adaptación rápida a cualquier negocio o uso personal.
* Diseñar una base sólida para automatización contable posterior.

---

## Core Features

### Personalización Total (Config-Driven)

La clasificación de gastos **no está en el código**. Proveedores, categorías, subcategorías, palabras clave y reglas fiscales se gestionan mediante archivos CSV y JSON editables.

Esto permite:

* Ajustes sin despliegues.
* Uso por personas no técnicas.
* Reglas distintas por usuario o empresa.

### Entrada Multimodal

El bot acepta gastos mediante:

* Texto libre.
* Notas de voz (transcripción automática).
* Fotos de tickets (OCR).
* Facturas PDF (extracción estructurada).

Todo converge en un modelo de gasto unificado.

### Procesamiento Inteligente con IA (Controlada)

La IA se utiliza para:

* Leer y transcribir información no estructurada.
* Extraer proveedor, fecha, monto y conceptos.
* Inferir contexto **solo cuando las reglas no aplican**.

La decisión final prioriza reglas explícitas antes que inferencia probabilística.

### Validación Fiscal (CFDI)

Si el sistema detecta una factura:

* Verifica que el RFC receptor coincida con el configurado.
* Considera el régimen fiscal del usuario.
* Marca inconsistencias como observaciones (no bloquea, pero alerta).

### Flujo de Confirmación y Auditoría

Ningún gasto entra al registro final sin pasar por confirmación.

El sistema:

* Presenta un resumen al usuario.
* Permite correcciones naturales por chat.
* Registra **qué cambió, quién lo cambió y por qué**.

Esto garantiza integridad y auditabilidad.

---

## Arquitectura de Datos: El Cerebro Configurable

El núcleo del sistema es la carpeta `config/`. Aquí se define **cómo piensa el bot**.

### 1. Configuración del Usuario

**Archivo:** `config/user_config.json`

Define la identidad fiscal y preferencias base del usuario.

```json
{
  "user_name": "Marco Gallegos",
  "rfc": "GAMM910513CW6",
  "regimen_fiscal_default": "612 - Persona Física con Actividad Empresarial y Profesional",
  "moneda_default": "MXN",
  "pais": "MX",
  "timezone": "America/Mexico_City"
}
```

Este archivo es crítico para validación CFDI y normalización de datos.

---

### 2. Base de Proveedores

**Archivo:** `config/providers.csv`

Es la regla de clasificación **más fuerte del sistema**.

```csv
provider_name,aliases,categoria_principal,subcategoria,tipo_gasto_default
Amazon,"amazon,amzn,amazon mx",Por Determinar,Compras en Línea,
Office Depot,"officedepot,office",Administración,Suministros de oficina,negocio
Uber Eats,"ubereats,uber",Personal,Comida a domicilio,personal
GoDaddy,"godaddy",Tecnología,Dominios y Hosting,negocio
Cinepolis,"cinepolis",Personal,Entretenimiento,personal
```

Si un proveedor coincide aquí, **no se consulta a la IA**.

---

### 3. Palabras Clave de Artículos

**Archivo:** `config/keywords.csv`

Se usa principalmente para proveedores genéricos.

```csv
keyword,categoria_principal,subcategoria,tipo_gasto_default
monitor,Tecnología,Equipo de Cómputo,negocio
croquetas,Personal,Mascotas,personal
hosting,Tecnología,Dominios y Hosting,negocio
libro,Educación,Libros y Material,negocio
```

Permite clasificación por contenido del ticket, no solo por tienda.

---

## Agentes de IA: Roles Claros, Responsabilidades Limitadas

El sistema usa dos agentes conceptuales, cada uno con límites estrictos.

### 1. The Analyst (Procesamiento Inicial)

Responsable de convertir una entrada cruda en un gasto estructurado.

Flujo lógico:

1. **Extracción de datos** (OCR, transcripción, parsing).
2. **Matching contra providers.csv** (prioridad máxima).
3. **Matching contra keywords.csv** si el proveedor es genérico.
4. **Inferencia con IA** solo si no hubo coincidencias.
5. **Validación fiscal básica** (RFC y régimen).
6. **Cálculo de confianza** (reglas > IA).

El resultado es un gasto provisional, nunca definitivo.

---

### 2. The Auditor (Confirmación y Correcciones)

Se activa tras la respuesta del usuario.

Funciones:

* Confirmar registros sin cambios.
* Aplicar correcciones explícitas.
* Registrar trazabilidad completa.

Ejemplo de auditoría:

```
AUDITORÍA: Usuario cambió monto de 150.00 a 180.00 (2025-01-14)
```

Nada se sobrescribe silenciosamente.

---

## Tecnologías Utilizadas

* **Lenguaje:** Python 3.10+
* **API Web:** FastAPI (webhook Telegram)
* **Bot:** python-telegram-bot
* **IA:** OpenAI API
* **OCR / Parsing:** vía IA
* **Almacenamiento:** Google Sheets (vía google-api-python-client)
* **Datos locales:** CSV / JSON
* **Validación:** Pydantic

---

## Estructura del Proyecto

```
/expense-tracker-python
│── .env
│── requirements.txt
│
│── /config
│   ├── user_config.json
│   ├── providers.csv
│   ├── keywords.csv
│   └── google_credentials.json
│
│── /src
│   ├── main.py              # FastAPI + webhook Telegram
│   ├── data_models.py       # Modelos Pydantic
│   │
│   ├── /modules
│   │   ├── ai_agents.py     # Analyst & Auditor
│   │   ├── config_loader.py # Carga y validación de CSV/JSON
│   │   ├── input_handler.py # Texto, voz, imagen, PDF
│   │   └── data_manager.py  # Google Sheets / storage
│   │
│   └── /prompts
│       ├── analyst_prompt.txt
│       └── auditor_prompt.txt
```

---

## Principios de Diseño

* Configuración > Código
* Reglas explícitas > Inferencia probabilística
* Confirmación humana obligatoria
* Auditoría antes que automatismo ciego
* IA como herramienta, no como autoridad

Este proyecto está diseñado para crecer hacia contabilidad automática, reportes fiscales y automatización financiera sin perder control humano.
