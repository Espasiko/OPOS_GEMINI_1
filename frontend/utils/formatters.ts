import { MindMapNode } from '../types';

export function validateResponse(obj: any, requiredFields: string[]): void {
  if (!obj || typeof obj !== 'object') throw new Error('Respuesta inválida');
  for (const f of requiredFields) {
    if (!(f in obj)) throw new Error(`Campo requerido faltante: ${f}`);
  }
}

export function convertMindMapNode(node: any): MindMapNode {
  // Conversión mínima a estructura esperada
  const toNode = (n: any, idPrefix = 'node'): MindMapNode => ({
    id: String(n.id || `${idPrefix}-${Math.random().toString(36).slice(2, 8)}`),
    text: String(n.label || n.text || 'Nodo'),
    children: Array.isArray(n.children) ? n.children.map((c: any, i: number) => toNode(c, `${idPrefix}-${i}`)) : [],
  });
  return toNode(node);
}

export function convertSchemaToMarkdown(res: any): string {
  // Si tiene sections con title/content, volcar a bullets simples
  if (res && Array.isArray(res.sections)) {
    const lines: string[] = [];
    for (const s of res.sections) {
      lines.push(`* ${s.title || 'Sección'}`);
      if (Array.isArray(s.content)) {
        for (const c of s.content) lines.push(`  * ${c}`);
      }
      if (Array.isArray(s.subsections)) {
        for (const ss of s.subsections) {
          lines.push(`  * ${ss.title || 'Subsección'}`);
          if (Array.isArray(ss.content)) {
            for (const c of ss.content) lines.push(`    * ${c}`);
          }
        }
      }
    }
    return lines.join('\n');
  }
  return typeof res === 'string' ? res : '* Esquema no disponible';
}

export function convertStudyPlanToText(res: any): string {
  if (!res) return 'Plan no disponible';
  const parts: string[] = [];
  if (res.title) parts.push(`# ${res.title}`);
  if (Array.isArray(res.weeks)) {
    for (const w of res.weeks) {
      parts.push(`\nSemana ${w.week}`);
      if (Array.isArray(w.topics)) parts.push(`- Temas: ${w.topics.join(', ')}`);
      if (Array.isArray(w.activities)) parts.push(`- Actividades: ${w.activities.join(', ')}`);
      if (Array.isArray(w.goals)) parts.push(`- Objetivos: ${w.goals.join(', ')}`);
    }
  }
  return parts.join('\n');
}

export function formatSummaryWithKeyPoints(res: any): string {
  if (res && typeof res.summary === 'string') return res.summary;
  if (res && Array.isArray(res.key_points)) return res.key_points.join('\n');
  return 'Resumen no disponible';
}
