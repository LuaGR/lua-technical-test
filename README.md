# Survey API & Weather Widget - Arquitectura

¡Buenas! Este proyecto es la solución para una prueba técnica que busca evaluar capacidad de diseño arquitectónico, claridad de código y visión de futuro. Acá te cuento cómo lo estructuré y porqué tomé cada decisión.

---

## Escalabilidad Futura

La arquitectura y estructura del proyecto están pensadas para facilitar la **escalabilidad** y el crecimiento a futuro. Algunas decisiones clave:

- **Monorepo NX:** Permite sumar nuevas apps (microservicios, widgets, libs compartidas) sin perder control ni duplicar esfuerzos.
- **Carpetas por feature (Screaming Architecture):** Si el dominio crece, se pueden agregar nuevas features como `/users`, `/responses`, `/analytics`, etc., manteniendo el código organizado y desacoplado.
- **Clean Architecture:** Separar en capas (domain, application, infrastructure, api) permite cambiar frameworks, bases de datos, o integrar nuevas tecnologías sin reescribir la lógica de negocio.
- **Repository Pattern:** Facilita migrar entre sistemas de persistencia (ej: de PostgreSQL a MongoDB) o agregar cachés/distribución.
- **Frontend Atomic Design:** Permite escalar el widget a una app más grande, sumar nuevas vistas, o reutilizar componentes en otros proyectos.
- **Testing y CI/CD centralizados:** Listo para escalar el equipo y mantener calidad en cada nueva funcionalidad.

La base está pensada para que, aunque el producto crezca en usuarios, features o complejidad, el código siga siendo mantenible y extensible.


---

## 1. Overview

Este repo es un **monorepo NX** que contiene dos apps independientes:

- **survey-be**: API REST para encuestas (FastAPI + PostgreSQL)
- **weather-widget-fe**: Widget del clima (Vue 3 + Composition API)

### Objetivos

- **survey-be:** Permitir la creación, gestión y extensión de encuestas flexibles y robustas, con validaciones claras y arquitectura escalable.
- **weather-widget-fe:** Brindar información del clima de cualquier ciudad de forma amigable, rápida y resiliente ante fallos de API, con feedback visual según la temperatura.
- Justificar cada decisión técnica y facilitar el testing, mantenibilidad y extensibilidad en ambos proyectos.

---

## 2. Decisiones Técnicas

### Monorepo con NX

- **¿Por qué?** Un solo repo para front y back, con tooling centralizado (linting, testing, scripts, CI/CD). Ideal para proyectos que pueden crecer y sumar más apps o libs.
- **Escala a futuro:** Si el producto crece, puedes sumar microservicios, libs compartidas, etc.

### Backend: Clean Architecture + Screaming Architecture + FastAPI

- **Screaming Architecture:** Las carpetas principales del backend representan features del dominio, por ejemplo `/surveys`, `/questions`, etc. Así, el propósito de la app grita desde el folder root.
- **Clean Architecture por feature:** Dentro de cada feature, separo en capas: `domain` (modelos/lógica pura), `application` (casos de uso), `infrastructure` (repositorios/adaptadores), y la capa de entrada `api` (routers/endpoints HTTP). Esto desacopla frameworks y facilita testing, escalabilidad y mantenimiento.
- **Repository pattern:** Permite cambiar la DB o el sistema de persistencia sin afectar la lógica.
- **Enum para tipos de preguntas:** Usar `enum` en modelos y DB para evitar errores y facilitar queries/migraciones.
- **Survey sin preguntas:** Permitir creación vacía para flexibilidad y mejor UX. Justificado porque es común armar encuestas en partes.
- **Opciones solo en preguntas choice:** Constraint y validación en endpoint y DB para robustez.
- **Timestamps:** Para auditar y ordenar datos.

### Frontend: Atomic Design + Vue 3

- **Atomic Design:** Componentes chicos, reutilizables y escalables.
- **Container/Presentational:** Separar lógica de UI para facilitar testing y mantenibilidad.
- **State management:** Para este caso, `ref`/`reactive` locales, pero listo para escalar a Pinia/signals si el widget crece.
- **Fallback de APIs:** Si el API principal falla, cambia automáticamente a otro proveedor público. Muestra resiliencia y experiencia real.
- **Testing:** Unit tests con Vitest y @vue/test-utils.

---

## 3. Estructura del Proyecto

