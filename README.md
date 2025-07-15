# Survey API & Weather Widget - Arquitectura

¡Buenas! Este proyecto es la solución para una prueba técnica que busca evaluar capacidad de diseño arquitectónico, claridad de código y visión de futuro. Acá te cuento cómo lo estructuré y porqué tomé cada decisión.

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

## 4. Backend: Requerimientos y Setup

- **Stack:** FastAPI, PostgreSQL, Alembic (migraciones), Pydantic
- **Endpoints:**
  - `POST /surveys` - Crear encuesta
  - `POST /surveys/{id}/questions` - Agregar pregunta
  - `POST /questions/{id}/options` - Agregar opción (solo para choice)
- **Testing:** Pytest + FastAPI test client
- **Migraciones:** Alembic (ver comandos abajo)

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
