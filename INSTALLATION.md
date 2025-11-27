# 📦 Guía de Instalación Completa - OpositaIA

Esta guía te permitirá clonar el repositorio y arrancar la aplicación completa en cualquier entorno (Windows, Linux, macOS).

## 📋 Requisitos Previos

### Software Necesario

1. **Git**
   - Windows: https://git-scm.com/download/win
   - Linux: `sudo apt install git`
   - macOS: `brew install git`

2. **Node.js v20+ (recomendado v24.11.1 LTS)**
   - Descarga: https://nodejs.org/
   - Verifica: `node --version`

3. **Python 3.11+**
   - Windows: https://www.python.org/downloads/
   - Linux: `sudo apt install python3.11 python3.11-venv`
   - macOS: `brew install python@3.11`
   - Verifica: `python --version` o `python3 --version`

4. **PostgreSQL 14+** (Base de datos)
   - Windows: https://www.postgresql.org/download/windows/
   - Linux: `sudo apt install postgresql postgresql-contrib`
   - macOS: `brew install postgresql@14`
   - Verifica: `psql --version`

### Servicios Cloud (Obligatorios)

5. **Qdrant Cloud** (Vector Database - GRATIS)
   - Regístrate en: https://cloud.qdrant.io/
   - Crea un cluster gratuito
   - Guarda la URL y API Key

6. **Supabase** (PostgreSQL Cloud - GRATIS)
   - Regístrate en: https://supabase.com/
   - Crea un proyecto nuevo
   - Guarda la Connection String

### APIs de IA (Opcional pero recomendado)

7. **API Keys de Modelos de IA**
   - Google Gemini: https://aistudio.google.com/app/apikey (GRATIS)
   - Groq: https://console.groq.com/ (GRATIS)
   - OpenRouter: https://openrouter.ai/ (Pago por uso)
   - Mistral: https://console.mistral.ai/ (Pago por uso)

---

## 🚀 Instalación Paso a Paso

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/opositaia.git
cd opositaia
```

### 2. Configurar el Backend

#### 2.1. Crear entorno virtual de Python

**Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

#### 2.2. Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

Esto instalará:
- FastAPI (framework web)
- Uvicorn (servidor ASGI)
- SQLAlchemy (ORM para PostgreSQL)
- Qdrant Client (vector database)
- Sentence Transformers (embeddings)
- Y más...

#### 2.3. Configurar variables de entorno del backend

Crea el archivo `backend/.env.backend` basándote en el ejemplo:

```bash
cp .env.backend.example .env.backend
```

Edita `backend/.env.backend` con tus credenciales:

```env
# === QDRANT CLOUD (Vector Database) ===
QDRANT_URL=https://tu-cluster.gcp.cloud.qdrant.io
QDRANT_API_KEY=tu_qdrant_api_key_aqui
QDRANT_COLLECTION=opositaia_leyes_seguridad_social

# === SUPABASE POSTGRESQL ===
DATABASE_URL=postgresql://postgres:tu_password@db.tu-proyecto.supabase.co:5432/postgres

# === EMBEDDING MODEL ===
EMBEDDING_MODEL=PlanTL-GOB-ES/RoBERTalex

# === OLLAMA (Opcional - para modelos locales) ===
OLLAMA_URL=http://localhost:11434

# === API KEYS DE MODELOS DE IA ===
GEMINI_API_KEY=tu_gemini_api_key
GROQ_API_KEY=tu_groq_api_key
OPENROUTER_API_KEY=tu_openrouter_api_key
MISTRAL_API_KEY=tu_mistral_api_key

# === MISTRAL VPS (Opcional) ===
MISTRAL_VPS_URL=http://tu-servidor-vps:11434
```

#### 2.4. Inicializar la base de datos

```bash
# Asegúrate de estar en la carpeta backend con el venv activado
python database/init_db.py
```

Esto creará las tablas necesarias en PostgreSQL.

### 3. Configurar el Frontend

#### 3.1. Volver a la raíz del proyecto

```bash
cd ..  # Salir de la carpeta backend
```

#### 3.2. Instalar dependencias de Node.js

```bash
npm install
```

Esto instalará:
- React 19
- Vite
- TypeScript
- TailwindCSS
- Y más...

#### 3.3. Configurar variables de entorno del frontend

Crea el archivo `.env` basándote en el ejemplo:

```bash
cp .env.example .env
```

Edita `.env` con tus credenciales:

```env
# API Key de Google Gemini (para el frontend)
VITE_GEMINI_API_KEY=tu_gemini_api_key_aqui

