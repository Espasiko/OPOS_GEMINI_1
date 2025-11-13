
import React, { useState, useMemo } from 'react';
import { ProgressData } from '../App';

interface ProgressViewProps {
    progressData: ProgressData[];
}

type TimeFilter = 'all' | '7d' | '30d';

const getMotivationalMessage = (percentage: number): { message: string, color: string } => {
    if (isNaN(percentage)) return { message: "¡Completa tu primer caso práctico para empezar a medir tu progreso!", color: "text-slate-500" };
    if (percentage >= 85) return { message: "¡Excelente! Estás en el camino correcto para conseguir tu plaza. ¡Sigue así!", color: "text-green-500" };
    if (percentage >= 70) return { message: "¡Muy buen trabajo! Estás por encima del notable. Un último empujón te acerca a la excelencia.", color: "text-emerald-500" };
    if (percentage >= 50) return { message: "¡Vas por buen camino! Has superado el aprobado. La constancia es la clave ahora.", color: "text-yellow-500" };
    if (percentage >= 30) return { message: "No te desanimes. Cada error es una oportunidad de aprendizaje. ¡Identifica tus fallos y a por ello!", color: "text-orange-500" };
    return { message: "El comienzo siempre es lo más difícil. Analiza las explicaciones y verás cómo mejoras. ¡Mucho ánimo!", color: "text-red-500" };
};

const ProgressView: React.FC<ProgressViewProps> = ({ progressData }) => {
    const [filter, setFilter] = useState<TimeFilter>('all');

    const filteredData = useMemo(() => {
        const now = Date.now();
        if (filter === '7d') {
            const sevenDaysAgo = now - 7 * 24 * 60 * 60 * 1000;
            return progressData.filter(d => d.timestamp >= sevenDaysAgo);
        }
        if (filter === '30d') {
            const thirtyDaysAgo = now - 30 * 24 * 60 * 60 * 1000;
            return progressData.filter(d => d.timestamp >= thirtyDaysAgo);
        }
        return progressData;
    }, [progressData, filter]);

    const totalQuestions = filteredData.length;
    const correctAnswers = filteredData.filter(d => d.isCorrect).length;
    const incorrectAnswers = totalQuestions - correctAnswers;
    const successPercentage = totalQuestions > 0 ? Math.round((correctAnswers / totalQuestions) * 100) : 0;
    
    const motivational = getMotivationalMessage(successPercentage);

    return (
        <div className="flex flex-col h-full bg-white dark:bg-slate-900">
            <header className="p-4 border-b border-slate-200 dark:border-slate-800">
                <h1 className="text-xl font-bold text-slate-800 dark:text-slate-100">Mi Progreso</h1>
                <p className="text-sm text-slate-500 dark:text-slate-400">Analiza tu rendimiento y mantén la motivación alta.</p>
            </header>
            
            <div className="flex-1 overflow-y-auto p-6 lg:p-8">
                <div className="max-w-4xl mx-auto space-y-8">
                    <div className="flex justify-end">
                        <select onChange={(e) => setFilter(e.target.value as TimeFilter)} value={filter} className="bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 border border-slate-300 dark:border-slate-600 rounded-md px-2 py-1 text-sm">
                            <option value="all">Siempre</option>
                            <option value="30d">Últimos 30 días</option>
                            <option value="7d">Últimos 7 días</option>
                        </select>
                    </div>

                    <div className="p-6 bg-slate-50 dark:bg-slate-800/50 rounded-xl shadow-sm text-center">
                        <h2 className="text-lg font-semibold mb-2">Porcentaje de Aciertos</h2>
                        <p className="text-5xl font-bold text-blue-500">{isNaN(successPercentage) ? '-' : `${successPercentage}%`}</p>
                         <p className={`mt-4 font-semibold ${motivational.color}`}>{motivational.message}</p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
                        <div className="p-4 bg-slate-50 dark:bg-slate-800/50 rounded-xl shadow-sm">
                            <h3 className="font-semibold text-slate-600 dark:text-slate-300">Total Respondidas</h3>
                            <p className="text-3xl font-bold mt-2">{totalQuestions}</p>
                        </div>
                         <div className="p-4 bg-green-50 dark:bg-green-900/40 rounded-xl shadow-sm">
                            <h3 className="font-semibold text-green-700 dark:text-green-200">Correctas</h3>
                            <p className="text-3xl font-bold mt-2 text-green-600 dark:text-green-300">{correctAnswers}</p>
                        </div>
                         <div className="p-4 bg-red-50 dark:bg-red-900/40 rounded-xl shadow-sm">
                            <h3 className="font-semibold text-red-700 dark:text-red-200">Incorrectas</h3>
                            <p className="text-3xl font-bold mt-2 text-red-600 dark:text-red-300">{incorrectAnswers}</p>
                        </div>
                    </div>

                    {totalQuestions > 0 && <div className="p-6 bg-slate-50 dark:bg-slate-800/50 rounded-xl shadow-sm">
                        <h3 className="text-lg font-semibold mb-4 text-center">Visualización de Aciertos</h3>
                        <div className="w-full h-10 bg-red-200 dark:bg-red-900/70 rounded-full overflow-hidden flex">
                           <div 
                             className="h-full bg-green-400 dark:bg-green-500 transition-all duration-500"
                             style={{ width: `${successPercentage}%` }}
                           ></div>
                        </div>
                         <div className="flex justify-between mt-2 text-sm font-medium">
                            <span className="text-green-600 dark:text-green-300">Aciertos: {correctAnswers}</span>
                            <span className="text-red-600 dark:text-red-300">Fallos: {incorrectAnswers}</span>
                        </div>
                    </div>}
                </div>
            </div>
        </div>
    );
};

export default ProgressView;
