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
