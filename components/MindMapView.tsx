import React, { useState, useCallback, useRef, useEffect } from 'react';
import { generateMindMap } from '../services/geminiService';
import { MindMapNode } from '../types';
import { SparkIcon } from './icons/SparkIcon';
import { DownloadIcon } from './icons/DownloadIcon';
import * as htmlToImage from 'html-to-image';

interface MindMapViewProps {
    savedState: { topic: string; map: MindMapNode | null };
    setSavedState: React.Dispatch<React.SetStateAction<{ topic: string; map: MindMapNode | null }>>;
}

// Recursive component to render the mind map nodes as a hierarchical HTML list
const RenderNode: React.FC<{ node: MindMapNode; onNodeUpdate: (id: string, newText: string) => void }> = ({ node, onNodeUpdate }) => {
    
    const handleDoubleClick = () => {
        const newText = prompt("Edita el texto del nodo:", node.text);
        if (newText !== null && newText.trim() !== '') {
            onNodeUpdate(node.id, newText);
        }
    };
    
    return (
        <li className="relative pl-8 before:absolute before:left-0 before:top-4 before:w-6 before:h-px before:bg-slate-400 dark:before:bg-slate-600 after:absolute after:left-0 after:top-0 after:bottom-0 after:w-px after:bg-slate-400 dark:after:bg-slate-600 last:after:h-4">
            <div 
                onDoubleClick={handleDoubleClick} 
                className="inline-block px-3 py-1.5 bg-white dark:bg-slate-800 rounded-md shadow-sm border border-slate-200 dark:border-slate-700 cursor-pointer hover:bg-blue-50 dark:hover:bg-slate-700 transition-colors"
            >
                {node.text}
            </div>
            {node.children && node.children.length > 0 && (
                <ul className="pt-4">
                    {node.children.map(child => <RenderNode key={child.id} node={child} onNodeUpdate={onNodeUpdate} />)}
                </ul>
            )}
        </li>
    );
};