```
/apps
  /survey-be          # FastAPI app (encuestas)
  /weather-widget-fe  # Vue 3 app (weather widget)
/libs                 # Compartir tipos/utils si es necesario
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

- **Stack:** FastAPI, PostgreSQL, Alembic (migraciones), Pydantic
- **Endpoints:**
  - `POST /surveys` - Crear encuesta
  - `POST /surveys/{id}/questions` - Agregar pregunta
  - `POST /questions/{id}/options` - Agregar opción (solo para choice)
- **Testing:** Pytest + FastAPI test client
- **Migraciones:** Alembic (ver comandos abajo)

### Ejemplo de uso de la API

**Crear encuesta**
```json
POST /surveys
{
  "title": "Satisfacción del servicio",
  "description": "Queremos conocer tu opinión"
}
```

**Agregar pregunta**
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

### Ejemplo de uso de la API

**Crear encuesta**
```json
POST /surveys
{
  "title": "Satisfacción del servicio",
  "description": "Queremos conocer tu opinión"
}
```

**Agregar pregunta**
```json
POST /surveys/{survey_id}/questions
{
  "text": "¿Cómo calificarías el servicio?",
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

```bash
cd apps/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Configurar DB en .env
alembic upgrade head
uvicorn main:app --reload
```

### 4.2 Modelo de Dominio: Survey (Entidad)

La entidad `Survey` representa el núcleo del dominio para el feature de encuestas. En Clean Architecture, una entidad encapsula los datos y la lógica de negocio relevante, independiente de frameworks, bases de datos o detalles de infraestructura.

#### ¿Por qué estructuramos así la entidad?

- **Atributos con significado de dominio:**  
  - `id`: Identificador único, fundamental para la identidad de la encuesta.
  - `title` y `description`: Información principal que define la encuesta.
  - `created_at`: Permite auditar y ordenar encuestas, útil para reportes y lógica temporal.
  - `status`: Usamos un Enum (`SurveyStatus`) para representar el estado de la encuesta (borrador, activa, cerrada). Esto previene errores y facilita validaciones.
  - `questions`: Lista de preguntas asociadas, modelando la relación natural entre encuesta y preguntas.

- **Métodos de negocio:**  
  - `add_question`: Permite agregar preguntas a la encuesta, reflejando el flujo real de creación.
  - `activate`: Cambia el estado a "activa", pero solo si hay preguntas, asegurando integridad del negocio.
  - `close`: Permite cerrar la encuesta, cambiando su estado.

- **Independencia de frameworks:**  
  La entidad no depende de FastAPI, Pydantic, SQLAlchemy ni ningún framework. Esto permite testear la lógica de negocio en aislamiento y migrar a otros frameworks sin reescribir el dominio.

- **Escalabilidad y mantenibilidad:**  
  Si el negocio evoluciona (por ejemplo, agregas lógica para duplicar encuestas, agregar colaboradores, etc.), lo haces aquí, sin tocar la infraestructura. Facilita la extensión: puedes agregar más métodos o atributos sin romper el resto del sistema.

- **Claridad y robustez:**  
  Usar Enums para estados y tipos de pregunta evita errores de tipo y facilita migraciones/queries. Los métodos de negocio encapsulan reglas, evitando que la lógica se disperse por el código.

**Justificación arquitectónica:**  
- Separa el “qué” del negocio del “cómo” de la tecnología.
- Permite que el dominio evolucione sin depender de detalles técnicos.
- Facilita el testing unitario y la extensión futura.
- Hace explícitas las reglas y restricciones del negocio.
- Alinea el código con el lenguaje del negocio y los stakeholders.

En resumen:  
La entidad `Survey` es el corazón del feature de encuestas. Modela los datos y reglas esenciales, es independiente de la tecnología, y está lista para crecer y adaptarse a nuevas necesidades del negocio.

---

## 5. Frontend: Requerimientos y Setup

- **Stack:** Vue 3, Composition API, Vite
- **Features:** Input de ciudad, fetch weather, feedback visual según temperatura, fallback automático si el API falla.
- **Testing:** Vitest + @vue/test-utils

### Setup

```bash
cd apps/frontend
npm install
npm dev
```

### Cambiar API Key

Editar `.env` en frontend y poner tu key de OpenWeatherMap (tengo fallback preparado si hay error).

---

## 6. Testing

- **Backend:**
  - `cd apps/backend && pytest`
- **Frontend:**
  - `cd apps/frontend && pnpm test`
- **Linting y typecheck:**
  - `npm lint` y `npm typecheck` (en la raíz)

---

---

## 7. Tasks y Checklist

### Backend

- [ ] Crear estructura de carpetas feature-based (surveys, questions, etc.) siguiendo Clean + Screaming Architecture.
- [ ] Implementar modelos de dominio y enums en surveys y questions.
- [ ] Desarrollar casos de uso (application) para creación de encuestas y preguntas.
- [ ] Implementar repositorios y acceso a PostgreSQL en infrastructure.
- [ ] Crear endpoints HTTP en la carpeta api (routers FastAPI).
- [ ] Agregar tests unitarios y de integración con Pytest.

### Frontend

- [ ] Crear estructura de carpetas siguiendo Atomic Design.
- [ ] Implementar componente de input y botón para ciudad.
- [ ] Desarrollar lógica de fetch de clima y fallback de API.
- [ ] Mostrar feedback visual según temperatura.
- [ ] Agregar tests unitarios con Vitest y @vue/test-utils.
