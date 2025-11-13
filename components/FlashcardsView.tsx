import React, { useState } from 'react';
import { generateFlashcardsAndMeme } from '../services/geminiService';
import { Flashcard } from '../types';
import { SparkIcon } from './icons/SparkIcon';
import { FlashcardIcon } from './icons/FlashcardIcon';

const FlashcardComponent: React.FC<{ card: Flashcard }> = ({ card }) => {
    const [isFlipped, setIsFlipped] = useState(false);
    return (
        <div className="w-full h-48 perspective" onClick={() => setIsFlipped(!isFlipped)}>
            <div className={`relative w-full h-full transform-style-3d transition-transform duration-500 ${isFlipped ? 'rotate-y-180' : ''}`}>
                <div className="absolute w-full h-full backface-hidden flex items-center justify-center p-4 bg-white dark:bg-slate-700 rounded-lg shadow-lg text-center font-semibold">
                    {card.front}
                </div>
                <div className="absolute w-full h-full backface-hidden rotate-y-180 flex items-center justify-center p-4 bg-blue-100 dark:bg-blue-900 rounded-lg shadow-lg text-center">
                    {card.back}
                </div>
            </div>
        </div>
    );
};


const FlashcardsView: React.FC = () => {
    const [topic, setTopic] = useState('');
    const [flashcards, setFlashcards] = useState<Flashcard[]>([]);
    const [meme, setMeme] = useState<{ imageUrl: string; prompt: string } | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleGenerate = async () => {
        if (!topic.trim()) return;
        setIsLoading(true);
        setError(null);
        setFlashcards([]);
        setMeme(null);
        try {
            const result = await generateFlashcardsAndMeme(topic);
            setFlashcards(result.flashcards);
            setMeme(result.meme);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full bg-white dark:bg-slate-900">
            <header className="p-4 border-b border-slate-200 dark:border-slate-800">
                <h1 className="text-xl font-bold text-slate-800 dark:text-slate-100">Tarjetas y Memes para Estudiar</h1>
                <p className="text-sm text-slate-500 dark:text-slate-400">Memoriza conceptos clave de forma rápida y divertida.</p>
            </header>
            
            <div className="flex-1 overflow-y-auto p-6 lg:p-8">
                <div className="max-w-6xl mx-auto">
                    <div className="flex gap-4 mb-8">
                        <input
                            type="text"
                            value={topic}
                            onChange={(e) => setTopic(e.target.value)}
                            placeholder="Ej: El silencio administrativo"
                            className="flex-grow px-4 py-2 bg-slate-100 dark:bg-slate-800 border-2 border-transparent rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:text-white"
                        />
                        <button onClick={handleGenerate} disabled={isLoading || !topic.trim()} className="px-4 py-2 bg-blue-500 text-white rounded-lg font-semibold hover:bg-blue-600 disabled:bg-slate-400 flex items-center gap-2">
                           {isLoading ? <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div> : <SparkIcon className="w-5 h-5"/>}
                           <span>{isLoading ? 'Creando...' : 'Generar'}</span>
                        </button>
                    </div>

                    {error && <div className="text-red-500 bg-red-100 dark:bg-red-900 p-4 rounded-lg text-center">{error}</div>}

                    {isLoading && (
                        <div className="text-center">
                           <FlashcardIcon className="w-16 h-16 text-blue-500 animate-pulse mx-auto" />
                           <h2 className="mt-4 text-xl font-semibold">Creando material de estudio...</h2>
                           <p className="mt-2 text-slate-500">Esto puede tardar unos segundos, especialmente la generación del meme.</p>
                       </div>
                    )}
                    
                    {!isLoading && flashcards.length === 0 && !error && (
                         <div className="text-center text-slate-500">
                            <p>Introduce un tema para generar tarjetas de memoria y un meme.</p>
                         </div>
                    )}

                    {flashcards.length > 0 && (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            <div className="lg:col-span-2">
                                <h2 className="text-2xl font-bold mb-4">Tarjetas de Memoria</h2>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    {flashcards.map(card => (
                                        <FlashcardComponent key={card.id} card={card} />
                                    ))}
                                </div>
                            </div>
                            {meme && (
                                <div className="lg:col-span-1">
                                    <h2 className="text-2xl font-bold mb-4">Meme para Recordar</h2>
                                    <div className="bg-slate-100 dark:bg-slate-800 rounded-lg p-4 shadow-lg">
                                        <img src={meme.imageUrl} alt="Meme generado por IA" className="w-full h-auto rounded-md object-cover" />
                                        <p className="text-xs italic text-slate-500 mt-2 text-center">{meme.prompt}</p>
                                    </div>
                                </div>
                            )}
                        </div>
                    )}

                </div>
            </div>
            <style>{`
                .perspective { perspective: 1000px; }
                .transform-style-3d { transform-style: preserve-3d; }
                .rotate-y-180 { transform: rotateY(180deg); }
                .backface-hidden { backface-visibility: hidden; -webkit-backface-visibility: hidden; }
            `}</style>
        </div>
    );
};

export default FlashcardsView;
