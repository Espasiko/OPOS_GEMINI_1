---
name: "opositaia-rag"
displayName: "Opositaia RAG"
description: "Servidor MCP para acceso al RAG de Seguridad Social española con herramientas de búsqueda, verificación BOE y generación de flashcards para oposiciones."
keywords: ["opositaia", "rag", "seguridad-social", "oposiciones", "boe", "jurisprudencia"]
author: "Opositaia Team"
---

# Opositaia RAG

## Overview

El servidor MCP de Opositaia proporciona acceso especializado a una base de conocimiento de Seguridad Social española a través de un sistema RAG (Retrieval-Augmented Generation). Está diseñado específicamente para estudiantes de oposiciones que necesitan acceso rápido y preciso a información legal actualizada.

El servidor conecta con Qdrant para búsquedas vectoriales y ofrece herramientas especializadas para verificación en BOE, búsqueda de jurisprudencia y generación de material de estudio.

## Herramientas Disponibles

### 1. search_rag
Busca en la base de conocimiento de leyes de Seguridad Social.

**Parámetros:**
- `query` (string, requerido): Consulta de búsqueda
- `limit` (number, opcional): Número máximo de resultados (default: 5)
- `score_threshold` (number, opcional): Umbral mínimo de relevancia (default: 0.7)

**Ejemplo:**
```typescript
await use_mcp_tool("opositaia", "search_rag", {
  query: "base de cotización máxima 2025",
  limit: 5,
  score_threshold: 0.7
});
```

### 2. verify_boe
Verifica la vigencia de una ley en el BOE oficial.

**Parámetros:**
- `ley_id` (string, requerido): Identificador BOE (ej: "BOE-A-2015-11724")
- `articulo` (string, opcional): Artículo específico a verificar

**Ejemplo:**
```typescript
await use_mcp_tool("opositaia", "verify_boe", {
  ley_id: "BOE-A-2015-11724",
  articulo: "161"
});
```

### 3. search_jurisprudence
Busca sentencias y jurisprudencia relevante.

**Parámetros:**
- `query` (string, requerido): Términos de búsqueda
- `tribunal` (string, opcional): Tribunal específico
- `fecha_desde` (string, opcional): Fecha desde (YYYY-MM-DD)
- `fecha_hasta` (string, opcional): Fecha hasta (YYYY-MM-DD)

**Ejemplo:**
```typescript
await use_mcp_tool("opositaia", "search_jurisprudence", {
  query: "incapacidad temporal",
  tribunal: "TSJ",
  fecha_desde: "2023-01-01"
});
```

### 4. generate_flashcards
Genera tarjetas de estudio sobre un tema específico.

**Parámetros:**
- `topic` (string, requerido): Tema para las flashcards
- `count` (number, opcional): Número de tarjetas (default: 10)
- `difficulty` (string, opcional): Nivel de dificultad ("facil", "medio", "dificil")

**Ejemplo:**
```typescript
await use_mcp_tool("opositaia", "generate_flashcards", {
  topic: "Artículo 161 LGSS",
  count: 10,
  difficulty: "medio"
});
```

### 5. get_law_summary
Obtiene un resumen estructurado de una ley específica.

**Parámetros:**
- `ley_id` (string, requerido): Identificador de la ley
- `include_articles` (boolean, opcional): Incluir artículos detallados
- `format` (string, opcional): Formato del resumen ("breve", "completo")

**Ejemplo:**
```typescript
await use_mcp_tool("opositaia", "get_law_summary", {
  ley_id: "LGSS",
  include_articles: true,
  format: "completo"
});
```

## Onboarding

### Prerequisites

**Sistema:**
- Node.js 18+ instalado
- Docker con Qdrant corriendo localmente
- Acceso a las APIs de Gemini y Qdrant

**Credenciales necesarias:**
- API Key de Qdrant Cloud o instancia local
- API Key de Gemini (opcional, para embeddings)
- Colección de Qdrant con datos de Seguridad Social

### Installation

