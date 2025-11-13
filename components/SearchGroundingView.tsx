import React, { useState } from 'react';
import { searchWithGrounding } from '../services/geminiService';
import { GroundingSource } from '../types';
import { SearchIcon } from './icons/SearchIcon';

const SearchGroundingView: React.FC = () => {
  const [query, setQuery] = useState('');
  const [untilDate, setUntilDate] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<{ text: string; sources: GroundingSource[] } | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || isLoading) return;

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const searchResult = await searchWithGrounding(query, untilDate);
      setResult(searchResult);
    } catch (err: any) {
      setError(err.message || 'An unknown error occurred.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white dark:bg-slate-900">
      <header className="p-4 border-b border-slate-200 dark:border-slate-800">
        <h1 className="text-xl font-bold text-slate-800 dark:text-slate-100">Búsqueda Actualizada</h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">Obtén respuestas basadas en información reciente de la web, con la posibilidad de filtrar por fecha.</p>
      </header>
      
      <div className="flex-1 overflow-y-auto p-6 lg:p-8">
        <div className="max-w-4xl mx-auto">
          <form onSubmit={handleSearch} className="mb-8 space-y-4">
            <div className="relative">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ej: ¿Cuál es la base de cotización máxima para 2024?"
                disabled={isLoading}
                className="w-full px-5 py-3 pr-14 text-lg bg-slate-100 dark:bg-slate-800 border-2 border-transparent rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 dark:text-white transition-all"
              />
              <button
                type="submit"
                disabled={isLoading || !query.trim()}
                className="absolute right-3 top-1/2 -translate-y-1/2 w-10 h-10 flex items-center justify-center bg-blue-500 text-white rounded-full disabled:bg-slate-400 dark:disabled:bg-slate-600 hover:bg-blue-600 transition-colors"
              >
                  {isLoading ? (
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  ) : (
                      <SearchIcon className="w-5 h-5"/>
                  )}
              </button>
            </div>
            <div className="flex items-center space-x-2 pl-2">
                <label htmlFor="until-date" className="text-sm font-medium text-slate-600 dark:text-slate-300">Limitar búsqueda a legislación vigente hasta:</label>
                <input 
                    type="date"
                    id="until-date"
                    value={untilDate}
                    onChange={(e) => setUntilDate(e.target.value)}
                    className="bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 border border-slate-300 dark:border-slate-600 rounded-md px-2 py-1 text-sm focus:ring-blue-500 focus:border-blue-500"
                />
            </div>
          </form>

          {error && <div className="text-red-500 bg-red-100 dark:bg-red-900 p-4 rounded-lg">{error}</div>}

          {result && (
            <div className="space-y-6 animate-fade-in">
                <div className="p-6 bg-slate-50 dark:bg-slate-800 rounded-xl shadow-sm">
                    <h2 className="text-xl font-semibold text-slate-800 dark:text-slate-100 mb-4">Respuesta</h2>
                    <div className="prose prose-slate dark:prose-invert max-w-none whitespace-pre-wrap">{result.text}</div>
                </div>

                {result.sources.length > 0 && (
                     <div className="p-6 bg-green-50 dark:bg-green-900/40 rounded-xl">
                        <h3 className="text-lg font-semibold text-green-800 dark:text-green-200 mb-3">Fuentes</h3>
                        <ul className="space-y-2">
                            {result.sources.map((source, index) => (
                                <li key={index} className="flex items-start space-x-2">
                                    <span className="text-green-600 dark:text-green-400 mt-1">&#10003;</span>
                                    <a 
                                      href={source.uri} 
                                      target="_blank" 
                                      rel="noopener noreferrer" 
                                      className="text-green-700 dark:text-green-300 hover:underline hover:text-green-600 dark:hover:text-green-200 transition-colors"
                                    >
                                        {source.title}
                                    </a>
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SearchGroundingView;