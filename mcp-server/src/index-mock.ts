#!/usr/bin/env node

/**
 * Opositaia MCP Server - MOCK VERSION
 * Para testing sin necesidad de Qdrant
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from "@modelcontextprotocol/sdk/types.js";

// Mock data
const MOCK_LEYES = [
  {
    id: "1",
    ley: "LGSS",
    articulo: "161",
    contenido: "La prestación económica por incapacidad temporal trata de cubrir la pérdida de rentas que se produce cuando el trabajador está imposibilitado temporalmente para trabajar y precisa asistencia sanitaria de la Seguridad Social.",
    fecha: "2015-10-30",
    boe_url: "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724"
  },
  {
    id: "2",
    ley: "LGSS",
    articulo: "194",
    contenido: "La base de cotización máxima será la establecida anualmente en la correspondiente Ley de Presupuestos Generales del Estado.",
    fecha: "2015-10-30",
    boe_url: "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724"
  },
  {
    id: "3",
    ley: "RD 2064/1995",
    articulo: "1",
    contenido: "El presente Reglamento tiene por objeto el desarrollo de las normas legales de cotización a la Seguridad Social.",
    fecha: "1995-12-22",
    boe_url: "https://www.boe.es/buscar/act.php?id=BOE-A-1996-845"
  }
];

const TOOLS: Tool[] = [
  {
    name: "search_rag",
    description: "Busca información en la base de conocimiento de leyes de Seguridad Social española. [MOCK VERSION - Datos de prueba]",
    inputSchema: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description: "Pregunta o término a buscar",
        },
        limit: {
          type: "number",
          description: "Número máximo de resultados (default: 5)",
          default: 5,
        },
      },
      required: ["query"],
    },
  },
  {
    name: "verify_boe",
    description: "Verifica si una ley está vigente en el BOE. [MOCK VERSION]",
    inputSchema: {
      type: "object",
      properties: {
        ley_id: {
          type: "string",
          description: "Identificador de la ley",
        },
      },
      required: ["ley_id"],
    },
  },
  {
    name: "generate_flashcards",
    description: "Genera flashcards de estudio. [MOCK VERSION]",
    inputSchema: {
      type: "object",
      properties: {
        topic: {
          type: "string",
          description: "Tema para generar flashcards",
        },
        count: {
          type: "number",
          description: "Número de flashcards (default: 10)",
          default: 10,
        },
      },
      required: ["topic"],
    },
  },
];

const server = new Server(
  {
    name: "opositaia-mcp-server-mock",
    version: "1.0.0-mock",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools: TOOLS };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "search_rag":
        return handleSearchRAG(args);
      
      case "verify_boe":
        return handleVerifyBOE(args);
      
      case "generate_flashcards":
        return handleGenerateFlashcards(args);
      
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

function handleSearchRAG(args: any) {
  const { query, limit = 5 } = args;
  
  // Búsqueda simple en mock data
  const results = MOCK_LEYES
    .filter(ley => 
      ley.contenido.toLowerCase().includes(query.toLowerCase()) ||
      ley.articulo.includes(query) ||
      ley.ley.toLowerCase().includes(query.toLowerCase())
    )
    .slice(0, limit);

  return {
    content: [
      {
        type: "text",
        text: JSON.stringify({
          query: query,
          total_results: results.length,
          results: results,
          note: "⚠️ MOCK DATA - Conecta a Qdrant Cloud para datos reales"
        }, null, 2),
      },
    ],
  };
}

function handleVerifyBOE(args: any) {
  const { ley_id } = args;

  return {
    content: [
      {
        type: "text",
        text: JSON.stringify({
          ley_id: ley_id,
          estado: "VIGENTE",
          fecha_consulta: new Date().toISOString(),
          url_boe: `https://www.boe.es/buscar/act.php?id=${ley_id}`,
          note: "⚠️ MOCK DATA - Implementar verificación real del BOE"
        }, null, 2),
      },
    ],
  };
}

function handleGenerateFlashcards(args: any) {
  const { topic, count = 10 } = args;

  const flashcards = Array.from({ length: Math.min(count, 5) }, (_, i) => ({
    id: i + 1,
    pregunta: `¿Qué regula ${topic}? (Pregunta ${i + 1})`,
    respuesta: `Respuesta sobre ${topic} basada en la legislación vigente.`,
    dificultad: "medio",
    tags: [topic],
  }));

  return {
    content: [
      {
        type: "text",
        text: JSON.stringify({
          topic: topic,
          count: flashcards.length,
          flashcards: flashcards,
          note: "⚠️ MOCK DATA - Integrar con LLM para generación real"
        }, null, 2),
      },
    ],
  };
}

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  
  console.error("🧪 Opositaia MCP Server (MOCK) iniciado");
  console.error("⚠️  Usando datos de prueba - No conectado a Qdrant");
}

main().catch((error) => {
  console.error("Error fatal:", error);
  process.exit(1);
});