const MindMapView: React.FC<MindMapViewProps> = ({ savedState, setSavedState }) => {
    const [topic, setTopic] = useState(savedState.topic);
    const [mindMap, setMindMap] = useState<MindMapNode | null>(savedState.map);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const graphContainerRef = useRef<HTMLDivElement>(null);

     useEffect(() => {
        setSavedState({ topic, map: mindMap });
    }, [topic, mindMap, setSavedState]);

    const handleGenerate = async () => {
        if (!topic.trim()) return;
        setIsLoading(true);
        setError(null);
        setMindMap(null);
        try {
            const map = await generateMindMap(topic);
            setMindMap(map);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    const handleNodeUpdate = useCallback((id: string, newText: string) => {
        setMindMap(prevMap => {
          if (!prevMap) return null;
          const updateRecursively = (n: MindMapNode): MindMapNode => {
            if (n.id === id) {
              return { ...n, text: newText };
            }
            return { ...n, children: n.children.map(child => updateRecursively(child)) };
          };
          return updateRecursively(prevMap);
        });
    }, []);
    
    const downloadAs = (format: 'json' | 'md' | 'png') => {
        if (!mindMap) return;
        const filename = `mapa_mental_${topic.replace(/\s+/g, '_').toLowerCase()}`;

        if (format === 'png') {
            if (graphContainerRef.current) {
                htmlToImage.toPng(graphContainerRef.current, { backgroundColor: '#f8fafc' }) // bg-slate-50
                    .then(dataUrl => {
                        const link = document.createElement('a');
                        link.download = `${filename}.png`;
                        link.href = dataUrl;
                        link.click();
                    })
                    .catch(err => console.error("Error exporting PNG:", err));
            }
            return;
        }

        let dataStr = "";

        if (format === 'json') {
            dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(mindMap, null, 2));
        } else if (format === 'md') {
            const toMarkdown = (node: MindMapNode, level = 0): string => {
                let md = `${'  '.repeat(level)}* ${node.text}\n`;
                node.children.forEach(child => {
                    md += toMarkdown(child, level + 1);
                });
                return md;
            };
            dataStr = "data:text/markdown;charset=utf-8," + encodeURIComponent(toMarkdown(mindMap));
        }

        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", `${filename}.${format}`);
        document.body.appendChild(downloadAnchorNode);
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
    };

    return (
        <div className="flex flex-col h-full bg-white dark:bg-slate-900">
            <header className="p-4 border-b border-slate-200 dark:border-slate-800 flex justify-between items-center">
                <div>
                    <h1 className="text-xl font-bold text-slate-800 dark:text-slate-100">Mapas Mentales con IA</h1>
                    <p className="text-sm text-slate-500 dark:text-slate-400">Genera mapas mentales jerárquicos sobre cualquier tema.</p>
                </div>
                 {mindMap && (
                    <div className="flex items-center gap-2">
                        <div className="relative group">
                             <button className="px-3 py-2 bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-100 rounded-lg font-semibold hover:bg-slate-300 dark:hover:bg-slate-600 flex items-center gap-2">
                                <DownloadIcon className="w-5 h-5"/>
                                <span>Descargar</span>
                             </button>
                             <div className="absolute right-0 mt-2 w-40 bg-white dark:bg-slate-800 rounded-md shadow-lg py-1 z-10 opacity-0 group-hover:opacity-100 transition-opacity invisible group-hover:visible">
                                <a onClick={() => downloadAs('png')} className="block px-4 py-2 text-sm text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-700 cursor-pointer">Como Imagen (.png)</a>
                                <a onClick={() => downloadAs('md')} className="block px-4 py-2 text-sm text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-700 cursor-pointer">Como Markdown (.md)</a>
                                <a onClick={() => downloadAs('json')} className="block px-4 py-2 text-sm text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-700 cursor-pointer">Como JSON (.json)</a>
                             </div>
                        </div>
                    </div>
                 )}
            </header>

            <div className="flex-1 flex flex-col p-6 lg:p-8 overflow-hidden">
                <div className="max-w-6xl mx-auto w-full flex flex-col">
                    <div className="flex gap-4 mb-8">
                        <input
                            type="text"
                            value={topic}
                            onChange={(e) => setTopic(e.target.value)}
                            placeholder="Ej: La Incapacidad Temporal o Artículo 41 CE"
                            className="flex-grow px-4 py-2 bg-slate-100 dark:bg-slate-800 border-2 border-transparent rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:text-white"
                        />
                        <button onClick={handleGenerate} disabled={isLoading || !topic.trim()} className="px-4 py-2 bg-blue-500 text-white rounded-lg font-semibold hover:bg-blue-600 disabled:bg-slate-400 flex items-center gap-2">
                           {isLoading ? <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div> : <SparkIcon className="w-5 h-5"/>}
                           <span>{isLoading ? 'Generando...' : 'Generar'}</span>
                        </button>
                    </div>

                    {error && <div className="text-red-500 bg-red-100 dark:bg-red-900 p-4 rounded-lg">{error}</div>}
                    
                    <div className="w-full flex-grow bg-slate-50 dark:bg-slate-800/50 rounded-xl shadow-inner flex p-8 overflow-auto min-h-[400px]">
                        {isLoading ? (
                            <div className="text-center m-auto">
                                <SparkIcon className="w-12 h-12 text-blue-500 animate-pulse mx-auto"/>
                                <p className="mt-2 font-semibold">Creando estructura de ideas...</p>
                            </div>
                        ) : mindMap ? (
                            <div ref={graphContainerRef} className="p-4">
                                <ul className="list-none">
                                    <RenderNode node={mindMap} onNodeUpdate={handleNodeUpdate}/>
                                </ul>
                            </div>
                        ) : (
                             <p className="text-slate-500 m-auto">Genera un mapa para visualizarlo aquí.</p>
                        )}
                    </div>
                     <p className="text-xs text-center text-slate-500 mt-2">Doble clic en un nodo para editar.</p>
                </div>
            </div>
        </div>
    );
};

export default MindMapView;