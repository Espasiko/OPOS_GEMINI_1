# Sprint 11: Integración PostgreSQL en Routers

**Fecha:** 24 Nov 2025  
**Objetivo:** Integrar PostgreSQL en los routers para tracking de usuarios y progreso  
**Duración estimada:** 2-3 horas

---

## 🎯 Objetivos del Sprint

1. Crear router de usuarios (`/user`)
2. Integrar tracking en chat router
3. Guardar resultados de simulacros
4. Guardar casos prácticos generados
5. Crear endpoint de estadísticas

---

## 📋 Tareas

### Tarea 1: Router de Usuarios ✅
**Archivo:** `backend/routers/user.py`

**Endpoints:**
- `POST /user/register` - Registrar nuevo usuario
- `GET /user/{user_id}/progress` - Ver progreso
- `GET /user/{user_id}/stats` - Estadísticas detalladas
- `PUT /user/{user_id}/session` - Actualizar sesión de estudio

### Tarea 2: Integrar Tracking en Chat ✅
**Archivo:** `backend/routers/chat.py`

**Modificaciones:**
- Guardar queries RAG en `rag_queries`
- Registrar feedback de utilidad
- Tracking de tiempo de respuesta

### Tarea 3: Guardar Simulacros ✅
**Archivo:** `backend/routers/ai_functions.py`

**Modificaciones:**
- Endpoint `/ai/mock-exam` guarda resultados en `simulacros`
- Registrar puntuación, tiempo, temas evaluados

### Tarea 4: Guardar Casos Prácticos ✅
**Archivo:** `backend/routers/ai_functions.py`

**Modificaciones:**
- Endpoint `/ai/practical-case` guarda en `user_cases`
- Permitir marcar como público

### Tarea 5: Guardar Mapas Mentales ✅
**Archivo:** `backend/routers/ai_functions.py`

**Modificaciones:**
- Endpoint `/ai/mind-map` guarda en `mind_maps`
- Soporte para likes y compartir

---

## 🔧 Implementación

### Estructura de archivos:
```
backend/
├── routers/
│   ├── user.py          (NUEVO)
│   ├── chat.py          (MODIFICAR)
│   └── ai_functions.py  (MODIFICAR)
└── database/
    └── db.py            (YA EXISTE)
```

---

## ✅ Criterios de Aceptación

1. ✅ Todos los endpoints funcionan
2. ✅ Datos se guardan correctamente en PostgreSQL
3. ✅ Tests pasan
4. ✅ No hay memory leaks (conexiones se cierran)
5. ✅ Logging apropiado

---

## 🧪 Tests

Crear `backend/tests/test_user_router.py` con:
- Test de registro de usuario
- Test de obtener progreso
- Test de actualizar sesión
- Test de estadísticas

---

## 📊 Métricas de Éxito

- Tiempo de respuesta < 200ms
- 0 errores de conexión
- 100% de queries guardadas
- Cobertura de tests > 80%
