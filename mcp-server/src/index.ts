#!/usr/bin/env node

/**
 * Opositaia MCP Server
 * 
 * Servidor MCP que expone herramientas para:
 * - Buscar en RAG de Qdrant (leyes de Seguridad Social)
 * - Verificar en BOE oficial
 * - Buscar jurisprudencia
 * - Generar contenido de estudio
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
const QDRANT_COLLECTION = process.env.QDRANT_COLLECTION || "leyes_seguridad_social";

// Cliente Qdrant
const qdrantClient = new QdrantClient({
  url: QDRANT_URL,
  apiKey: QDRANT_API_KEY,
});

// Definición de herramientas
const TOOLS: Tool[] = [
  {
    name: "search_rag",
    description: "Busca información en la base de conocimiento de leyes de Seguridad Social española indexadas en Qdrant. Devuelve chunks relevantes con metadatos (ley, artículo, fecha).",
    inputSchema: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description: "Pregunta o término a buscar (ej: 'base de cotización máxima 2025')",
        },
        limit: {
          type: "number",
          description: "Número máximo de resultados (default: 5)",
          default: 5,
        },
        score_threshold: {
          type: "number",
          description: "Umbral mínimo de similitud (0-1, default: 0.7)",
          default: 0.7,
        },
      },
      required: ["query"],
    },
  },
  {
    name: "verify_boe",
    description: "Verifica si una ley o artículo está vigente consultando el BOE oficial. Devuelve estado (VIGENTE/DEROGADO/MODIFICADO), fecha de última modificación y URL del BOE.",
    inputSchema: {
      type: "object",
      properties: {
        ley_id: {
          type: "string",
          description: "Identificador de la ley (ej: 'BOE-A-2015-11724' o 'LGSS')",
        },
        articulo: {
          type: "string",
          description: "Número de artículo específico (opcional)",
        },
      },
      required: ["ley_id"],
    },
  },
  {
    name: "search_jurisprudence",
    description: "Busca sentencias relevantes del Tribunal Supremo y TSJ relacionadas con Seguridad Social. Útil para conocer interpretaciones judiciales de las normas.",
    inputSchema: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description: "Tema o concepto legal a buscar (ej: 'incapacidad temporal')",
        },
        tribunal: {
          type: "string",
          description: "Tribunal específico: 'TS' (Supremo) o 'TSJ' (Superior Justicia)",
          enum: ["TS", "TSJ", "todos"],
          default: "todos",
        },
        limit: {
          type: "number",
          description: "Número máximo de sentencias (default: 3)",
          default: 3,
        },
      },
      required: ["query"],
    },
  },
  {
    name: "generate_flashcards",
    description: "Genera flashcards (tarjetas de estudio) a partir de un tema o artículo de ley. Devuelve preguntas y respuestas en formato estructurado.",
    inputSchema: {
      type: "object",
      properties: {
        topic: {
          type: "string",
          description: "Tema o artículo para generar flashcards (ej: 'Artículo 161 LGSS')",
        },
        count: {
          type: "number",
          description: "Número de flashcards a generar (default: 10)",
          default: 10,
        },
        difficulty: {
          type: "string",
          description: "Nivel de dificultad",
          enum: ["facil", "medio", "dificil"],
          default: "medio",
        },
      },
      required: ["topic"],
    },
  },
  {
    name: "get_law_summary",
    description: "Obtiene un resumen estructurado de una ley completa con sus artículos principales, ámbito de aplicación y conceptos clave.",
    inputSchema: {
      type: "object",
      properties: {
        ley_name: {
          type: "string",
          description: "Nombre de la ley (ej: 'LGSS', 'LISOS', 'RD 2064/1995')",
        },
      },
      required: ["ley_name"],
    },
  },
];

// Crear servidor MCP
const server = new Server(
  {
    name: "opositaia-mcp-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Handler: Listar herramientas
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: TOOLS,
  };
});

// Handler: Ejecutar herramienta
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "search_rag":
        return await handleSearchRAG(args);
      
      case "verify_boe":
        return await handleVerifyBOE(args);
      
      case "search_jurisprudence":
        return await handleSearchJurisprudence(args);
      
      case "generate_flashcards":
        return await handleGenerateFlashcards(args);
      
      case "get_law_summary":
        return await handleGetLawSummary(args);
      
      default:
        throw new Error(`Herramienta desconocida: ${name}`);
    }
  } catch (error: any) {
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

// Implementación: Buscar en RAG
async function handleSearchRAG(args: any) {
  const { query, limit = 5, score_threshold = 0.7 } = args;

  // TODO: Generar embedding del query (usar OpenAI, Cohere, etc.)
  // Por ahora, búsqueda por scroll (obtener todos y filtrar)
  
  const results = await qdrantClient.scroll(QDRANT_COLLECTION, {
    limit: limit,
    with_payload: true,
    with_vector: false,
  });

  const formattedResults = results.points.map((result: any) => ({
    id: result.id,
    ley: result.payload?.ley_nombre || "Desconocida",
    articulo: result.payload?.articulo || "",
    contenido: result.payload?.texto || "",
    fecha: result.payload?.fecha_publicacion || "",
    boe_url: result.payload?.boe_url || "",
  }));

  return {
    content: [
      {
        type: "text",
        text: JSON.stringify({
          query: query,
          total_results: formattedResults.length,
          results: formattedResults,
        }, null, 2),
      },
    ],
  };
}

// Implementación: Verificar en BOE
async function handleVerifyBOE(args: any) {
  const { ley_id, articulo } = args;

  try {
    // Llamar a API del BOE
    const response = await axios.get(
      `https://www.boe.es/buscar/act.php?id=${ley_id}`,
      { timeout: 10000 }
    );

    // Parsear respuesta (simplificado)
    const estado = response.data.includes("VIGENTE") ? "VIGENTE" : 
                   response.data.includes("DEROGADO") ? "DEROGADO" : "DESCONOCIDO";

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({
            ley_id: ley_id,
            articulo: articulo || "toda la ley",
            estado: estado,
            fecha_consulta: new Date().toISOString(),
            url_boe: `https://www.boe.es/buscar/act.php?id=${ley_id}`,
          }, null, 2),
        },
      ],
    };
  } catch (error: any) {
    throw new Error(`Error consultando BOE: ${error.message}`);
  }
}

// Implementación: Buscar jurisprudencia
async function handleSearchJurisprudence(args: any) {
  const { query, tribunal = "todos", limit = 3 } = args;

  // TODO: Implementar scraping de CENDOJ o API de jurisprudencia
  // Por ahora, respuesta simulada
  
  const mockResults = [
    {
      tribunal: "Tribunal Supremo",
      numero: "STS 3421/2023",
      fecha: "2023-10-15",
      resumen: `Sentencia sobre ${query}`,
      url: "https://www.poderjudicial.es/search/...",
    },
  ];

  return {
    content: [
      {
        type: "text",
        text: JSON.stringify({
          query: query,
          tribunal: tribunal,
          total_results: mockResults.length,
          sentencias: mockResults,
        }, null, 2),
      },
    ],
  };
}

// Implementación: Generar flashcards
async function handleGenerateFlashcards(args: any) {
  const { topic, count = 10, difficulty = "medio" } = args;

  // Primero buscar información del tema en RAG
  const ragResults = await handleSearchRAG({ query: topic, limit: 3 });
  
  // TODO: Usar LLM para generar flashcards basadas en el contenido
  // Por ahora, respuesta simulada
  
  const mockFlashcards = Array.from({ length: count }, (_, i) => ({
    id: i + 1,
    pregunta: `Pregunta ${i + 1} sobre ${topic}`,
    respuesta: `Respuesta basada en el contenido del RAG`,
    dificultad: difficulty,
    tags: [topic],
  }));

  return {
    content: [
      {
        type: "text",
        text: JSON.stringify({
          topic: topic,
          count: count,
          difficulty: difficulty,
          flashcards: mockFlashcards,
        }, null, 2),
      },
    ],
  };
}

// Implementación: Resumen de ley
async function handleGetLawSummary(args: any) {
  const { ley_name } = args;

  // Buscar todos los artículos de la ley en RAG
  const ragResults = await handleSearchRAG({ 
    query: ley_name, 
    limit: 50 
  });

  // TODO: Usar LLM para generar resumen estructurado
  
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify({
          ley: ley_name,
          total_articulos: 50, // Placeholder
          resumen: `Resumen de ${ley_name}`,
          articulos_principales: [],
          ambito_aplicacion: "",
          conceptos_clave: [],
        }, null, 2),
      },
    ],
  };
}

// Iniciar servidor
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  
  console.error("Opositaia MCP Server iniciado");
  console.error(`Conectado a Qdrant: ${QDRANT_URL}`);
  console.error(`Colección: ${QDRANT_COLLECTION}`);
}

main().catch((error) => {
  console.error("Error fatal:", error);
  process.exit(1);
});
