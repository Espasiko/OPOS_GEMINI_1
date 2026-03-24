#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const PROJECT_ROOT = '/home/spas/OPOS_GEMINI_1';
const BMAD_ROOT = path.join(PROJECT_ROOT, '.bmad');
const OUTPUT_DIR = path.join(PROJECT_ROOT, '.continue/bmad-prompts');

console.log('🚀 Generador de Prompts BMAD para Continue.dev\n');

// Función simple para parsear CSV
function parseCSV(content) {
    const lines = content.split('\n').filter(line => line.trim());
    if (lines.length === 0) return [];

    const headers = lines[0].split(',').map(h => h.trim().replace(/^"|"$/g, ''));
    const rows = [];

    for (let i = 1; i < lines.length; i++) {
        const line = lines[i];
        if (!line.trim()) continue;

        // Parser CSV simple que maneja comillas
        const values = [];
        let current = '';
        let inQuotes = false;

        for (let j = 0; j < line.length; j++) {
            const char = line[j];

            if (char === '"') {
                inQuotes = !inQuotes;
            } else if (char === ',' && !inQuotes) {
                values.push(current.trim().replace(/^"|"$/g, ''));
                current = '';
            } else {
                current += char;
            }
        }
        values.push(current.trim().replace(/^"|"$/g, ''));

        const row = {};
        headers.forEach((header, index) => {
            row[header] = values[index] || '';
        });

        if (row.name) { // Solo incluir filas con nombre
            rows.push(row);
        }
    }

    return rows;
}

// Leer manifiestos
const agentManifestPath = path.join(BMAD_ROOT, '_cfg/agent-manifest.csv');
const workflowManifestPath = path.join(BMAD_ROOT, '_cfg/workflow-manifest.csv');

console.log('📖 Leyendo manifiestos...');
console.log(`   - Agentes: ${agentManifestPath}`);
console.log(`   - Workflows: ${workflowManifestPath}\n`);

// Parsear CSV
const agents = parseCSV(fs.readFileSync(agentManifestPath, 'utf-8'));
const workflows = parseCSV(fs.readFileSync(workflowManifestPath, 'utf-8'));

console.log(`✓ Encontrados ${agents.length} agentes`);
console.log(`✓ Encontrados ${workflows.length} workflows\n`);

// Crear directorios
console.log('📁 Creando directorios de salida...');
fs.mkdirSync(path.join(OUTPUT_DIR, 'agents'), { recursive: true });
fs.mkdirSync(path.join(OUTPUT_DIR, 'workflows'), { recursive: true });
console.log(`   - ${OUTPUT_DIR}/agents/`);
console.log(`   - ${OUTPUT_DIR}/workflows/\n`);

// Generar prompts para agentes
console.log('🤖 Generando prompts de agentes...');
agents.forEach(agent => {
    const agentPath = path.join(BMAD_ROOT, agent.path);
    const promptContent = `---
name: ${agent.name}
description: ${agent.title}
invokable: true
---

Activa el agente **${agent.displayName}** (${agent.title}).

**Instrucciones de activación**:

1. Lee el archivo completo del agente: \`${agentPath}\`
2. Sigue EXACTAMENTE todas las instrucciones de activación del agente
3. Carga la configuración desde: \`${BMAD_ROOT}/${agent.module}/config.yaml\`
4. Ejecuta el agente según su persona y menú definidos

**IMPORTANTE**: NO improvises. Lee y ejecuta el archivo del agente tal como está definido.

**Rol**: ${agent.role}
**Módulo**: ${agent.module}
`;

    const outputPath = path.join(OUTPUT_DIR, 'agents', `${agent.name}.md`);
    fs.writeFileSync(outputPath, promptContent);
    console.log(`   ✓ ${agent.name}.md`);
});

// Generar prompts para workflows
console.log('\n⚙️  Generando prompts de workflows...');
workflows.forEach(workflow => {
    const workflowPath = path.join(BMAD_ROOT, workflow.path);
    const promptContent = `---
name: ${workflow.name}
description: ${workflow.description}
invokable: true
---

Ejecuta el workflow **${workflow.name}**.

**Descripción**: ${workflow.description}

**Instrucciones de ejecución**:

1. Lee el archivo completo del workflow: \`${workflowPath}\`
2. Sigue TODOS los pasos del workflow en el orden especificado
3. Usa los recursos, templates y datos definidos en el workflow
4. Genera los artefactos en la carpeta de salida configurada

**IMPORTANTE**: NO improvises. Ejecuta el workflow completo tal como está definido.

**Módulo**: ${workflow.module}
`;

    const outputPath = path.join(OUTPUT_DIR, 'workflows', `${workflow.name}.md`);
    fs.writeFileSync(outputPath, promptContent);
    console.log(`   ✓ ${workflow.name}.md`);
});

console.log(`\n✅ Generación completa:`);
console.log(`   - ${agents.length} agentes`);
console.log(`   - ${workflows.length} workflows`);
console.log(`   - Total: ${agents.length + workflows.length} prompts invocables\n`);

console.log('📍 Ubicación: ' + OUTPUT_DIR);
console.log('\n🎯 Próximos pasos:');
console.log('   1. Copia config.yaml a ~/.continue/config.yaml');
console.log('   2. Recarga VS Code (Ctrl+R)');
console.log('   3. Abre Continue (Ctrl+L) y escribe "/" para ver los comandos BMAD');
