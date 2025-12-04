# 🎓 SETUP: Servidor MCP de Opositaia

**Fecha**: 23 Noviembre 2025  
**Estado**: ✅ Compilado y listo para usar

---

## ✅ LO QUE HEMOS CREADO

### 📦 Servidor MCP Personalizado

Hemos creado tu propio servidor MCP en `mcp-server/` con 5 herramientas:

1. **search_rag** - Busca en Qdrant (tu RAG de leyes)
2. **verify_boe** - Verifica vigencia en BOE
3. **search_jurisprudence** - Busca sentencias
4. **generate_flashcards** - Genera tarjetas de estudio
5. **get_law_summary** - Resumen de leyes

### 📁 Estructura Creada

```
mcp-server/
├── package.json          # Dependencias
├── tsconfig.json         # Config TypeScript
├── .env.example          # Plantilla de variables
├── README.md             # Documentación
├── src/
│   └── index.ts          # Código del servidor
└── dist/                 # Compilado (generado)
    └── index.js
```

---

## ⚙️ CONFIGURACIÓN

### Paso 1: Crear archivo .env

```bash
# En mcp-server/
cp .env.example .env
```

Edita `mcp-server/.env` con tus credenciales:

```env
QDRANT_URL=https://tu-cluster.qdrant.io
QDRANT_API_KEY=tu-api-key-aqui
QDRANT_COLLECTION=leyes_seguridad_social
```

### Paso 2: Configurar en Kiro

Edita `C:\Users\USER\.kiro\settings\mcp.json`:

```json
{
  "mcpServers": {
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    },
    "opositaia": {
      "command": "node",
      "args": ["E:/1/OPOS_GEMINI_1/mcp-server/dist/index.js"],
      "env": {
        "QDRANT_URL": "https://tu-cluster.qdrant.io",
        "QDRANT_API_KEY": "tu-api-key-aqui",
        "QDRANT_COLLECTION": "leyes_seguridad_social"
      }
    }
  }
}
```

### Paso 3: Reiniciar Kiro

1. Cierra Kiro completamente
2. Abre Kiro de nuevo
3. El servidor MCP se conectará automáticamente

---

## 🧪 PROBAR EL SERVIDOR

### Desde Kiro (Chat):

```
"Usa la herramienta search_rag para buscar información sobre 
'base de cotización máxima 2025'"
```

### Desde código:

```typescript
// Kiro llamará automáticamente al MCP
const result = await use_mcp_tool("opositaia", "search_rag", {
  query: "base de cotización máxima 2025",
  limit: 5,
  score_threshold: 0.7
});
```

---

## 🔧 DESARROLLO

### Compilar cambios:

```bash
cd mcp-server
npm run build
```

### Modo desarrollo (watch):

```bash
cd mcp-server
npm run dev
```

### Ver logs:

Los logs del servidor MCP aparecen en:
- Kiro: Panel "MCP Logs"
- Terminal: Si ejecutas manualmente

---

## 📊 HERRAMIENTAS DISPONIBLES

### 1. search_rag

**Descripción**: Busca en tu base de conocimiento de leyes

**Parámetros**:
```typescript
{
  query: string;           // Pregunta o término
  limit?: number;          // Máx resultados (default: 5)
  score_threshold?: number; // Umbral similitud (default: 0.7)
}
```

**Ejemplo**:
```typescript
{
  query: "incapacidad temporal",
  limit: 10,
  score_threshold: 0.8
}
```

**Respuesta**:
```json
{
  "query": "incapacidad temporal",
  "total_results": 5,
  "results": [
    {
      "id": "123",
      "ley": "LGSS",
      "articulo": "161",
      "contenido": "...",
      "fecha": "2015-10-30",
      "boe_url": "https://..."
    }
  ]
}
```

---

### 2. verify_boe

**Descripción**: Verifica si una ley está vigente en el BOE

**Parámetros**:
```typescript
{
  ley_id: string;    // ID de la ley (ej: "BOE-A-2015-11724")
  articulo?: string; // Artículo específico (opcional)
}
```

**Ejemplo**:
```typescript
{
  ley_id: "BOE-A-2015-11724",
  articulo: "161"
}
```

**Respuesta**:
```json
{
  "ley_id": "BOE-A-2015-11724",
  "articulo": "161",
  "estado": "VIGENTE",
  "fecha_consulta": "2025-11-23T...",
  "url_boe": "https://www.boe.es/..."
}
```

---

### 3. search_jurisprudence

**Descripción**: Busca sentencias relevantes

**Parámetros**:
```typescript
{
  query: string;              // Tema a buscar
  tribunal?: "TS"|"TSJ"|"todos"; // Tribunal (default: "todos")
  limit?: number;             // Máx sentencias (default: 3)
}
```

**Ejemplo**:
```typescript
{
  query: "incapacidad temporal",
  tribunal: "TS",
  limit: 5
}
```

---

### 4. generate_flashcards

**Descripción**: Genera tarjetas de estudio

**Parámetros**:
```typescript
{
  topic: string;                      // Tema
  count?: number;                     // Cantidad (default: 10)
  difficulty?: "facil"|"medio"|"dificil"; // Nivel
}
```

**Ejemplo**:
```typescript
{
  topic: "Artículo 161 LGSS",
  count: 15,
  difficulty: "medio"
}
```

---

### 5. get_law_summary

**Descripción**: Obtiene resumen de una ley

**Parámetros**:
```typescript
{
  ley_name: string; // Nombre de la ley (ej: "LGSS")
}
```

**Ejemplo**:
```typescript
{
  ley_name: "LGSS"
}
```

---

## 🚀 PRÓXIMOS PASOS

### Mejoras Pendientes:

1. **Embeddings** - Añadir generación de embeddings (OpenAI/Cohere)
2. **Jurisprudencia Real** - Scraping de CENDOJ
3. **LLM Integration** - Usar Groq para generar flashcards
4. **Caché** - Añadir caché de resultados
5. **Rate Limiting** - Limitar requests por minuto

### Código para añadir embeddings:

```typescript
import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

async function generateEmbedding(text: string): Promise<number[]> {
  const response = await openai.embeddings.create({
    model: "text-embedding-3-small",
    input: text,
  });
  return response.data[0].embedding;
}

// Usar en search_rag:
const embedding = await generateEmbedding(query);
const results = await qdrantClient.search(QDRANT_COLLECTION, {
  vector: embedding,
  limit: limit,
  score_threshold: score_threshold,
  with_payload: true,
});
```

---

## 🐛 TROUBLESHOOTING

### Error: "Cannot find module"
```bash
cd mcp-server
npm install
npm run build
```

### Error: "QDRANT_URL is not defined"
- Verifica que `.env` existe en `mcp-server/`
- Verifica que las variables están en `mcp.json`

### Error: "Connection refused"
- Verifica que Qdrant Cloud está accesible
- Verifica que la API key es correcta
- Prueba la conexión: `curl https://tu-cluster.qdrant.io`

### Servidor no aparece en Kiro
1. Verifica `mcp.json` está bien formateado
2. Reinicia Kiro completamente
3. Mira logs en "MCP Logs" panel

---

## 📝 NOTAS

- El servidor usa **stdio** (stdin/stdout) para comunicarse con Kiro
- Los logs van a **stderr** para no interferir con MCP
- Las credenciales se pasan por **variables de entorno** (seguro)
- El servidor se inicia automáticamente cuando Kiro lo necesita

---

**Estado**: ✅ Listo para usar  
**Próximo**: Configurar credenciales y probar

