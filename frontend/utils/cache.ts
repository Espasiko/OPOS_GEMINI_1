/**
 * Cache Utilities - Sprint 10
 * 
 * Sistema simple de caché en memoria para respuestas de AI
 */

interface CacheEntry<T> {
  data: T;
  timestamp: number;
}

const cache = new Map<string, CacheEntry<any>>();

// TTL por defecto: 5 minutos
const DEFAULT_TTL = 5 * 60 * 1000;

/**
 * Obtiene un valor del caché si existe y no ha expirado
 * 
 * @param key - Clave del caché
 * @param ttl - Tiempo de vida en milisegundos (opcional)
 * @returns Valor cacheado o null si no existe o expiró
 */
export function getCached<T>(key: string, ttl: number = DEFAULT_TTL): T | null {
  const cached = cache.get(key);
  
  if (!cached) {
    return null;
  }
  
  // Verificar si expiró
  if (Date.now() - cached.timestamp > ttl) {
    cache.delete(key);
    return null;
  }
  
  return cached.data as T;
}

/**
 * Guarda un valor en el caché
 * 
 * @param key - Clave del caché
 * @param data - Datos a cachear
 */
export function setCache<T>(key: string, data: T): void {
  cache.set(key, {
    data,
    timestamp: Date.now(),
  });
}

/**
 * Elimina un valor específico del caché
 * 
 * @param key - Clave del caché a eliminar
 */
export function deleteCache(key: string): void {
  cache.delete(key);
}

/**
 * Limpia todo el caché
 */
export function clearCache(): void {
  cache.clear();
}

/**
 * Obtiene el tamaño actual del caché
 * 
 * @returns Número de entradas en el caché
 */
export function getCacheSize(): number {
  return cache.size;
}

/**
 * Genera una clave de caché a partir de parámetros
 * 
 * @param prefix - Prefijo de la clave (ej: 'mindmap', 'summary')
 * @param params - Objeto con parámetros
 * @returns Clave de caché única
 */
export function generateCacheKey(prefix: string, params: Record<string, any>): string {
  const sortedParams = Object.keys(params)
    .sort()
    .map(key => `${key}:${JSON.stringify(params[key])}`)
    .join('|');
  
  return `${prefix}:${sortedParams}`;
}

/**
 * Ejecuta una función con caché automático
 * 
 * @param key - Clave del caché
 * @param fn - Función a ejecutar si no hay caché
 * @param ttl - Tiempo de vida del caché (opcional)
 * @returns Resultado (desde caché o ejecutando la función)
 */
export async function withCache<T>(
  key: string,
  fn: () => Promise<T>,
  ttl: number = DEFAULT_TTL
): Promise<T> {
  // Intentar obtener del caché
  const cached = getCached<T>(key, ttl);
  if (cached !== null) {
    return cached;
  }
  
  // Ejecutar función y cachear resultado
  const result = await fn();
  setCache(key, result);
  
  return result;
}
