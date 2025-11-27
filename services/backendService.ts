/**
 * Backend Service - Sprint 7
 *
 * Service to connect with FastAPI backend
 * Handles chat, upload, and RAG operations
 */

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

// ============================================================================
// TYPES
// ============================================================================

export interface ChatMessageRequest {
  message: string;
  conversation_id: string;
  use_rag?: boolean;
  provider?: string;
  top_k?: number;
  min_score?: number;
}

export interface ChatSource {
  norma: string;
  articulo?: string;
  score: number;
  content_preview: string;
}

export interface ChatMessageResponse {
  response: string;
  sources: ChatSource[];
  conversation_id: string;
}

export interface UploadFileResponse {
  document_id: string;
  filename: string;
  text_length: number;
  pages?: number;
  indexed: boolean;
  text_preview: string;
}

export interface UploadUrlRequest {
  url: string;
}

export interface UploadUrlResponse {
  document_id: string;
  url: string;
  text_length: number;
  indexed: boolean;
  text_preview: string;
}

export interface DocumentResponse {
  document_id: string;
  text: string;
  metadata: Record<string, unknown>;
}

export interface HealthResponse {
  status: string;
  mistral?: string;
  rag?: string;
  cached_documents?: number;
}

// ============================================================================
// AI FUNCTIONS TYPES (Sprint 9)
// ============================================================================

export interface PracticalCaseRequest {
  topic: string;
  difficulty: 'easy' | 'medium' | 'hard';
  provider?: string;
}

export interface PracticalCaseResponse {
  scenario: string;
  questions: Array<{
    question: string;
    points: number;
  }>;
  total_points: number;
  estimated_time: number;
}

export interface MindMapRequest {
  topic: string;
  depth?: number;
  provider?: string;
}

export interface MindMapNode {
  label: string;
  children?: MindMapNode[];
}

export interface MindMapResponse {
  root: MindMapNode;
}

export interface FlashcardsRequest {
  topic: string;
  count?: number;
  provider?: string;
}

export interface Flashcard {
  front: string;
  back: string;
  difficulty: string;
}

export interface FlashcardsResponse {
  cards: Flashcard[];
}

export interface SchemaRequest {
  topic: string;
  format?: 'outline' | 'hierarchical';
  provider?: string;
}

export interface SchemaResponse {
  title: string;
  sections: Array<{
    title: string;
    content: string[];
    subsections?: Array<{
      title: string;
      content: string[];
    }>;
  }>;
}

export interface SummaryRequest {
  text: string;
  length?: 'short' | 'medium' | 'long';
  provider?: string;
}

export interface SummaryResponse {
  summary: string;
  key_points: string[];
  word_count: number;
}

export interface CompareRequest {
  text1: string;
  text2: string;
  aspect?: string;
  provider?: string;
}

export interface CompareResponse {
  similarities: string[];
  differences: string[];
  conclusion: string;
}

export interface StudyPlanRequest {
  topic: string;
  duration_weeks: number;
  hours_per_week: number;
  provider?: string;
}

export interface StudyPlanWeek {
  week: number;
  topics: string[];
  activities: string[];
  goals: string[];
}

export interface StudyPlanResponse {
  title: string;
  total_weeks: number;
  total_hours: number;
  weeks: StudyPlanWeek[];
}

// ============================================================================
// CHAT ENDPOINTS
// ============================================================================

/**
 * Send a chat message (non-streaming)
 */
export async function sendChatMessage(request: ChatMessageRequest): Promise<ChatMessageResponse> {
  try {
    const response = await fetch(`${BACKEND_URL}/chat/message`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `Chat failed: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error sending chat message:', error);
    throw error;
  }
}

/**
 * Send a chat message with streaming (SSE)
 * Returns an async generator that yields chunks
 */
export async function* sendChatMessageStream(
  request: ChatMessageRequest
): AsyncGenerator<string, void, unknown> {
  try {
    const response = await fetch(`${BACKEND_URL}/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Chat stream failed: ${response.statusText}`);
    }

    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error('No response body');
    }

    // eslint-disable-next-line no-undef
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        break;
      }

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          if (data === '[DONE]') {
            return;
          }
          try {
            const parsed = JSON.parse(data);
            // Handle different message types
            if (parsed.error) {
              throw new Error(parsed.error);
            }
            if (parsed.sources) {
              // Sources are sent at the end
              yield JSON.stringify({ type: 'sources', data: parsed.sources });
            } else if (parsed.choices) {
              // Mistral format
              const content = parsed.choices[0]?.delta?.content || '';
              if (content) {
                yield content;
              }
            }
          } catch (e) {
            console.error('Error parsing SSE data:', e);
          }
        }
      }
    }
  } catch (error) {
    console.error('Error in chat stream:', error);
    throw error;
  }
}

export interface LLMProvider {
  id: string;
  provider: string;
  model: string;
  speed: string;
  cost: string;
  configured: boolean;
}

/**
 * Get available LLM providers
 */
export async function getProviders(): Promise<{ providers: LLMProvider[] }> {
  try {
    const response = await fetch(`${BACKEND_URL}/chat/providers`);
    if (!response.ok) {
      throw new Error(`Get providers failed: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error getting providers:', error);
    throw error;
  }
}

/**
 * Check chat service health
 */
export async function checkChatHealth(): Promise<HealthResponse> {
  try {
    const response = await fetch(`${BACKEND_URL}/chat/health`);
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error checking chat health:', error);
    throw error;
  }
}

// ============================================================================
// UPLOAD ENDPOINTS
// ============================================================================

/**
 * Upload a file (PDF or TXT)
 */
export async function uploadFile(file: File): Promise<UploadFileResponse> {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${BACKEND_URL}/upload/file`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `Upload failed: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error uploading file:', error);
    throw error;
  }
}