1. **Verificar que el servidor esté compilado:**
```bash
cd mcp-server
npm install
npm run build
```

2. **Verificar que Qdrant esté corriendo:**
```bash
# Si usas Docker local
docker ps | grep qdrant
# Debería mostrar el contenedor corriendo en puerto 6333
```

3. **Configurar en Kiro:**
Edita `~/.kiro/settings/mcp.json` (Windows: `C:\Users\Usuario\.kiro\settings\mcp.json`):

```json
{
  "mcpServers": {
    "opositaia": {
      "command": "node",
      "args": ["/ruta/completa/a/mcp-server/dist/index.js"],
      "env": {
        "QDRANT_URL": "http://localhost:6333",
        "QDRANT_API_KEY": "tu-api-key-aqui",
        "QDRANT_COLLECTION": "leyes_seguridad_social",
        "GEMINI_API_KEY": "tu-gemini-api-key"
      }
    }
  }
}
```

4. **Reiniciar Kiro** para cargar la nueva configuración.

### Configuration

**Variables de entorno requeridas:**

- `QDRANT_URL`: URL de tu instancia Qdrant
  - Local: `http://localhost:6333`
  - Cloud: `https://tu-cluster.qdrant.io`
- `QDRANT_API_KEY`: Tu API key de Qdrant
- `QDRANT_COLLECTION`: Nombre de la colección (default: `leyes_seguridad_social`)
- `GEMINI_API_KEY`: API key de Google Gemini (opcional)

## Common Workflows

### Workflow 1: Búsqueda Básica de Información Legal

**Objetivo:** Encontrar información específica sobre un tema de Seguridad Social.

**Pasos:**
1. Usar `search_rag` con tu consulta
2. Revisar los resultados y su puntuación de relevancia
3. Si necesitas verificación oficial, usar `verify_boe`

**Ejemplo completo:**
```typescript
// 1. Buscar información
const resultados = await use_mcp_tool("opositaia", "search_rag", {
  query: "prestación por desempleo requisitos",
  limit: 3,
  score_threshold: 0.8
});

// 2. Verificar en BOE si es necesario
const verificacion = await use_mcp_tool("opositaia", "verify_boe", {
  ley_id: "BOE-A-2015-11724",
  articulo: "266"
});
```

### Workflow 2: Preparación de Examen con Flashcards

**Objetivo:** Generar material de estudio para un tema específico.

**Pasos:**
1. Identificar el tema de estudio
2. Generar flashcards con `generate_flashcards`
3. Complementar con búsqueda de jurisprudencia relacionada

**Ejemplo completo:**
```typescript
// 1. Generar flashcards
const flashcards = await use_mcp_tool("opositaia", "generate_flashcards", {
  topic: "Incapacidad temporal",
  count: 15,
  difficulty: "medio"
});

// 2. Buscar jurisprudencia relacionada
const jurisprudencia = await use_mcp_tool("opositaia", "search_jurisprudence", {
  query: "incapacidad temporal",
  fecha_desde: "2022-01-01"
});
```

### Workflow 3: Investigación Jurisprudencial Completa

**Objetivo:** Realizar un análisis completo de un tema legal.

**Pasos:**
1. Búsqueda inicial en RAG
2. Obtener resumen de ley relevante
3. Buscar jurisprudencia actualizada
4. Verificar vigencia en BOE

**Ejemplo completo:**
```typescript
// 1. Búsqueda inicial
const info_base = await use_mcp_tool("opositaia", "search_rag", {
  query: "pensión de jubilación anticipada",
  limit: 5
});

// 2. Resumen de ley
const resumen = await use_mcp_tool("opositaia", "get_law_summary", {
  ley_id: "LGSS",
  include_articles: true
});

// 3. Jurisprudencia
const sentencias = await use_mcp_tool("opositaia", "search_jurisprudence", {
  query: "jubilación anticipada",
  tribunal: "TS"
});

// 4. Verificación BOE
const vigencia = await use_mcp_tool("opositaia", "verify_boe", {
  ley_id: "BOE-A-2015-11724"
});
```

