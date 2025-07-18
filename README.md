# Survey API & Weather Widget - Arquitectura

¡Buenas! Este proyecto es la solución para una prueba técnica que busca evaluar capacidad de diseño arquitectónico, claridad de código y visión de futuro. Acá te cuento cómo lo estructuré y porqué tomé cada decisión.

## 1. Overview

Este repo es un **monorepo NX** que contiene dos apps independientes:

- **survey-be**: API REST para encuestas (FastAPI + PostgreSQL)
- **weather-widget-fe**: Widget del clima (Vue 3 + Composition API)

### Objetivos

- **survey-be:** Permitir la creación, gestión y extensión de encuestas flexibles y robustas, con validaciones claras y arquitectura escalable.
- **weather-widget-fe:** Brindar información del clima de cualquier ciudad de forma amigable, rápida y resiliente ante fallos de API, con feedback visual según la temperatura.

---

## 2. Decisiones Técnicas

### Monorepo con NX

- **¿Por qué?** Un solo repo para front y back, con tooling centralizado (linting, testing, scripts, CI/CD). Ideal para proyectos que pueden crecer y sumar más apps o libs.
- **Escala a futuro:** Si el producto crece, puedes sumar microservicios, libs compartidas, etc.

### Backend: Clean Architecture + Screaming Architecture + FastAPI

- **Screaming Architecture:** Las carpetas principales del backend representan features del dominio, por ejemplo `/surveys`, `/questions`, etc. Así, el propósito de la app grita desde el folder root.
- **Clean Architecture por feature:** Dentro de cada feature, separo en capas: `domain` (modelos/lógica pura), `application` (casos de uso), `infrastructure` (repositorios), y la capa de entrada `api` (routers/endpoints HTTP). Esto desacopla frameworks y facilita testing, escalabilidad y mantenimiento.
- **Repository pattern:** Permite cambiar la DB o el sistema de persistencia sin afectar la lógica.
- **Enum para tipos de preguntas:** Usar `enum` en modelos y DB para evitar errores y facilitar queries/migraciones.
- **Survey sin preguntas:** Permitir creación vacía para flexibilidad y mejor UX. Justificado porque es común armar encuestas en partes.
- **Opciones solo en preguntas choice:** Constraint y validación en endpoint y DB para robustez.
- **Timestamps:** Para auditar y ordenar datos.

## Frontend: Clean Architecture + Screaming Architecture + Atomic Design + Vue

- **Atomic Design (no estricto):** La estructura de componentes sigue la filosofía de Atomic Design para fomentar la reutilización y escalabilidad, pero se adapta y mezcla con principios de Clean Architecture y Screaming Architecture. Esto permite que los componentes estén organizados tanto por tipo como por feature, facilitando el crecimiento del widget a una app más grande o la reutilización en otros proyectos.
- **Separación lógica/UI:** Uso de la Composition API y separación container/presentational para facilitar mantenibilidad, manteniendo la lógica desacoplada de la presentación.
- **Gestión de estado local:** Se utiliza `ref`/`reactive` locales, pero la arquitectura está preparada para escalar a soluciones como Pinia o signals si el widget crece.
- **Fallback de APIs:** El widget es resiliente: si el API principal falla, cambia automáticamente a otro proveedor público, mejorando la experiencia de usuario y la robustez ante fallos externos.

---

## 3. Estructura del Proyecto

```
/apps
  /survey-be          # FastAPI app (encuestas)
  /weather-widget-fe  # Vue 3 app (weather widget)
/nx.json              # Configuración NX
/README.md            # Documentación
```

---

## 4. Backend

### 4.1 Requerimientos y Setup

### Decisiones en Endpoints

- **Encuestas sin preguntas:** Permitir crear encuestas vacías da flexibilidad y mejora la experiencia de usuario. Es común definir primero la encuesta y luego agregar preguntas en pasos separados, como hacen herramientas profesionales. Esto facilita el trabajo iterativo y colaborativo.
- **Fecha de creación:** Se almacena automáticamente al crear la encuesta para facilitar auditoría y orden cronológico.
- **Tipos de pregunta como Enum:** Facilita validaciones, migraciones y queries, y evita errores de tipo.
- **Validación de existencia de encuesta:** Antes de agregar una pregunta, se valida que la encuesta exista para evitar referencias inválidas.
- **Opciones solo en preguntas choice:** Validado tanto en la API como en la base de datos para robustez y consistencia.

- **Stack:** FastAPI, PostgreSQL, Alembic, Pydantic
- **Endpoints:**
  - `POST /surveys` - Crear encuesta
  - `POST /surveys/{id}/questions` - Agregar pregunta
  - `POST /questions/{id}/options` - Agregar opción (solo para choice)
  - `GET /surveys` - Listar todas las encuestas
  - `GET /surveys/{survey_id}` - Obtener detalles de una encuesta (con preguntas y opciones)
- **Migraciones:** Alembic

### Ejemplo de uso de la API

**Crear encuesta**

```json
POST /surveys
{
  "title": "Satisfacción del servicio",
  "description": "Queremos conocer tu opinión"
}
```

**Listar encuestas**

```json
GET /surveys
```

**Obtener detalles de una encuesta**

```json
GET /surveys/{survey_id}
```

**Agregar pregunta a una encuesta**

```json
POST /surveys/{survey_id}/questions
{
  "text": "¿Cómo calificarías nuestro servicio?",
  "question_type": "single_choice"
}
```

**Agregar opción a pregunta choice**

```json
POST /questions/{question_id}/options
{
  "text": "Muy satisfecho"
}
```

### Setup

#### 1. Levantar la base de datos con Docker

Asegúrate de tener Docker instalado. Desde la raíz del proyecto, ejecuta:

```bash
docker-compose up -d
```

Esto creará un contenedor de PostgreSQL accesible en `localhost:5432` con la base de datos `survey_db`, usuario `postgres` y contraseña `postgres`.

---

#### 2. Configurar y correr el backend

1. Ve a la carpeta del backend:

   ```bash
   cd apps/survey-be
   ```

2. Crea y activa el entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Configura la URL de la base de datos en `.env`:

   ```
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/survey_db
   ```

5. Aplica las migraciones para crear las tablas:

   ```bash
   alembic upgrade head
   ```

6. Inicia el servidor FastAPI:

   - Si estás en `/apps/survey-be/`:
     ```bash
     uvicorn src.main:app --reload
     ```
   - O desde `/apps/survey-be/src/`:
     ```bash
     uvicorn main:app --reload
     ```

7. Accede a la documentación interactiva en [http://localhost:8000/docs](http://localhost:8000/docs)

---

**Notas:**

- Asegúrate de tener Docker corriendo para la base de datos antes de iniciar el backend.
- Si cambias la estructura de carpetas, ajusta los comandos de Uvicorn en consecuencia.

---

## 5. Frontend: Requerimientos y Setup

## Instrucciones para revisar el frontend

1. Instala dependencias:
   ```bash
   cd apps/weather-widget-fe
   npm install
   ```

2. Inicia el servidor de desarrollo:
   ```bash
   npm run dev
   ```

3. (Opcional) Cambia la API Key de OpenWeatherMap en el archivo `.env` si lo deseas.