/**
 * Upload content from URL
 */
export async function uploadUrl(request: UploadUrlRequest): Promise<UploadUrlResponse> {
  try {
    const response = await fetch(`${BACKEND_URL}/upload/url`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `URL upload failed: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error uploading URL:', error);
    throw error;
  }
}

/**
 * Get document from cache
 */
export async function getDocument(documentId: string): Promise<DocumentResponse> {
  try {
    const response = await fetch(`${BACKEND_URL}/upload/document/${documentId}`);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `Get document failed: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error getting document:', error);
    throw error;
  }
}

/**
 * Delete document from cache
 */
export async function deleteDocument(documentId: string): Promise<{ status: string; document_id: string }> {
  try {
    const response = await fetch(`${BACKEND_URL}/upload/document/${documentId}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `Delete failed: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error deleting document:', error);
    throw error;
  }
}

/**
 * Check upload service health
 */
export async function checkUploadHealth(): Promise<HealthResponse> {
  try {
    const response = await fetch(`${BACKEND_URL}/upload/health`);
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error checking upload health:', error);
    throw error;
  }
}

// ============================================================================
// GENERAL ENDPOINTS
// ============================================================================

/**
 * Check backend health
 */
export async function checkBackendHealth(): Promise<HealthResponse> {
  try {
    const response = await fetch(`${BACKEND_URL}/health`);
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error checking backend health:', error);
    throw error;
  }
}

/**
 * Get backend root info
 */
export async function getBackendInfo(): Promise<Record<string, unknown>> {
  try {
    const response = await fetch(`${BACKEND_URL}/`);
    if (!response.ok) {
      throw new Error(`Get info failed: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error getting backend info:', error);
    throw error;
  }
}

// ============================================================================
// AI FUNCTIONS ENDPOINTS (Sprint 9)
// ============================================================================

/**
 * Generate a practical case
 */
export async function generatePracticalCase(request: PracticalCaseRequest): Promise<PracticalCaseResponse> {
  try {
    const response = await fetch(`${BACKEND_URL}/ai/practical-case`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `Practical case generation failed: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error generating practical case:', error);
    throw error;
  }
}

/**
 * Generate a mind map
 */
export async function generateMindMap(request: MindMapRequest): Promise<MindMapResponse> {
  try {
    const response = await fetch(`${BACKEND_URL}/ai/mind-map`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `Mind map generation failed: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error generating mind map:', error);
    throw error;
  }
}

/**
 * Generate flashcards
 */
export async function generateFlashcards(request: FlashcardsRequest): Promise<FlashcardsResponse> {
  try {
    const response = await fetch(`${BACKEND_URL}/ai/flashcards`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `Flashcards generation failed: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error generating flashcards:', error);
    throw error;
  }
}

/**
 * Generate a schema/outline
 */
export async function generateSchema(request: SchemaRequest): Promise<SchemaResponse> {
  try {
    const response = await fetch(`${BACKEND_URL}/ai/schema`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `Schema generation failed: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error generating schema:', error);
    throw error;
  }
}

/**
 * Generate a summary
 */
export async function generateSummary(request: SummaryRequest): Promise<SummaryResponse> {
  try {
    const response = await fetch(`${BACKEND_URL}/ai/summary`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `Summary generation failed: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error generating summary:', error);
    throw error;
  }
}

/**
 * Compare two texts
 */
export async function compareTexts(request: CompareRequest): Promise<CompareResponse> {
  try {
    const response = await fetch(`${BACKEND_URL}/ai/compare`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `Text comparison failed: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error comparing texts:', error);
    throw error;
  }
}

/**
 * Generate a study plan
 */
export async function generateStudyPlan(request: StudyPlanRequest): Promise<StudyPlanResponse> {
  try {
    const response = await fetch(`${BACKEND_URL}/ai/study-plan`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `Study plan generation failed: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error generating study plan:', error);
    throw error;
  }
}

/**
 * Check AI functions health
 */
export async function checkAIHealth(): Promise<{ status: string; providers_available: number }> {
  try {
    const response = await fetch(`${BACKEND_URL}/ai/health`);
    if (!response.ok) {
      throw new Error(`AI health check failed: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error checking AI health:', error);
    throw error;
  }
}
