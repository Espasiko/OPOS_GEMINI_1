/**
 * Format Utilities - Sprint 10
 * 
 * Funciones para convertir formatos de respuestas del backend
 */

import { MindMapNode } from '../types';

/**
 * Convierte nodo del backend (label) a formato frontend (text)
 * 
 * @param node - Nodo del backend con formato { label, children }
 * @param parentId - ID del nodo padre (para generar IDs únicos)
 * @returns Nodo en formato frontend { id, text, children }
 */
export function convertMindMapNode(node: any, parentId = ''): MindMapNode {
  if (!node || !node.label) {
    throw new Error('Nodo inválido en la respuesta');
  }
  
  const id = parentId ? `${parentId}-${node.label}` : node.label;
  
  return {
    id,
    text: node.label,
    children: node.children
      ? node.children.map((child: any, idx: number) => 
          convertMindMapNode(child, `${id}-${idx}`)
        )
      : [],
  };
}

/**
 * Convierte schema del backend a markdown
 * 
 * @param response - Respuesta del backend con formato estructurado
 * @returns String en formato markdown
 */
export function convertSchemaToMarkdown(response: any): string {
  if (!response || !response.title || !response.sections) {
    throw new Error('Respuesta de schema inválida');
  }

  let markdown = `# ${response.title}\n\n`;
  
  response.sections.forEach((section: any) => {
    markdown += `* ${section.title}\n`;
    
    if (section.content && Array.isArray(section.content)) {
      section.content.forEach((item: string) => {
        markdown += `  * ${item}\n`;
      });
    }
    
    if (section.subsections && Array.isArray(section.subsections)) {
      section.subsections.forEach((sub: any) => {
        markdown += `  * ${sub.title}\n`;
        if (sub.content && Array.isArray(sub.content)) {
          sub.content.forEach((item: string) => {
            markdown += `    * ${item}\n`;
          });
        }
      });
    }
  });
  
  return markdown;
}

/**
 * Convierte study plan del backend a texto formateado
 * 
 * @param response - Respuesta del backend con plan estructurado
 * @returns String con el plan formateado
 */
export function convertStudyPlanToText(response: any): string {
  if (!response || !response.title || !response.weeks) {
    throw new Error('Respuesta de study plan inválida');
  }

  let planText = `# ${response.title}\n\n`;
  planText += `**Duración:** ${response.total_weeks} semanas\n`;
  planText += `**Horas totales:** ${response.total_hours} horas\n\n`;

  response.weeks.forEach((week: any) => {
    planText += `## Semana ${week.week}\n\n`;
    
    if (week.topics && Array.isArray(week.topics)) {
      planText += `**Temas:**\n`;
      week.topics.forEach((topic: string) => {
        planText += `- ${topic}\n`;
      });
    }
    
    if (week.activities && Array.isArray(week.activities)) {
      planText += `\n**Actividades:**\n`;
      week.activities.forEach((activity: string) => {
        planText += `- ${activity}\n`;
      });
    }
    
    if (week.goals && Array.isArray(week.goals)) {
      planText += `\n**Objetivos:**\n`;
      week.goals.forEach((goal: string) => {
        planText += `- ${goal}\n`;
      });
    }
    
    planText += `\n`;
  });

  return planText;
}

/**
 * Formatea resumen con puntos clave
 * 
 * @param response - Respuesta del backend con summary y key_points
 * @returns String con el resumen formateado
 */
export function formatSummaryWithKeyPoints(response: any): string {
  if (!response || !response.summary) {
    throw new Error('Respuesta de summary inválida');
  }

  let formattedSummary = response.summary;
  
  if (response.key_points && Array.isArray(response.key_points) && response.key_points.length > 0) {
    formattedSummary += '\n\n**Puntos Clave:**\n';
    response.key_points.forEach((point: string) => {
      formattedSummary += `• ${point}\n`;
    });
  }
  
  return formattedSummary;
}

/**
 * Valida que una respuesta del backend tenga los campos requeridos
 * 
 * @param response - Respuesta del backend
 * @param requiredFields - Array de campos requeridos
 * @throws Error si falta algún campo requerido
 */
export function validateResponse(response: any, requiredFields: string[]): void {
  if (!response) {
    throw new Error('Respuesta inválida del servidor');
  }
  
  const missingFields = requiredFields.filter(field => !(field in response));
  
  if (missingFields.length > 0) {
    throw new Error(`Respuesta incompleta. Faltan campos: ${missingFields.join(', ')}`);
  }
}
