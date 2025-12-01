import { createContext, useContext } from 'react';

export interface ModelContextValue {
  selectedModel: string;
  setSelectedModel: (model: string) => void;
}

const ModelContext = createContext<ModelContextValue | undefined>(undefined);

export const ModelProvider = ModelContext.Provider;

export function useModel(): ModelContextValue {
  const ctx = useContext(ModelContext);
  if (!ctx) {
    throw new Error('useModel must be used within a ModelProvider');
  }
  return ctx;
}
