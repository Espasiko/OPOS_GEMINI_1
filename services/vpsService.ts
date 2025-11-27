/**
 * VPS API Service
 * 
 * Connects to the existing FastAPI backend on VPS
 * Domain: https://electroyhogarpelotazo.tienda
 */

const VPS_API_URL = import.meta.env.VITE_VPS_API_URL || 'https://electroyhogarpelotazo.tienda';

export interface RAGSearchRequest {
  query: string;
  top_k?: number;
  filters?: Record<string, any>;
}

export interface RAGSearchResponse {
  answer: string;
  sources: Array<{
    content: string;
    metadata: Record<string, any>;
    score: number;
  }>;
  model_used: string;
}

export interface RAGIndexRequest {
  docs: Array<{
    content: string;
    metadata?: Record<string, any>;
    id?: string;
  }>;
}

/**
 * Search documents using RAG
 */
export async function ragSearch(request: RAGSearchRequest): Promise<RAGSearchResponse> {
  try {
    const response = await fetch(`${VPS_API_URL}/rag/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request)
    });

    if (!response.ok) {
      throw new Error(`RAG search failed: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error in RAG search:', error);
    throw error;
  }
}

/**
 * Index documents in the vector store
 */
export async function ragIndex(request: RAGIndexRequest): Promise<{ status: string; indexed: number }> {
  try {
    const response = await fetch(`${VPS_API_URL}/rag/index`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request)
    });

    if (!response.ok) {
      throw new Error(`RAG index failed: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error indexing documents:', error);
    throw error;
  }
}

/**
 * Health check
 */
export async function healthCheck(): Promise<{ status: string; service: string }> {
  try {
    const response = await fetch(`${VPS_API_URL}/health`);
    
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error in health check:', error);
    throw error;
  }
}

/**
 * Get API documentation URL
 */
export function getDocsUrl(): string {
  return `${VPS_API_URL}/docs`;
}

/**
 * Get OpenAPI spec URL
 */
export function getOpenAPIUrl(): string {
  return `${VPS_API_URL}/openapi.json`;
}
