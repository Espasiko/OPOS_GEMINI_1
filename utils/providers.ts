/**
 * Provider Utilities - Sprint 10
 * 
 * Funciones helper para manejar providers de AI
 */

export interface ProviderInfo {
  id: string;
  name: string;
  modelId: string;
}

/**
 * Mapea el ID del modelo al provider correspondiente
 * 
 * @param modelId - ID del modelo (ej: 'groq-8b', 'gemini-flash')
 * @returns Provider ID (ej: 'groq', 'google')
 */
export function getProviderFromModelId(modelId: string): string {
  if (modelId.startsWith('groq-')) {
    return 'groq';
  }
  if (modelId.startsWith('deepseek-')) {
    return 'deepseek';
  }
  if (modelId.startsWith('gemini-')) {
    return 'google';
  }
  if (modelId.startsWith('hf-')) {
    return 'huggingface';
  }
  if (modelId.startsWith('cohere-')) {
    return 'cohere';
  }
  if (modelId.startsWith('mistral-')) {
    return 'mistral-vps';
  }
  return 'groq'; // Default
}

/**
 * Obtiene información completa del provider
 * 
 * @param modelId - ID del modelo
 * @returns Información del provider (id, name, modelId)
 */
export function getProviderInfo(modelId: string): ProviderInfo {
  const provider = getProviderFromModelId(modelId);
  
  const providerNames: Record<string, string> = {
    groq: 'Groq',
    deepseek: 'DeepSeek',
    google: 'Google Gemini',
    huggingface: 'Hugging Face',
    cohere: 'Cohere',
    'mistral-vps': 'Mistral VPS',
  };
  
  return {
    id: provider,
    name: providerNames[provider] || provider,
    modelId,
  };
}

/**
 * Verifica si un provider está disponible
 * 
 * @param providerId - ID del provider
 * @returns true si el provider está disponible
 */
export function isProviderAvailable(providerId: string): boolean {
  const availableProviders = ['groq', 'deepseek', 'google', 'huggingface', 'cohere', 'mistral-vps'];
  return availableProviders.includes(providerId);
}