# URL del backend (por defecto en desarrollo)
VITE_BACKEND_URL=http://localhost:8000
```

---

## ▶️ Arrancar la Aplicación

### Opción 1: Arrancar todo manualmente (recomendado para desarrollo)

#### Terminal 1 - Backend:

**Windows:**
```bash
cd backend
venv\Scripts\activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Linux/macOS:**
```bash
cd backend
source venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

O usa el script:
```bash
bash start-backend.sh
```

El backend estará disponible en:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

#### Terminal 2 - Frontend:

```bash
npm run dev
```

El frontend estará disponible en:
- Local: http://localhost:3000

### Opción 2: Usar Docker (próximamente)

```bash
docker-compose up
```

---

## ✅ Verificar la Instalación

### 1. Verificar Backend

```bash
curl http://localhost:8000/health
```

Deberías ver:
```json
{
  "status": "healthy",
  "embedding_model": "PlanTL-GOB-ES/RoBERTalex",
  "qdrant_url": "https://...",
  "ollama_url": "http://localhost:11434"
}
```

### 2. Verificar Base de Datos

```bash
cd backend
source venv/bin/activate  # o venv\Scripts\activate en Windows
python test_db_integration.py
```

### 3. Verificar Qdrant

```bash
python check_qdrant_status.py
```

Deberías ver información sobre las leyes indexadas.

### 4. Verificar Frontend

Abre http://localhost:3000 en tu navegador. Deberías ver la interfaz de OpositaIA.

---

## 🗂️ Estructura del Proyecto

```
opositaia/
├── backend/                    # Backend FastAPI
│   ├── agents/                # Agentes de IA y RAG
│   ├── database/              # Configuración de PostgreSQL
│   ├── models/                # Modelos de datos
│   ├── routers/               # Endpoints de la API
│   ├── tests/                 # Tests del backend
│   ├── main.py                # Punto de entrada
│   ├── requirements.txt       # Dependencias Python
│   └── .env.backend           # Variables de entorno (NO SUBIR A GIT)
│
├── components/                 # Componentes React
├── services/                   # Servicios del frontend
├── contexts/                   # Contextos de React
├── utils/                      # Utilidades
├── __tests__/                  # Tests del frontend
│
├── ai-specs/                   # Especificaciones de desarrollo
├── docs/                       # Documentación
│
├── package.json                # Dependencias Node.js
├── vite.config.ts             # Configuración de Vite
├── tsconfig.json              # Configuración de TypeScript
├── .env                        # Variables de entorno frontend (NO SUBIR A GIT)
└── .gitignore                 # Archivos ignorados por Git
```

---

## 🔧 Solución de Problemas

### Error: "No module named 'fastapi'"

**Solución**: Activa el entorno virtual y reinstala dependencias:
```bash
cd backend
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
```

### Error: "Connection refused" al conectar con PostgreSQL

**Solución**: 
1. Verifica que PostgreSQL esté corriendo
2. Verifica que la `DATABASE_URL` en `.env.backend` sea correcta
3. Verifica que el firewall permita conexiones al puerto 5432

### Error: "Qdrant connection failed"

**Solución**:
1. Verifica que tu cluster de Qdrant Cloud esté activo
2. Verifica que `QDRANT_URL` y `QDRANT_API_KEY` sean correctos
3. Verifica tu conexión a internet

### Error: "Port 8000 already in use"

**Solución**: Mata el proceso que está usando el puerto:

**Windows:**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Linux/macOS:**
```bash
lsof -ti:8000 | xargs kill -9
```

### Error: "VITE_GEMINI_API_KEY not set"

**Solución**:
1. Crea el archivo `.env` en la raíz del proyecto
2. Añade: `VITE_GEMINI_API_KEY=tu_api_key`
3. Reinicia el servidor de desarrollo

---

## 📚 Próximos Pasos

1. **Lee la documentación**:
   - `README.md` - Visión general del proyecto
   - `AI_SPECS_QUICKSTART.md` - Metodología de desarrollo
   - `docs/DECISIONES_CLAVE.md` - Decisiones arquitectónicas

2. **Indexa las leyes** (si es necesario):
   ```bash
   cd backend
   source venv/bin/activate
   python agents/indexar_todas_las_leyes.py
   ```

3. **Verifica la cobertura de leyes**:
   ```bash
   python verificar_leyes_temario_oficial.py
   ```

4. **Prueba la aplicación**:
   - Abre http://localhost:3000
   - Haz una pregunta sobre leyes de Seguridad Social
   - Prueba las diferentes funcionalidades

---

## 🆘 Soporte

Si tienes problemas:

1. Revisa esta guía completa
2. Consulta los logs del backend y frontend
3. Verifica que todas las variables de entorno estén configuradas
4. Abre un issue en GitHub con:
   - Descripción del problema
   - Logs de error
   - Sistema operativo
   - Versiones de Node.js y Python

---

## 🔐 Seguridad

**IMPORTANTE**: Nunca subas a Git:
- `.env` (frontend)
- `backend/.env.backend` (backend)
- `.credentials.local`
- Cualquier archivo con API keys

Estos archivos ya están en `.gitignore`.

---

## 📝 Licencia

Ver archivo LICENSE para más detalles.