## Troubleshooting

### Error: "Connection refused" o servidor no responde

**Causa:** El servidor MCP no puede iniciarse o conectar con Qdrant.

**Soluciones:**
1. **Verificar que Qdrant esté corriendo:**
   ```bash
   curl http://localhost:6333/health
   # Debería devolver: {"status":"ok"}
   ```

2. **Verificar compilación del servidor:**
   ```bash
   cd mcp-server
   npm run build
   ls -la dist/  # Verificar que index.js existe
   ```

3. **Probar el servidor manualmente:**
   ```bash
   cd mcp-server
   node dist/index.js
   ```

4. **Verificar variables de entorno en mcp.json**

### Error: "Collection not found"

**Causa:** La colección de Qdrant no existe o tiene un nombre diferente.

**Soluciones:**
1. **Verificar colecciones existentes:**
   ```bash
   curl http://localhost:6333/collections
   ```

2. **Actualizar el nombre en mcp.json:**
   ```json
   "QDRANT_COLLECTION": "nombre-correcto-de-coleccion"
   ```

### Error: "API key invalid"

**Causa:** Las API keys no son válidas o están mal configuradas.

**Soluciones:**
1. **Verificar API key de Qdrant:**
   - Si es local, puede que no necesites API key
   - Si es cloud, verifica en tu dashboard de Qdrant

2. **Verificar API key de Gemini:**
   - Verifica en https://aistudio.google.com/app/apikey
   - Asegúrate de que tenga permisos para Gemini API

### Error: "Tool not found"

**Causa:** El nombre de la herramienta no es correcto.

**Solución:**
Usar los nombres exactos:
- `search_rag`
- `verify_boe`
- `search_jurisprudence`
- `generate_flashcards`
- `get_law_summary`

### Problemas de rendimiento o resultados irrelevantes

**Causa:** Configuración de búsqueda no optimizada.

**Soluciones:**
1. **Ajustar score_threshold:**
   - Valores más altos (0.8-0.9): resultados más precisos
   - Valores más bajos (0.6-0.7): más resultados, menos precisos

2. **Refinar consultas:**
   - Usar términos específicos del dominio legal
   - Incluir sinónimos y variaciones
   - Especificar el contexto (ej: "artículo 161 LGSS")

## Best Practices

### Para Búsquedas Efectivas
- **Usa terminología legal específica** en lugar de lenguaje coloquial
- **Incluye referencias normativas** cuando las conozcas (ej: "artículo 161")
- **Ajusta el score_threshold** según la precisión que necesites
- **Combina múltiples herramientas** para obtener información completa

### Para Estudio de Oposiciones
- **Genera flashcards por temas específicos** en lugar de temas muy amplios
- **Verifica siempre en BOE** la información crítica para el examen
- **Busca jurisprudencia reciente** para estar actualizado
- **Usa diferentes niveles de dificultad** en las flashcards según tu progreso

### Para Investigación Legal
- **Comienza con búsquedas amplias** y luego especifica
- **Verifica la vigencia** de las normas que encuentres
- **Consulta jurisprudencia** para entender la aplicación práctica
- **Documenta las fuentes** BOE para referencias oficiales

### Optimización de Rendimiento
- **Usa límites apropiados** (5-10 resultados suelen ser suficientes)
- **Cachea resultados** de búsquedas repetitivas
- **Combina consultas relacionadas** en lugar de hacer múltiples búsquedas similares

## Configuration

**No se requiere configuración adicional** una vez que el servidor MCP esté instalado en Kiro.

**Configuración opcional:**
- Ajustar `score_threshold` por defecto según tus necesidades
- Configurar colecciones adicionales de Qdrant si tienes otros dominios legales
- Personalizar los prompts de generación de flashcards

---

**Servidor MCP:** `opositaia`  
**Repositorio:** Local en `mcp-server/`  
**Especialización:** Seguridad Social española y oposiciones