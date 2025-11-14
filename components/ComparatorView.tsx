import React, { useState } from 'react';
import { compareLawVersions, getTextFromUrl } from '../services/geminiService';
import { CompareIcon } from './icons/CompareIcon';
import InputSourceSelector, { extractTextFromFile } from './InputSourceSelector';

interface ComparatorViewProps {
    savedComparison: string;
    setSavedComparison: (comparison: string) => void;
}

const ComparatorView: React.FC<ComparatorViewProps> = ({ savedComparison, setSavedComparison }) => {
    // FIX: Use local state for input texts to avoid storing large data in localStorage.
    const [textA, setTextA] = useState('');
    const [textB, setTextB] = useState('');
    const [comparison, setComparison] = useState(savedComparison);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [errorA, setErrorA] = useState<string | null>(null);
    const [errorB, setErrorB] = useState<string | null>(null);

    const handleGenerate = async () => {
        if (!textA.trim() || !textB.trim()) return;
        setIsLoading(true);
        setError(null);
        setComparison('');
        try {
            const result = await compareLawVersions(textA, textB);
            setComparison(result);
            // FIX: Persist only the comparison result, not the input texts.
            setSavedComparison(result);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };
    
    const handleDataSourceSubmit = async (
        target: 'A' | 'B', 
        source: { type: 'text'; content: string } | { type: 'file'; content: File } | { type: 'url', content: string }
    ) => {
        setIsLoading(true); 
        const setErrorState = target === 'A' ? setErrorA : setErrorB;
        const setTextState = target === 'A' ? setTextA : setTextB;
        
        setErrorState(null);
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
            setTextState(sourceText);
        } catch(err: any) {
            setErrorState(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full bg-white dark:bg-slate-900">
            <header className="p-4 border-b border-slate-200 dark:border-slate-800">
                <h1 className="text-xl font-bold text-slate-800 dark:text-slate-100">Comparador de Leyes</h1>
                <p className="text-sm text-slate-500 dark:text-slate-400">Carga dos versiones de un texto legal para que la IA resalte las diferencias.</p>
            </header>
            
             <div className="flex-1 grid grid-cols-1 xl:grid-cols-2 gap-2 p-4 overflow-hidden">
                <div className="flex flex-col gap-4 overflow-y-auto pr-2">
                     <div className="flex flex-col">
                        <h2 className="text-lg font-semibold mb-2 p-2">Texto A (Versión Antigua)</h2>
                         <InputSourceSelector
                            onTextSubmit={(source) => handleDataSourceSubmit('A', source)}
                            isLoading={isLoading}
                            error={errorA}
                            initialText={textA}
                            showTextField={true}
                            textAreaRows={10}
                        />
                    </div>
                    <div className="flex flex-col">
                        <h2 className="text-lg font-semibold mb-2 p-2">Texto B (Versión Nueva)</h2>
                        <InputSourceSelector
                            onTextSubmit={(source) => handleDataSourceSubmit('B', source)}
                            isLoading={isLoading}
                            error={errorB}
                            initialText={textB}
                            showTextField={true}
                            textAreaRows={10}
                        />
                    </div>
                </div>
                
                <div className="flex flex-col overflow-y-auto xl:border-l border-slate-200 dark:border-slate-800 p-4">
                    <button onClick={handleGenerate} disabled={isLoading || !textA.trim() || !textB.trim()} className="mb-4 w-full px-4 py-2 bg-blue-500 text-white rounded-lg font-semibold hover:bg-blue-600 disabled:bg-slate-400 flex items-center justify-center gap-2">
                        {isLoading ? <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div> : <CompareIcon className="w-5 h-5"/>}
                        <span>{isLoading ? 'Analizando...' : 'Comparar Versiones'}</span>
                    </button>
                    <h2 className="text-lg font-semibold mb-2">Análisis de Diferencias</h2>
                    <div className="flex-grow p-4 bg-slate-50 dark:bg-slate-800/50 rounded-lg">
                        {isLoading && (
                            <div className="flex flex-col items-center justify-center h-full text-center">
                                <CompareIcon className="w-12 h-12 text-blue-500 animate-pulse" />
                                <p className="mt-4 font-semibold">Buscando cambios, adiciones y eliminaciones...</p>
                            </div>
                        )}
                        {error && <div className="text-red-500 text-center p-4"><strong>Error:</strong> {error}</div>}
                        {comparison && (
                            <div className="prose prose-slate dark:prose-invert max-w-none whitespace-pre-wrap animate-fade-in" dangerouslySetInnerHTML={{ __html: comparison.replace(/\n/g, '<br />') }}></div>
                        )}
                        {!isLoading && !comparison && !error && (
                            <div className="flex items-center justify-center h-full text-slate-500">
                                <p>El análisis de las diferencias aparecerá aquí.</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ComparatorView;
