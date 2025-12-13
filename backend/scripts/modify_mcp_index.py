#!/usr/bin/env python3
"""
Script to modify mcp-server/src/index.ts to add the ingest_new_law tool
"""

# Read the original file
with open('/home/spas/OPOS_GEMINI_1/mcp-server/src/index.ts', 'r') as f:
    lines = f.readlines()

# Modification 1: Add tool definition before line 145 (index 144)
tool_definition = '''  {
    name: "ingest_new_law",
    description: "Ingesta automática de una nueva ley del BOE en la base de conocimiento RAG. Ejecuta scraping, procesamiento, ingesta en Postgres/Qdrant y verificación automática. Requiere un BOE ID válido.",
    inputSchema: {
      type: "object",
      properties: {
        boe_id: {
          type: "string",
          description: "Identificador BOE de la ley a ingestar (ej: 'BOE-A-2024-1234')",
        },
      },
      required: ["boe_id"],
    },
  },
'''

# Insert before the closing ];
lines.insert(144, tool_definition)

# Modification 2: Add case handler after line 187 (now shifted by tool_definition lines)
case_handler = '''      case "ingest_new_law":
        return await handleIngestNewLaw(args);
      
'''

# Find the line with 'case "get_law_summary"' and add after it
for i, line in enumerate(lines):
    if 'case "get_law_summary":' in line:
        # Find the next line that has 'return await'
        for j in range(i, min(i+5, len(lines))):
            if 'return await handleGetLawSummary' in lines[j]:
                lines.insert(j+2, case_handler)
                break
        break

# Modification 3: Add handler function before main()
handler_function = '''
// Implementación: Ingestar nueva ley
async function handleIngestNewLaw(args: any) {
  const { boe_id } = args;
  const { exec } = await import("child_process");
  const { promisify } = await import("util");
  const execAsync = promisify(exec);

  const projectRoot = process.cwd().replace("/mcp-server", "");
  const venvPython = `${projectRoot}/.venv/bin/python`;
  
  // Cargar variables de entorno adicionales desde .env.backend si existe
  const backendEnvPath = `${projectRoot}/backend/.env.backend`;
  try {
    const fs = await import("fs");
    if (fs.existsSync(backendEnvPath)) {
      dotenv.config({ path: backendEnvPath });
    }
  } catch (e) {
    // Ignorar si no existe
  }

  const env = {
    ...process.env,
    QDRANT_URL: process.env.QDRANT_URL || "http://localhost:6333",
    QDRANT_API_KEY: process.env.QDRANT_API_KEY || "",
    POSTGRES_HOST: process.env.POSTGRES_HOST || "localhost",
    POSTGRES_PORT: process.env.POSTGRES_PORT || "5432",
    POSTGRES_DB: process.env.POSTGRES_DB || "opositaia",
    POSTGRES_USER: process.env.POSTGRES_USER || "postgres",
    POSTGRES_PASSWORD: process.env.POSTGRES_PASSWORD || "postgres",
  };

  try {
    // Paso 1: Scraping
    const scrapeCmd = `${venvPython} ${projectRoot}/backend/utils/scrape_boe_universal.py ${boe_id}`;
    const scrapeResult = await execAsync(scrapeCmd, { env, cwd: projectRoot });
    
    // Paso 2: Ingesta
    const mdFile = `${projectRoot}/backend/data/${boe_id}_scraped.md`;
    const ingestCmd = `${venvPython} ${projectRoot}/backend/scripts/ingest_scraped_universal.py ${mdFile} ${boe_id}`;
    const ingestResult = await execAsync(ingestCmd, { env, cwd: projectRoot });
    
    // Paso 3: Verificación
    const verifyCmd = `${venvPython} ${projectRoot}/backend/scripts/verify_ingestion_universal.py ${boe_id}`;
    const verifyResult = await execAsync(verifyCmd, { env, cwd: projectRoot });

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({
            status: "success",
            boe_id: boe_id,
            scrape_summary: scrapeResult.stdout.trim().split("\\n").slice(-2).join("\\n"),
            ingest_summary: ingestResult.stdout.trim().split("\\n").slice(-2).join("\\n"),
            verification: verifyResult.stdout.trim(),
            message: `Ley ${boe_id} ingestada y verificada exitosamente`,
          }, null, 2),
        },
      ],
    };
  } catch (error: any) {
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({
            status: "error",
            boe_id: boe_id,
            error_message: error.message,
            stderr: error.stderr || "",
            stdout: error.stdout || "",
          }, null, 2),
        },
      ],
      isError: true,
    };
  }
}

'''

# Find line with 'async function main()' and insert before it
for i, line in enumerate(lines):
    if 'async function main()' in line:
        lines.insert(i, handler_function)
        break

# Write the modified file
with open('/home/spas/OPOS_GEMINI_1/mcp-server/src/index.ts', 'w') as f:
    f.writelines(lines)

print("✅ Successfully modified index.ts")
print("Added:")
print("  - Tool definition for 'ingest_new_law'")
print("  - Case handler in switch statement")
print("  - Implementation function handleIngestNewLaw()")
