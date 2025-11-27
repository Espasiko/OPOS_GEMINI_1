#!/usr/bin/env node

/**
 * Script de prueba para el servidor MCP de Opositaia
 * Simula la comunicación MCP sin necesitar Kiro
 */

import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

console.log('🧪 Probando servidor MCP de Opositaia...\n');

// Iniciar el servidor
const serverPath = join(__dirname, 'dist', 'index.js');
const server = spawn('node', [serverPath], {
  env: {
    ...process.env,
    QDRANT_URL: process.env.QDRANT_URL || 'http://localhost:6333',
    QDRANT_COLLECTION: process.env.QDRANT_COLLECTION || 'leyes_seguridad_social',
  },
  stdio: ['pipe', 'pipe', 'pipe']
});

let responseBuffer = '';

server.stdout.on('data', (data) => {
  responseBuffer += data.toString();
  
  // Intentar parsear respuestas JSON-RPC
  const lines = responseBuffer.split('\n');
  responseBuffer = lines.pop() || '';
  
  lines.forEach(line => {
    if (line.trim()) {
      try {
        const response = JSON.parse(line);
        console.log('📥 Respuesta del servidor:');
        console.log(JSON.stringify(response, null, 2));
        console.log('');
      } catch (e) {
        // No es JSON, probablemente log
      }
    }
  });
});

server.stderr.on('data', (data) => {
  console.log('📋 Log del servidor:', data.toString().trim());
});

server.on('error', (error) => {
  console.error('❌ Error al iniciar servidor:', error);
  process.exit(1);
});

// Esperar a que el servidor esté listo
setTimeout(() => {
  console.log('\n🔧 Enviando solicitud de inicialización...\n');
  
  // 1. Inicializar
  const initRequest = {
    jsonrpc: '2.0',
    id: 1,
    method: 'initialize',
    params: {
      protocolVersion: '2024-11-05',
      capabilities: {},
      clientInfo: {
        name: 'test-client',
        version: '1.0.0'
      }
    }
  };
  
  server.stdin.write(JSON.stringify(initRequest) + '\n');
  
  // 2. Listar herramientas
  setTimeout(() => {
    console.log('🔧 Solicitando lista de herramientas...\n');
    
    const listToolsRequest = {
      jsonrpc: '2.0',
      id: 2,
      method: 'tools/list',
      params: {}
    };
    
    server.stdin.write(JSON.stringify(listToolsRequest) + '\n');
    
    // 3. Probar herramienta search_rag
    setTimeout(() => {
      console.log('🔧 Probando herramienta search_rag...\n');
      
      const callToolRequest = {
        jsonrpc: '2.0',
        id: 3,
        method: 'tools/call',
        params: {
          name: 'search_rag',
          arguments: {
            query: 'base de cotización',
            limit: 3
          }
        }
      };
      
      server.stdin.write(JSON.stringify(callToolRequest) + '\n');
      
      // Esperar respuestas y cerrar
      setTimeout(() => {
        console.log('\n✅ Prueba completada. Cerrando servidor...\n');
        server.kill();
        process.exit(0);
      }, 3000);
      
    }, 2000);
    
  }, 2000);
  
}, 1000);

// Timeout de seguridad
setTimeout(() => {
  console.error('\n⏱️ Timeout: El servidor no respondió en 15 segundos');
  server.kill();
  process.exit(1);
}, 15000);
