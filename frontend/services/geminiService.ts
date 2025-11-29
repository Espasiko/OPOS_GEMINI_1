import {
  PracticalCase,
  GroundingSource,
  MindMapNode,
  StudyPlanInput,
  MockExam,
  Flashcard,
} from '../types';

// Configuration
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

/**
 * Helper function to make API calls to the backend
 */
async function apiCall<T>(endpoint: string, body: any): Promise<T> {
  try {
    const response = await fetch(`${BACKEND_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `API Error: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`Error calling ${endpoint}:`, error);
    throw error;
  }
}

/**
 * Intenta obtener el contenido de texto de una URL utilizando una estrategia de múltiples proxies CORS.
 */
export async function getTextFromUrl(url: string): Promise<string> {
  // TODO: Implementar endpoint en backend para esto para evitar proxies públicos
  const proxies = [
    `https://api.allorigins.win/raw?url=${encodeURIComponent(url)}`,
    `https://api.codetabs.com/v1/proxy?quest=${encodeURIComponent(url)}`,
  ];

  for (const proxyUrl of proxies) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 15000);

    try {
      const response = await fetch(proxyUrl, { signal: controller.signal });
      clearTimeout(timeoutId);

      if (response.ok) {
        const textContent = await response.text();
        if (textContent && textContent.trim().length > 0) {
          return textContent;
        }
      }
    } catch (error) {
      clearTimeout(timeoutId);
      console.warn(`Proxy failed: ${proxyUrl}`);
    }
  }

  throw new Error('No se pudo obtener el contenido de la URL.');
}

/**
 * Genera un caso práctico completo.
 */
export async function generatePracticalCase(): Promise<PracticalCase> {
  return apiCall<PracticalCase>('/ai/practical-case', {
    topic: 'Seguridad Social', // Se podría hacer dinámico
    difficulty: 'hard',
    provider: 'groq-70b' // Usar modelo potente
  });
}

/**
 * Obtiene o crea una instancia de chat.
 * En la nueva arquitectura, el estado del chat se gestiona en el backend o via API stateless.
 * Por compatibilidad, mantenemos la firma pero ahora usaremos el endpoint de chat.
 */
export const getChatInstance = (conversationId: string) => {
  return {
    sendMessage: async (message: string) => {
      const response = await apiCall<any>('/chat/message', {
        message,
        conversation_id: conversationId,
        use_rag: true,
        provider: 'mistral-vps' // O el que se prefiera
      });
      return {
        response: {
          text: () => response.response
        }
      };
    }
  };
};

/**
 * Realiza una búsqueda utilizando RAG (anteriormente Grounding).
 */
export async function searchWithGrounding(
  query: string,
  untilDate?: string
): Promise<{ text: string; sources: GroundingSource[] }> {
  // Usamos el endpoint de chat que ya devuelve fuentes
  const response = await apiCall<any>('/chat/message', {
    message: query + (untilDate ? ` (Información válida hasta ${untilDate})` : ''),
    conversation_id: 'search-' + Date.now(),
    use_rag: true,
    provider: 'mistral-vps'
  });

  return {
    text: response.response,
    sources: response.sources.map((s: any) => ({
      uri: s.norma, // Ajustar mapeo según respuesta del backend
      title: `${s.norma} ${s.articulo ? '- Art. ' + s.articulo : ''}`
    }))
  };
}

/**
 * Genera un mapa mental jerárquico.
 */
export async function generateMindMap(topic: string): Promise<MindMapNode> {
  return apiCall<MindMapNode>('/ai/mind-map', {
    topic,
    provider: 'groq-70b'
  });
}

/**
 * Genera un plan de estudios personalizado.
 */
export async function generateStudyPlan(input: StudyPlanInput): Promise<string> {
  const response = await apiCall<{ plan: string }>('/ai/study-plan', {
    exam_date: '2025-06-01', // Placeholder o input
    topics: ['Seguridad Social'],
    hours_per_day: 4,
    provider: 'groq-70b'
  });
  return response.plan;
}

/**
 * Genera un esquema estructurado.
 */
export async function generateSchema(topic: string): Promise<string> {
  const response = await apiCall<{ schema: string }>('/ai/schema', {
    topic,
    provider: 'groq-70b'
  });
  return response.schema;
}

/**
 * Genera un resumen de un texto.
 */
export async function generateSummary(text: string): Promise<string> {
  const response = await apiCall<{ summary: string }>('/ai/summary', {
    text,
    provider: 'groq-70b'
  });
  return response.summary;
}

/**
 * Compara dos versiones de un texto legal.
 */
export async function compareLawVersions(textA: string, textB: string): Promise<string> {
  const response = await apiCall<{ comparison: string }>('/ai/compare', {
    text1: textA,
    text2: textB,
    provider: 'groq-70b'
  });
  return response.comparison;
}

/**
 * Genera un simulacro de examen.
 */
export async function generateMockExam(topics: string[], questionCount: number): Promise<MockExam> {
  return apiCall<MockExam>('/ai/mock-exam', {
    topics,
    num_questions: questionCount,
    provider: 'groq-70b'
  });
}

/**
 * Genera flashcards y meme.
 * NOTA: Por ahora solo flashcards, el meme se deja pendiente o se implementará en backend.
 */
export async function generateFlashcardsAndMeme(
  topic: string
): Promise<{ flashcards: Flashcard[]; meme: { imageUrl: string; prompt: string } }> {
  const response = await apiCall<any>('/ai/flashcards', {
    topic,
    num_cards: 10,
    provider: 'groq-70b'
  });

  // Placeholder para meme ya que el backend aún no genera imágenes
  return {
    flashcards: response.cards,
    meme: {
      imageUrl: 'https://placehold.co/400x400?text=Meme+Generator+Coming+Soon',
      prompt: 'Meme generation pending backend implementation'
    }
  };
}

