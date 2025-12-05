# OpositaIA: Asistente de Examen para la Seguridad Social

[![Installation Guide](https://img.shields.io/badge/📦-Installation_Guide-blue)](./INSTALLATION.md)
[![Setup Guide](https://img.shields.io/badge/⚙️-Setup_Guide-green)](./SETUP.md)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

> 🚀 **¿Primera vez aquí?** Lee la [Guía de Instalación Completa](./INSTALLATION.md) para configurar el proyecto desde cero.

## 1. Descripción General

OpositaIA es una aplicación web full-stack diseñada como un asistente de estudio integral para opositores al Cuerpo Administrativo de la Administración de la Seguridad Social en España.

**Arquitectura:**
- **Frontend**: React 19 + TypeScript + Vite (carpeta `frontend/`)
- **Backend**: FastAPI + Python (carpeta `backend/`)
- **Base de Datos**: Qdrant (Vector DB) + PostgreSQL
- **IA**: Google Gemini, Groq, DeepSeek, Claude, Mistral

---

## 2. Estructura del Proyecto

```
/
├── frontend/                  # Aplicación React
│   ├── components/           # Componentes UI
│   ├── services/             # Servicios API
│   ├── contexts/             # React Contexts
│   ├── hooks/                # Custom Hooks
│   ├── utils/                # Utilidades
│   ├── package.json          # Dependencias frontend
│   └── vite.config.ts        # Configuración Vite
├── backend/                   # API FastAPI
│   ├── main.py               # Punto de entrada
│   ├── routers/              # Endpoints API
│   ├── services/             # Lógica de negocio
│   └── .env.backend          # Variables de entorno
├── dataset_generator/         # Scripts generación Q&A
├── scripts/                   # Scripts mantenimiento
│   ├── maintenance/          # Scripts de mantenimiento
│   └── tests/                # Scripts de prueba
├── docs/                      # Documentación
│   ├── AI_AGENTS.md          # Especificación prompts IA
│   ├── ARCHITECTURE.md       # Arquitectura del sistema
│   └── DATA_MODEL.md         # Modelo de datos
└── docker-compose.yml         # Servicios Docker
```

---

## 3. Instalación y Configuración

### **Requisitos Previos:**

- **Node.js** 18+ (para el frontend)
- **Python** 3.10+ (para el backend)
- **Docker** (para Qdrant y PostgreSQL)
- **WSL** (opcional, para Ollama local)

### **Paso 1: Clonar el Repositorio**

```bash
git clone https://github.com/tu-usuario/OPOS_GEMINI_1.git
cd OPOS_GEMINI_1
```

### **Paso 2: Configurar Backend**

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.backend.example .env.backend
# Edita .env.backend con tus API keys
```

### **Paso 3: Iniciar Servicios Docker**

```bash
# Desde la raíz del proyecto
docker-compose up -d

# Verificar que Qdrant y PostgreSQL están corriendo
docker ps
```

Deberías ver:
- `opositaia-qdrant` (puerto 6333)
- `opositaia-postgres` (puerto 5432)

### **Paso 4: Configurar Frontend**

```bash
cd frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env
# Edita .env con tu API key de Google Gemini
```

### **Paso 5: Iniciar la Aplicación**

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

La aplicación estará disponible en:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 4. Servicios y Puertos

| Servicio | Puerto | Ubicación | Estado |
|----------|--------|-----------|--------|
| Frontend (Vite) | 3000 | `frontend/` | ✅ |
| Backend (FastAPI) | 8000 | `backend/` | ✅ |
| Qdrant | 6333 | Docker | ✅ |
| PostgreSQL | 5432 | Docker | ✅ |
| Ollama (opcional) | 11434 | WSL | ⚠️ |

---

## 5. Características Principales

- **Chat Explicativo**: Tutor IA 24/7 para resolver dudas legales
- **Generador de Casos Prácticos**: Supuestos complejos con 5 preguntas tipo test
- **Simulacros de Examen**: Exámenes completos con control de tiempo
- **Búsqueda Actualizada**: Google Search grounding para respuestas actualizadas
- **Mapas Mentales**: Visualización interactiva de conceptos
- **Esquemas y Resúmenes**: Generación automática de material de estudio
- **Comparador de Leyes**: Análisis de diferencias entre versiones legales
- **Tarjetas y Memes**: Flashcards interactivas con contenido visual
- **Plan de Estudios**: Planificación personalizada
- **Mi Progreso**: Estadísticas de rendimiento

---

## 6. Desarrollo

### **Scripts Disponibles (Frontend)**

```bash
cd frontend

npm run dev          # Servidor de desarrollo
npm run build        # Build de producción
npm run preview      # Preview del build
npm run test         # Ejecutar tests
npm run lint         # Linter
npm run format       # Formatear código
```

### **Scripts Disponibles (Backend)**

```bash
cd backend

# Iniciar servidor
uvicorn main:app --reload

# Tests
pytest

# Linter
black .
flake8 .
```

---

## 7. Despliegue

### **Frontend (Vercel)**

1. Conecta tu repositorio a Vercel
2. **Importante**: Configura el "Root Directory" como `frontend`
3. Las variables de entorno se configuran en el panel de Vercel

### **Backend (VPS/Railway/Render)**

1. Asegúrate de que `.env.backend` tiene todas las API keys
2. Configura las variables de entorno en tu plataforma
3. El backend se conecta a Qdrant Cloud (ya configurado en `.env.backend`)

---

## 8. Documentación Adicional

- **[Arquitectura del Sistema](./docs/ARCHITECTURE.md)**: Visión de alto nivel
- **[Definición de Agentes de IA](./docs/AI_AGENTS.md)**: Configuración de prompts
- **[Modelo de Datos](./docs/DATA_MODEL.md)**: Estructuras de datos

---

## 9. Solución de Problemas

### **Frontend no compila**

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### **Backend no encuentra Qdrant**

```bash
# Verificar que Docker está corriendo
docker ps

# Reiniciar Qdrant
docker restart opositaia-qdrant

# Ver logs
docker logs opositaia-qdrant
```

### **Error de CORS**

Verifica que `CORS_ORIGINS` en `backend/.env.backend` incluye tu URL del frontend:
```
CORS_ORIGINS=http://localhost:3000,https://tu-dominio.com
```

---

## 10. Licencia

MIT License - Ver [LICENSE](./LICENSE) para más detalles.
