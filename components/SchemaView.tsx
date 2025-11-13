import React, { useState, useEffect } from 'react';
import { generateSchema } from '../services/geminiService';
import { SparkIcon } from './icons/SparkIcon';
import { SchemaIcon } from './icons/SchemaIcon';

interface SchemaViewProps {
    savedState: { topic: string; schema: string };
    setSavedState: React.Dispatch<React.SetStateAction<{ topic: string; schema: string }>>;
}

// Simple Markdown to HTML list parser
const parseSchemaToHtml = (markdown: string): string => {
    const lines = markdown.split('\n');
    let html = '<ul>';
    let level = 0;

    for (const line of lines) {
        if (!line.trim()) continue;
        
        const trimmedLine = line.trim();
        const currentLevel = (line.match(/^\s*\*/) || [''])[0].length - 1;
        const content = trimmedLine.substring(1).trim();

        if (currentLevel > level) {
            html += '<ul>'.repeat(currentLevel - level);
        } else if (currentLevel < level) {
            html += '</ul>'.repeat(level - currentLevel);
        }
        
        html += `<li>${content}</li>`;
        level = currentLevel;
    }

    html += '</ul>'.repeat(level + 1);
    return html;
};


const SchemaView: React.FC<SchemaViewProps> = ({ savedState, setSavedState }) => {
    const [topic, setTopic] = useState(savedState.topic);
    const [schema, setSchema] = useState(savedState.schema);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        setSavedState({ topic, schema });
    }, [topic, schema, setSavedState]);

    const handleGenerate = async () => {
        if (!topic.trim()) return;
        setIsLoading(true);
        setError(null);
        setSchema('');
        try {
            const result = await generateSchema(topic);
            setSchema(result);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full bg-white dark:bg-slate-900">
            <header className="p-4 border-b border-slate-200 dark:border-slate-800">
                <h1 className="text-xl font-bold text-slate-800 dark:text-slate-100">Generador de Esquemas</h1>
                <p className="text-sm text-slate-500 dark:text-slate-400">Introduce un tema del temario y la IA creará un esquema detallado.</p>
            </header>
            
            <div className="flex-1 overflow-y-auto p-6 lg:p-8">
                <div className="max-w-4xl mx-auto">
                    <div className="flex gap-4 mb-8">
                        <input
                            type="text"
                            value={topic}
                            onChange={(e) => setTopic(e.target.value)}
                            placeholder="Ej: El procedimiento administrativo común"
                            className="flex-grow px-4 py-2 bg-slate-100 dark:bg-slate-800 border-2 border-transparent rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:text-white"
                        />
                        <button onClick={handleGenerate} disabled={isLoading || !topic.trim()} className="px-4 py-2 bg-blue-500 text-white rounded-lg font-semibold hover:bg-blue-600 disabled:bg-slate-400 flex items-center gap-2">
                           {isLoading ? <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div> : <SparkIcon className="w-5 h-5"/>}
                           <span>{isLoading ? 'Generando...' : 'Generar Esquema'}</span>
                        </button>
                    </div>

                    {error && <div className="text-red-500 bg-red-100 dark:bg-red-900 p-4 rounded-lg">{error}</div>}

                    <div className="p-6 bg-slate-50 dark:bg-slate-800/50 rounded-xl shadow-sm min-h-[400px]">
                        {isLoading && (
                            <div className="flex flex-col items-center justify-center h-full text-center">
                                <SchemaIcon className="w-12 h-12 text-blue-500 animate-pulse" />
                                <p className="mt-4 font-semibold">Estructurando el conocimiento...</p>
                            </div>
                        )}
                         {schema && (
                            <div 
                                className="prose prose-slate dark:prose-invert max-w-none animate-fade-in prose-ul:list-disc prose-li:my-1" 
                                dangerouslySetInnerHTML={{ __html: parseSchemaToHtml(schema) }}
                            ></div>
                        )}
                        {!isLoading && !schema && (
                            <div className="flex items-center justify-center h-full text-slate-500">
                                <p>El esquema generado aparecerá aquí.</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SchemaView;