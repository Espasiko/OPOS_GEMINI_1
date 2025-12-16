#!/usr/bin/env node

/**
 * Opositaia MCP Server
 * 
 * Servidor MCP para acceso al RAG de Seguridad Social española.
 * Usa modelo pablosi/bge-m3-spa-law-qa-trained-2 para embeddings (1024 dims)
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from "@modelcontextprotocol/sdk/types.js";
import { QdrantClient } from "@qdrant/js-client-rest";
import axios from "axios";
import * as dotenv from "dotenv";

dotenv.config();

// Configuración
const QDRANT_URL = process.env.QDRANT_URL || "http://localhost:6333";
const QDRANT_API_KEY = process.env.QDRANT_API_KEY;
const QDRANT_COLLECTION = process.env.QDRANT_COLLECTION || "opositaia_knowledge";
const HUGGINGFACE_TOKEN = process.env.HUGGINGFACE_TOKEN;
const MISTRAL_API_KEY = process.env.MISTRAL_API_KEY;

// Cliente Qdrant
const qdrantClient = new QdrantClient({
  url: QDRANT_URL,
  apiKey: QDRANT_API_KEY,
  checkCompatibility: false,
});

// Embedding con modelo pablosi (HuggingFace) - RECOMENDADO
async function generatePablosiEmbedding(text: string): Promise<number[]> {
  if (!HUGGINGFACE_TOKEN) {
    throw new Error("HUGGINGFACE_TOKEN no configurada");
  }
  const response = await axios.post(
    'https://api-inference.huggingface.co/models/pablosi/bge-m3-spa-law-qa-trained-2',
    { inputs: text },
    {
      headers: {
        'Authorization': `Bearer ${HUGGINGFACE_TOKEN}`,
        'Content-Type': 'application/json'
      },
      timeout: 30000
    }
  );
  return response.data;
}

// Embedding con Mistral AI (fallback)
async function generateMistralEmbedding(text: string): Promise<number[]> {
  if (!MISTRAL_API_KEY) {
    throw new Error("MISTRAL_API_KEY no configurada");
  }
  const response = await axios.post(
    'https://api.mistral.ai/v1/embeddings',
    { model: 'mistral-embed', input: text },
    {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${MISTRAL_API_KEY}`
      },
      timeout: 10000
    }
  );
  return response.data.data[0].embedding;
}

// Función principal para generar embeddings
async function generateEmbedding(text: string): Promise<number[]> {
  if (HUGGINGFACE_TOKEN) {
    try {
      return await generatePablosiEmbedding(text);
    } catch (err: any) {
      console.error("Error con pablosi:", err.message);
    }
  }
  if (MISTRAL_API_KEY) {
    return await generateMistralEmbedding(text);
  }
  throw new Error("No hay proveedor de embeddings. Configura HUGGINGFACE_TOKEN o MISTRAL_API_KEY");
}

// Definición de herramientas
const TOOLS: Tool[] = [
  {
    name: "search_rag",
    description: "Busca información en la base de conocimiento de leyes de Seguridad Social española.",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Pregunta o término a buscar" },
        limit: { type: "number", description: "Número máximo de resultados (default: 5)" },
        score_threshold: { type: "number", description: "Umbral mínimo de similitud (0-1, default: 0.7)" },
      },
      required: ["query"],
    },
  },
  {
    name: "list_collections",
    description: "Lista todas las colecciones disponibles en Qdrant.",
    inputSchema: { type: "object", properties: {}, required: [] },
  },
  {
    name: "verify_boe",
    description: "Verifica si una ley está vigente consultando el BOE oficial.",
    inputSchema: {
      type: "object",
      properties: {
        ley_id: { type: "string", description: "Identificador de la ley (ej: 'BOE-A-2015-11724')" },
        articulo: { type: "string", description: "Número de artículo específico (opcional)" },
      },
      required: ["ley_id"],
    },
  },
  {
    name: "search_jurisprudence",
    description: "Busca sentencias relevantes del Tribunal Supremo y TSJ.",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Tema legal a buscar" },
        tribunal: { type: "string", enum: ["TS", "TSJ", "todos"], description: "Tribunal específico" },
        limit: { type: "number", description: "Número máximo de sentencias (default: 3)" },
      },
      required: ["query"],
    },
  },
  {
    name: "get_law_summary",
    description: "Obtiene un resumen estructurado de una ley.",
    inputSchema: {
      type: "object",
      properties: {
        ley_name: { type: "string", description: "Nombre de la ley (ej: 'LGSS')" },
      },
      required: ["ley_name"],
    },
  },
  {
    name: "ingest_new_law",
    description: "Ingesta automática de una nueva ley del BOE.",
    inputSchema: {
      type: "object",
      properties: {
        boe_id: { type: "string", description: "Identificador BOE (ej: 'BOE-A-2024-1234')" },
      },
      required: ["boe_id"],
    },
  },
];

// Crear servidor MCP
const server = new Server(
  { name: "opositaia-mcp-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: TOOLS }));

server.setRequestHandler(CallToolRequestSchema, async (request: any) => {
  const { name, arguments: args } = request.params;
  try {
    switch (name) {
      case "search_rag": return await handleSearchRAG(args);
      case "list_collections": return await handleListCollections();
      case "verify_boe": return await handleVerifyBOE(args);
      case "search_jurisprudence": return await handleSearchJurisprudence(args);
      case "get_law_summary": return await handleGetLawSummary(args);
      case "ingest_new_law": return await handleIngestNewLaw(args);
      default: throw new Error(`Herramienta desconocida: ${name}`);
    }
  } catch (error: any) {
    return { content: [{ type: "text", text: `Error: ${error.message}` }], isError: true };
  }
});

async function handleListCollections() {
  const collections = await qdrantClient.getCollections();
  const details = await Promise.all(
    collections.collections.map(async (col: any) => {
      try {
        const info = await qdrantClient.getCollection(col.name);
        return { name: col.name, indexed_vectors_count: info.indexed_vectors_count, points_count: info.points_count, status: info.status };
      } catch { return { name: col.name, error: "No se pudo obtener info" }; }
    })
  );
  return { content: [{ type: "text", text: JSON.stringify({ collections: details }, null, 2) }] };
}

async function handleSearchRAG(args: any) {
  const { query, limit = 5, score_threshold = 0.7 } = args;
  try {
    const embedding = await generateEmbedding(query);
    const results = await qdrantClient.search(QDRANT_COLLECTION, {
      vector: embedding, limit, score_threshold, with_payload: true, with_vector: false,
    });
    const formatted = results.map((r: any) => ({
      id: r.id, score: r.score,
      ley: r.payload?.metadata?.law_name || r.payload?.law_name || "Desconocida",
      articulo: r.payload?.metadata?.article_id || r.payload?.article_id || "",
      contenido: r.payload?.text || r.payload?.content || "",
      boe_url: r.payload?.metadata?.boe_url || "",
    }));
    return { content: [{ type: "text", text: JSON.stringify({ query, collection: QDRANT_COLLECTION, total_results: formatted.length, results: formatted }, null, 2) }] };
  } catch (error: any) {
    const results = await qdrantClient.scroll(QDRANT_COLLECTION, { limit, with_payload: true, with_vector: false });
    const formatted = results.points.map((r: any) => ({
      id: r.id, ley: r.payload?.metadata?.law_name || "Desconocida",
      articulo: r.payload?.metadata?.article_id || "", contenido: r.payload?.text || "",
    }));
    return { content: [{ type: "text", text: JSON.stringify({ query, total_results: formatted.length, results: formatted, note: "Búsqueda sin embeddings" }, null, 2) }] };
  }
}

async function handleVerifyBOE(args: any) {
  const { ley_id, articulo } = args;
  const response = await axios.get(`https://www.boe.es/buscar/act.php?id=${ley_id}`, { timeout: 10000 });
  const estado = response.data.includes("VIGENTE") ? "VIGENTE" : response.data.includes("DEROGADO") ? "DEROGADO" : "DESCONOCIDO";
  return { content: [{ type: "text", text: JSON.stringify({ ley_id, articulo: articulo || "toda la ley", estado, fecha_consulta: new Date().toISOString(), url_boe: `https://www.boe.es/buscar/act.php?id=${ley_id}` }, null, 2) }] };
}

async function handleSearchJurisprudence(args: any) {
  const { query, tribunal = "todos", limit = 3 } = args;
  try {
    const embedding = await generateEmbedding(query);
    const results = await qdrantClient.search(QDRANT_COLLECTION, { vector: embedding, limit, with_payload: true, with_vector: false });
    const formatted = results.map((r: any) => ({ id: r.id, score: r.score, tribunal: r.payload?.tribunal || tribunal, resumen: r.payload?.text || "" }));
    return { content: [{ type: "text", text: JSON.stringify({ query, tribunal, total_results: formatted.length, sentencias: formatted }, null, 2) }] };
  } catch (error: any) {
    return { content: [{ type: "text", text: JSON.stringify({ query, tribunal, total_results: 0, sentencias: [], note: error.message }, null, 2) }] };
  }
}

async function handleGetLawSummary(args: any) {
  const { ley_name } = args;
  const embedding = await generateEmbedding(ley_name);
  const results = await qdrantClient.search(QDRANT_COLLECTION, { vector: embedding, limit: 20, with_payload: true, with_vector: false });
  const articulos = results.map((r: any) => ({ articulo: r.payload?.metadata?.article_id || "", contenido: (r.payload?.text || "").substring(0, 200) + "...", score: r.score }));
  return { content: [{ type: "text", text: JSON.stringify({ ley: ley_name, total_articulos: articulos.length, articulos }, null, 2) }] };
}

async function handleIngestNewLaw(args: any) {
  const { boe_id } = args;
  const { exec } = await import("child_process");
  const { promisify } = await import("util");
  const execAsync = promisify(exec);
  const projectRoot = process.cwd().replace(/[/\\]mcp-server$/, "");
  const venvPython = `${projectRoot}/.venv/bin/python`;
  const env = { ...process.env, QDRANT_URL: QDRANT_URL, QDRANT_API_KEY: QDRANT_API_KEY || "" };
  try {
    const scrapeCmd = `${venvPython} ${projectRoot}/backend/utils/scrape_boe_universal.py ${boe_id}`;
    const scrapeResult = await execAsync(scrapeCmd, { env, cwd: projectRoot });
    const mdFile = `${projectRoot}/backend/data/${boe_id}_scraped.md`;
    const ingestCmd = `${venvPython} ${projectRoot}/backend/scripts/ingest_scraped_universal.py ${mdFile} ${boe_id}`;
    const ingestResult = await execAsync(ingestCmd, { env, cwd: projectRoot });
    return { content: [{ type: "text", text: JSON.stringify({ status: "success", boe_id, scrape: scrapeResult.stdout.trim().split("\n").slice(-2).join("\n"), ingest: ingestResult.stdout.trim().split("\n").slice(-2).join("\n") }, null, 2) }] };
  } catch (error: any) {
    return { content: [{ type: "text", text: JSON.stringify({ status: "error", boe_id, error: error.message, stderr: error.stderr || "" }, null, 2) }], isError: true };
  }
}

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Opositaia MCP Server iniciado");
  console.error(`Qdrant: ${QDRANT_URL} | Colección: ${QDRANT_COLLECTION}`);
  console.error(`HuggingFace: ${!!HUGGINGFACE_TOKEN} | Mistral: ${!!MISTRAL_API_KEY}`);
}

main().catch((error) => { console.error("Error fatal:", error); process.exit(1); });
