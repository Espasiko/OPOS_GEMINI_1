# 🎓 Opositaia MCP Server

Servidor MCP (Model Context Protocol) para Opositaia que expone herramientas de acceso al RAG de Seguridad Social española.

## 🚀 Características

### Herramientas Disponibles:

1. **search_rag** - Busca en base de conocimiento de leyes
2. **verify_boe** - Verifica vigencia en BOE oficial
3. **search_jurisprudence** - Busca sentencias relevantes
4. **generate_flashcards** - Genera tarjetas de estudio
5. **get_law_summary** - Obtiene resumen de leyes

## 📦 Instalación

```bash
cd mcp-server
npm install
npm run build
```

## ⚙️ Configuración

1. Copia `.env.example` a `.env`:
```bash
cp .env.example .env
```

2. Configura tus credenciales:
```env
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-api-key-here
QDRANT_COLLECTION=leyes_seguridad_social
```

## 🔧 Uso con Kiro

Añade a tu `~/.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "opositaia": {
      "command": "node",
      "args": ["E:/1/OPOS_GEMINI_1/mcp-server/dist/index.js"],
      "env": {
        "QDRANT_URL": "https://your-cluster.qdrant.io",
        "QDRANT_API_KEY": "your-api-key-here",
        "QDRANT_COLLECTION": "leyes_seguridad_social"
      }
    }
  }
}
```

## 📖 Ejemplos de Uso

### Buscar en RAG
```typescript
await use_mcp_tool("opositaia", "search_rag", {
  query: "base de cotización máxima 2025",
  limit: 5,
  score_threshold: 0.7
});
```

### Verificar en BOE
```typescript
await use_mcp_tool("opositaia", "verify_boe", {
  ley_id: "BOE-A-2015-11724",
  articulo: "161"
});
```

### Generar Flashcards
```typescript
await use_mcp_tool("opositaia", "generate_flashcards", {
  topic: "Artículo 161 LGSS",
  count: 10,
  difficulty: "medio"
});
```

## 🛠️ Desarrollo

```bash
# Modo desarrollo (watch)
npm run dev

# Build
npm run build

# Ejecutar
npm start
```

## 📝 TODO

- [ ] Implementar generación de embeddings (OpenAI/Cohere)
- [ ] Añadir scraping real de jurisprudencia (CENDOJ)
- [ ] Integrar LLM para generar flashcards
- [ ] Añadir caché de resultados
- [ ] Implementar rate limiting
- [ ] Añadir tests unitarios

## 🔒 Seguridad

- Las API keys se pasan por variables de entorno
- No se almacenan credenciales en el código
- Conexión segura a Qdrant Cloud (HTTPS)

## 📄 Licencia

MIT

## 🤝 Contribuir

Pull requests son bienvenidos!

---

**Creado por**: Opositaia Team  
**Fecha**: 23 Noviembre 2025
