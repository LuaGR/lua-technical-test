# Survey API & Weather Widget - Arquitectura

¡Buenas! Este proyecto es mi solución para una prueba técnica en la que quiero reflejar mi enfoque arquitectónico, la claridad del código y cómo preparo todo pensando en el futuro. Aquí te cuento cómo lo estructuré y por qué tomé cada decisión.

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

## 5. Frontend: Decisiones en la Interfaz y Funcionalidad 

- **Input validado:** El campo de ciudad no permite números y muestra errores solo después de la interacción del usuario, mejorando la experiencia y evitando búsquedas inválidas.
- **Prevención de búsquedas repetidas:** No permite realizar la misma búsqueda dos veces seguidas, evitando llamadas innecesarias a la API.
- **Feedback visual inmediato:** El usuario recibe mensajes claros de carga, error y resultados, con feedback visual según la temperatura.
- **Fallback automático:** Si la API principal falla, el widget consulta automáticamente una API alternativa, asegurando resiliencia y continuidad en la experiencia.
- **Tipado estricto:** Uso de TypeScript para modelos y props, asegurando robustez y autocompletado.

## 6. 🚀 Quick Start: Run Everything with Docker

1. Clona el repositorio:
   ```bash
   git clone <url-del-repo>
   cd <carpeta-del-repo>
   ```

2. Levanta todo el stack (backend, frontend y base de datos):
   ```bash
   docker-compose up --build
   ```

   Esto construirá las imágenes, instalará dependencias, aplicará migraciones y levantará todos los servicios.

3. Accede a las aplicaciones:
   - **Frontend:** [http://localhost:4200](http://localhost:4200)
   - **Backend (API docs):** [http://localhost:8000/docs](http://localhost:8000/docs)

4. Para detener los servicios:
   ```bash
   docker-compose down
   ```

**Notas:**
- No necesitas instalar dependencias ni crear archivos `.env` manualmente.
- Si quieres reiniciar la base de datos desde cero: `docker-compose down -v`
- Las migraciones se aplican automáticamente al arrancar el backend.
