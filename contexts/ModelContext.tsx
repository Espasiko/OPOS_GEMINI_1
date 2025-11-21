import React, { createContext, useContext } from 'react';

interface ModelContextType {
  selectedModel: string;
  setSelectedModel: () => void;
}

const ModelContext = createContext<ModelContextType | undefined>(undefined);

export const ModelProvider: React.FC<{
  value: ModelContextType;
  children: React.ReactNode;
}> = ({ value, children }) => {
  return <ModelContext.Provider value={value}>{children}</ModelContext.Provider>;
};

export const useModel = () => {
  const context = useContext(ModelContext);
  if (!context) {
    throw new Error('useModel must be used within ModelProvider');
  }
  return context;
};
