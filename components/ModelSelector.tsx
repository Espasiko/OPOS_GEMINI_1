import React, { useState, useEffect } from 'react';
import { getProviders } from '../services/backendService';

interface Provider {
  id: string;
  provider: string;
  model: string;
  speed: string;
  cost: string;
  configured: boolean;
}

interface ModelSelectorProps {
  value: string;
  // eslint-disable-next-line no-unused-vars
  onChange: (value: string) => void;
}

const SPEED_EMOJI = {
  ultra: '⚡',
  fast: '🚀',
  medium: '🏃',
  slow: '🐌',
};

const COST_EMOJI = {
  free: '🆓',
  cheap: '💰',
  medium: '💵',
  expensive: '💸',
};

const ModelSelector: React.FC<ModelSelectorProps> = ({ value, onChange }) => {
  const [providers, setProviders] = useState<Provider[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProviders();
  }, []);

  const loadProviders = async () => {
    try {
      const data = await getProviders();
      setProviders(data.providers);
    } catch (error) {
      console.error('Error loading providers:', error);
    } finally {
      setLoading(false);
    }
  };

  const selectedProvider = providers.find((p) => p.id === value);

  return (
    <div className="flex items-center gap-2">
      <label htmlFor="model-selector" className="text-sm font-medium text-slate-700 dark:text-slate-300">
        Modelo:
      </label>
      <select
        id="model-selector"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={loading}
        className="px-3 py-1.5 text-sm border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
      >
        {loading ? (
          <option>Cargando...</option>
        ) : (
          <>
            <optgroup label="⚡ Ultra Rápido + Gratis">
              {providers
                .filter((p) => p.provider === 'groq')
                .map((p) => (
                  <option key={p.id} value={p.id} disabled={!p.configured}>
                    {SPEED_EMOJI[p.speed as keyof typeof SPEED_EMOJI]} {p.model}
                    {!p.configured && ' (No configurado)'}
                  </option>
                ))}
            </optgroup>
            <optgroup label="💰 Barato + Potente">
              {providers
                .filter((p) => p.provider === 'deepseek')
                .map((p) => (
                  <option key={p.id} value={p.id} disabled={!p.configured}>
                    {SPEED_EMOJI[p.speed as keyof typeof SPEED_EMOJI]} {p.model}
                    {!p.configured && ' (No configurado)'}
                  </option>
                ))}
            </optgroup>
            <optgroup label="🌟 Google Gemini">
              {providers
                .filter((p) => p.provider === 'gemini')
                .map((p) => (
                  <option key={p.id} value={p.id} disabled={!p.configured}>
                    {SPEED_EMOJI[p.speed as keyof typeof SPEED_EMOJI]}{' '}
                    {COST_EMOJI[p.cost as keyof typeof COST_EMOJI]} {p.model}
                    {!p.configured && ' (No configurado)'}
                  </option>
                ))}
            </optgroup>
            <optgroup label="🔮 Mistral AI">
              {providers
                .filter((p) => p.provider === 'mistral')
                .map((p) => (
                  <option key={p.id} value={p.id} disabled={!p.configured}>
                    {SPEED_EMOJI[p.speed as keyof typeof SPEED_EMOJI]}{' '}
                    {COST_EMOJI[p.cost as keyof typeof COST_EMOJI]} {p.model}
                    {!p.configured && ' (No configurado)'}
                  </option>
                ))}
            </optgroup>
            <optgroup label="🤗 Hugging Face">
              {providers
                .filter((p) => p.provider === 'huggingface')
                .map((p) => (
                  <option key={p.id} value={p.id} disabled={!p.configured}>
                    {SPEED_EMOJI[p.speed as keyof typeof SPEED_EMOJI]}{' '}
                    {COST_EMOJI[p.cost as keyof typeof COST_EMOJI]} {p.model}
                    {!p.configured && ' (No configurado)'}
                  </option>
                ))}
            </optgroup>
            <optgroup label="🔷 Cohere">
              {providers
                .filter((p) => p.provider === 'cohere')
                .map((p) => (
                  <option key={p.id} value={p.id} disabled={!p.configured}>
                    {SPEED_EMOJI[p.speed as keyof typeof SPEED_EMOJI]}{' '}
                    {COST_EMOJI[p.cost as keyof typeof COST_EMOJI]} {p.model}
                    {!p.configured && ' (No configurado)'}
                  </option>
                ))}
            </optgroup>
            <optgroup label="🐌 Lento pero Gratis">
              {providers
                .filter((p) => p.provider === 'mistral-vps')
                .map((p) => (
                  <option key={p.id} value={p.id}>
                    {SPEED_EMOJI[p.speed as keyof typeof SPEED_EMOJI]} {p.model}
                  </option>
                ))}
            </optgroup>
          </>
        )}
      </select>
      {selectedProvider && (
        <span className="text-xs text-slate-500 dark:text-slate-400">
          {SPEED_EMOJI[selectedProvider.speed as keyof typeof SPEED_EMOJI]}{' '}
          {COST_EMOJI[selectedProvider.cost as keyof typeof COST_EMOJI]}
        </span>
      )}
    </div>
  );
};

export default ModelSelector;
