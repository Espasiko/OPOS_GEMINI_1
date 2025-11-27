/**
 * ErrorMessage Component - Sprint 10
 *
 * Componente reutilizable para mostrar mensajes de error
 */

import React from 'react';

interface ErrorMessageProps {
  error: string;
  onRetry?: () => void;
}

/**
 * Componente para mostrar mensajes de error con opción de reintentar
 *
 * @param error - Mensaje de error a mostrar
 * @param onRetry - Función opcional para reintentar la operación
 */
export function ErrorMessage({ error, onRetry }: ErrorMessageProps) {
  return (
    <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
      <div className="flex items-start gap-3">
        <svg
          className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <div className="flex-1">
          <p className="text-red-700 dark:text-red-300">{error}</p>
          {onRetry && (
            <button
              onClick={onRetry}
              className="mt-2 text-sm text-red-600 dark:text-red-400 underline hover:text-red-800 dark:hover:text-red-200 transition-colors"
            >
              Reintentar
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default ErrorMessage;
