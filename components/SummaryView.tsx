import React, { useState } from 'react';
import { generateSummary, getTextFromUrl } from '../services/geminiService';
import { SummaryIcon } from './icons/SummaryIcon';
import InputSourceSelector, { extractTextFromFile } from './InputSourceSelector';

interface SummaryViewProps {
    savedSummary: string;
    setSavedSummary: (summary: string) => void;
}

const SummaryView: React.FC<SummaryViewProps> = ({ savedSummary, setSavedSummary }) => {
    // FIX: Use local state for the input text to avoid storing large data in localStorage.
    const [text, setText] = useState('');
    const [summary, setSummary] = useState(savedSummary);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleGenerate = async (sourceText: string) => {
        if (!sourceText.trim()) return;
        setIsLoading(true);
        setError(null);
        setSummary('');
        try {
            const result = await generateSummary(sourceText);
            setSummary(result);
            // FIX: Persist only the summary result, not the input text.
            setSavedSummary(result);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };
    
    const handleDataSourceSubmit = async (source: { type: 'text'; content: string } | { type: 'file'; content: File } | { type: 'url'; content: string }) => {
        setIsLoading(true);
        setError(null);
        let sourceText = '';
        try {
            switch (source.type) {
                case 'text':
                    sourceText = source.content;
                    break;
                case 'file':
                    sourceText = await extractTextFromFile(source.content);
                    break;
                case 'url':
                    sourceText = await getTextFromUrl(source.content);
                    break;
            }
            setText(sourceText);
            await handleGenerate(sourceText);
        } catch(err: any) {
            setError(err.message);
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full bg-white dark:bg-slate-900">
            <header className="p-4 border-b border-slate-200 dark:border-slate-800">
                <h1 className="text-xl font-bold text-slate-800 dark:text-slate-100">Generador de Resúmenes</h1>
                <p className="text-sm text-slate-500 dark:text-slate-400">Pega un texto legal, sube un archivo o introduce una URL y la IA extraerá las ideas clave.</p>
            </header>
            
            <div className="flex-1 grid grid-cols-1 md:grid-cols-2 gap-6 p-6 lg:p-8 overflow-hidden">
                <div className="flex flex-col">
                    <h2 className="text-lg font-semibold mb-2">Fuente del Texto</h2>
                    <InputSourceSelector
                        onTextSubmit={handleDataSourceSubmit}
                        isLoading={isLoading}
                        error={error}
                        initialText={text}
                        showTextField={true}
                    />
                </div>
                
                <div className="flex flex-col overflow-y-auto">
                    <h2 className="text-lg font-semibold mb-2">Resumen Generado</h2>
                    <div className="flex-grow p-4 bg-slate-50 dark:bg-slate-800/50 rounded-lg">
                        {isLoading && (
                            <div className="flex flex-col items-center justify-center h-full text-center">
                                <SummaryIcon className="w-12 h-12 text-blue-500 animate-pulse" />
                                <p className="mt-4 font-semibold">Sintetizando información...</p>
                                <p className="mt-1 text-sm text-slate-500">Si el texto es muy largo, puede tardar un poco.</p>
                            </div>
                        )}
                        {summary && (
                            <div className="prose prose-slate dark:prose-invert max-w-none whitespace-pre-wrap animate-fade-in" dangerouslySetInnerHTML={{ __html: summary.replace(/\n/g, '<br />') }}></div>
                        )}
                        {!isLoading && !summary && !error && (
                            <div className="flex items-center justify-center h-full text-slate-500">
                                <p>El resumen aparecerá aquí.</p>
                            </div>
                        )}
                         {error && !isLoading && (
                            <div className="flex items-center justify-center h-full text-red-500 p-4 text-center">
                                <p><strong>Error:</strong> {error}</p>
                            </div>
                         )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SummaryView;