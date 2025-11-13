
import React, { useState } from 'react';
import { generateStudyPlan } from '../services/geminiService';
import { StudyPlanInput } from '../types';
import { SparkIcon } from './icons/SparkIcon';

const StudyPlanView: React.FC = () => {
    const [inputs, setInputs] = useState<StudyPlanInput>({
        availability: 'Lunes a viernes por la tarde (4 horas) y sábados por la mañana (5 horas).',
        duration: 'semanal',
        includeTracking: true,
        includeSuggestions: true,
    });
    const [plan, setPlan] = useState<string>('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleGenerate = async () => {
        setIsLoading(true);
        setError(null);
        setPlan('');
        try {
            const result = await generateStudyPlan(inputs);
            setPlan(result);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full bg-white dark:bg-slate-900">
            <header className="p-4 border-b border-slate-200 dark:border-slate-800">
                <h1 className="text-xl font-bold text-slate-800 dark:text-slate-100">Plan de Estudios Personalizado</h1>
                <p className="text-sm text-slate-500 dark:text-slate-400">Crea un plan de estudio a tu medida con la ayuda de la IA.</p>
            </header>
            
            <div className="flex-1 grid grid-cols-1 md:grid-cols-3 overflow-hidden">
                <aside className="col-span-1 md:border-r border-slate-200 dark:border-slate-800 p-6 flex flex-col gap-6 bg-slate-50 dark:bg-slate-900/50 overflow-y-auto">
                    <h2 className="text-lg font-semibold">Configura tu Plan</h2>
                    <div>
                        <label htmlFor="availability" className="block text-sm font-medium mb-1">Tu disponibilidad</label>
                        <textarea
                            id="availability"
                            rows={4}
                            value={inputs.availability}
                            onChange={(e) => setInputs(prev => ({ ...prev, availability: e.target.value }))}
                            className="w-full p-2 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-md text-sm"
                        />
                    </div>
                    <div>
                        <label htmlFor="duration" className="block text-sm font-medium mb-1">Duración del plan</label>
                        <select
                            id="duration"
                            value={inputs.duration}
                            onChange={(e) => setInputs(prev => ({ ...prev, duration: e.target.value as any }))}
                             className="w-full p-2 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-md text-sm"
                        >
                            <option value="semanal">Semanal</option>
                            <option value="mensual">Mensual</option>
                            <option value="trimestral">Trimestral</option>
                        </select>
                    </div>
                    <div className="space-y-3">
                       <label className="flex items-center gap-2 text-sm">
                           <input type="checkbox" checked={inputs.includeTracking} onChange={(e) => setInputs(prev => ({...prev, includeTracking: e.target.checked}))} className="rounded"/>
                           Incluir seguimiento de tareas
                       </label>
                       <label className="flex items-center gap-2 text-sm">
                           <input type="checkbox" checked={inputs.includeSuggestions} onChange={(e) => setInputs(prev => ({...prev, includeSuggestions: e.target.checked}))} className="rounded"/>
                           Recibir sugerencias de la IA
                       </label>
                    </div>
                    <button onClick={handleGenerate} disabled={isLoading} className="w-full mt-auto px-4 py-2 bg-blue-500 text-white rounded-lg font-semibold hover:bg-blue-600 disabled:bg-slate-400 flex items-center justify-center gap-2">
                        {isLoading ? <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div> : <SparkIcon className="w-5 h-5"/>}
                        <span>Generar Plan</span>
                    </button>
                </aside>

                <main className="col-span-2 p-6 lg:p-8 overflow-y-auto">
                    {error && <div className="text-red-500 bg-red-100 dark:bg-red-900 p-4 rounded-lg">{error}</div>}
                    <h2 className="text-lg font-semibold mb-4">Plan Generado</h2>
                    <textarea 
                        value={isLoading ? "Generando tu plan..." : plan}
                        readOnly={isLoading}
                        onChange={(e) => setPlan(e.target.value)}
                        placeholder="Aquí aparecerá tu plan de estudio editable..."
                        className="w-full h-full min-h-[500px] p-4 bg-slate-50 dark:bg-slate-800/50 rounded-lg text-sm font-mono leading-relaxed focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </main>
            </div>
        </div>
    );
};

export default StudyPlanView;
