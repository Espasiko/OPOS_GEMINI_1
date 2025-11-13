import React, { useState, useCallback, useMemo, useRef, useEffect } from 'react';
import { generateMindMap } from '../services/geminiService';
import { MindMapNode } from '../types';
import { SparkIcon } from './icons/SparkIcon';
import { DownloadIcon } from './icons/DownloadIcon';
import * as htmlToImage from 'html-to-image';

interface MindMapViewProps {
    savedState: { topic: string; map: MindMapNode | null };
    setSavedState: React.Dispatch<React.SetStateAction<{ topic: string; map: MindMapNode | null }>>;
}

const MindMapView: React.FC<MindMapViewProps> = ({ savedState, setSavedState }) => {
    // The library is loaded from CDN, so we access it from the window object inside the component
    // to ensure the script has loaded before we try to access it. This prevents a race condition.
    const ForceGraph2D = (window as any).ForceGraph2D?.default;

    const [topic, setTopic] = useState(savedState.topic);
    const [mindMap, setMindMap] = useState<MindMapNode | null>(savedState.map);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    // FIX: The error "Expected 1 arguments, but got 0" likely refers to this useRef call.
    // Providing an explicit `null` initial value resolves the issue.
    const fgRef = useRef<any>(null);
    const graphContainerRef = useRef<HTMLDivElement>(null);

     useEffect(() => {
        setSavedState({ topic, map: mindMap });
    }, [topic, mindMap, setSavedState]);

    const graphData = useMemo(() => {
        if (!mindMap) return { nodes: [], links: [] };
    
        const nodes: any[] = [];
        const links: any[] = [];
    
        const traverse = (node: MindMapNode, parent: MindMapNode | null) => {
          nodes.push({ id: node.id, name: node.text, val: parent ? 1 : 10 }); // Root node is bigger
          if (parent) {
            links.push({ source: parent.id, target: node.id });
          }
          node.children.forEach(child => traverse(child, node));
        };
    
        traverse(mindMap, null);
        return { nodes, links };
      }, [mindMap]);
    
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
    
    const handleNodeDoubleClick = useCallback((node: any) => {
        const newText = prompt("Edita el texto del nodo:", node.name);
        if (newText !== null && newText.trim() !== '') {
          setMindMap(prevMap => {
            if (!prevMap) return null;
            const updateRecursively = (n: MindMapNode): MindMapNode => {
              if (n.id === node.id) {
                return { ...n, text: newText };
              }
              return { ...n, children: n.children.map(child => updateRecursively(child)) };
            };
            return updateRecursively(prevMap);
          });
        }
    }, []);

    const nodeCanvasObject = useCallback((node: any, ctx: CanvasRenderingContext2D, globalScale: number) => {
        const label = node.name;
        const fontSize = 14 / globalScale;
        ctx.font = `600 ${fontSize}px Inter, sans-serif`;
        const textWidth = ctx.measureText(label).width;
        const bgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.6);

        ctx.fillStyle = node.id === 'root' ? 'rgba(30, 64, 175, 1)' : 'rgba(45, 55, 72, 0.95)';
        ctx.beginPath();
        ctx.roundRect(node.x - bgDimensions[0] / 2, node.y - bgDimensions[1] / 2, bgDimensions[0], bgDimensions[1], 5 / globalScale);
        ctx.fill();
        
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = 'rgba(237, 242, 247, 1)';
        ctx.fillText(label, node.x, node.y);

        node.__bckgDimensions = bgDimensions;
    }, []);
    
    const downloadAs = (format: 'json' | 'md' | 'png') => {
        if (!mindMap) return;
        const filename = `mapa_mental_${topic.replace(/\s+/g, '_').toLowerCase()}`;

        if (format === 'png') {
            if (graphContainerRef.current) {
                htmlToImage.toPng(graphContainerRef.current)
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
                    <p className="text-sm text-slate-500 dark:text-slate-400">Genera mapas mentales interactivos sobre cualquier tema.</p>
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
                    
                    <div ref={graphContainerRef} className="w-full flex-grow bg-slate-100 dark:bg-slate-800/50 rounded-xl shadow-inner flex items-center justify-center relative min-h-[400px]">
                        {isLoading ? (
                            <div className="text-center">
                                <SparkIcon className="w-12 h-12 text-blue-500 animate-pulse mx-auto"/>
                                <p className="mt-2 font-semibold">Creando estructura de ideas...</p>
                            </div>
                        ) : mindMap && ForceGraph2D ? (
                            <ForceGraph2D
                                ref={fgRef}
                                graphData={graphData}
                                onNodeDragEnd={(node: any) => { node.fx = node.x; node.fy = node.y; }}
                                onNodeDoubleClick={handleNodeDoubleClick}
                                nodeCanvasObject={nodeCanvasObject}
                                linkColor={() => 'rgba(100, 116, 139, 0.5)'}
                                linkWidth={1.5}
                                backgroundColor="rgba(0,0,0,0)"
                            />
                        ) : (
                             <p className="text-slate-500">Genera un mapa para visualizarlo aquí.</p>
                        )}
                    </div>
                     <p className="text-xs text-center text-slate-500 mt-2">Doble clic en un nodo para editar. Arrastra los nodos para organizar. Usa la rueda del ratón para hacer zoom.</p>
                </div>
            </div>
        </div>
    );
};

export default MindMapView;