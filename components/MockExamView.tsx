import React, { useState, useEffect } from 'react';
import { generateMockExam } from '../services/geminiService';
import { MockExam, PracticalCaseQuestion, CaseAnswer } from '../types';
import { ProgressData } from '../App';
import { SparkIcon } from './icons/SparkIcon';
import { ExamIcon } from './icons/ExamIcon';

const syllabusTopics = [
    "Incapacidad Temporal", "Jubilación", "Muerte y Supervivencia",
    "Cotización y Recaudación", "Afiliación y Altas/Bajas", "Acción Protectora",
    "Nacimiento y Cuidado de Menor", "Incapacidad Permanente", "Ingreso Mínimo Vital"
];

type ExamStage = 'config' | 'generating' | 'in_progress' | 'results';

const MockExamView: React.FC<{ addProgressData: (data: ProgressData[]) => void }> = ({ addProgressData }) => {
    const [stage, setStage] = useState<ExamStage>('config');
    const [exam, setExam] = useState<MockExam | null>(null);
    const [answers, setAnswers] = useState<CaseAnswer>({});
    const [error, setError] = useState<string | null>(null);
    
    // Config state
    const [selectedTopics, setSelectedTopics] = useState<string[]>([]);
    const [questionCount, setQuestionCount] = useState(10);

    // Timer state
    const [timeLeft, setTimeLeft] = useState(0);

    useEffect(() => {
        if (stage === 'in_progress' && timeLeft > 0) {
            const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
            return () => clearTimeout(timer);
        } else if (stage === 'in_progress' && timeLeft === 0) {
            handleFinishExam();
        }
    }, [stage, timeLeft]);

    const handleTopicToggle = (topic: string) => {
        setSelectedTopics(prev =>
            prev.includes(topic) ? prev.filter(t => t !== topic) : [...prev, topic]
        );
    };

    const handleStartGeneration = async () => {
        if (selectedTopics.length === 0) {
            setError("Debes seleccionar al menos un tema.");
            return;
        }
        setStage('generating');
        setError(null);
        try {
            const newExam = await generateMockExam(selectedTopics, questionCount);
            setExam(newExam);
            const initialAnswers: CaseAnswer = {};
            newExam.questions.forEach(q => {
                initialAnswers[q.id] = { selectedOptions: [], attempts: 1, showExplanation: false };
            });
            setAnswers(initialAnswers);
            setTimeLeft(questionCount * 90); // 90 seconds per question
            setStage('in_progress');
        } catch (err: any) {
            setError(err.message);
            setStage('config');
        }
    };
    
    const handleOptionSelect = (questionId: string, optionId: string) => {
        setAnswers(prev => ({
            ...prev,
            [questionId]: {
                ...prev[questionId],
                selectedOptions: [optionId],
            }
        }));
    };
    
    const handleFinishExam = () => {
        const progress: ProgressData[] = exam!.questions.map(q => {
            const answer = answers[q.id];
            const isCorrect = answer?.selectedOptions[0] === q.correct_option_id;
            return {
                questionId: `${q.id}-${Date.now()}`,
                isCorrect,
                timestamp: Date.now(),
                topic: selectedTopics.join(', ')
            };
        });
        addProgressData(progress);
        setStage('results');
    };
    
    const formatTime = (seconds: number) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    };

    const correctCount = exam ? Object.keys(answers).filter(qId => answers[qId].selectedOptions[0] === exam.questions.find(q => q.id === qId)?.correct_option_id).length : 0;
    const score = exam ? (correctCount / exam.questions.length) * 10 : 0;


    const renderContent = () => {
        switch (stage) {
            case 'config':
                return (
                    <div className="max-w-3xl mx-auto">
                        <h2 className="text-2xl font-bold mb-4">Configura tu Simulacro</h2>
                        {error && <p className="text-red-500 bg-red-100 p-3 rounded-md mb-4">{error}</p>}
                        <div className="mb-6">
                            <label className="block text-lg font-semibold mb-2">Número de preguntas:</label>
                            <input type="number" value={questionCount} onChange={e => setQuestionCount(Number(e.target.value))} min="5" max="50" className="w-full p-2 border rounded-md dark:bg-slate-800 dark:border-slate-700" />
                        </div>
                        <div className="mb-6">
                            <h3 className="text-lg font-semibold mb-2">Temas a incluir:</h3>
                            <div className="flex flex-wrap gap-2">
                                {syllabusTopics.map(topic => (
                                    <button key={topic} onClick={() => handleTopicToggle(topic)} className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${selectedTopics.includes(topic) ? 'bg-blue-500 text-white' : 'bg-slate-200 dark:bg-slate-700'}`}>
                                        {topic}
                                    </button>
                                ))}
                            </div>
                        </div>
                        <button onClick={handleStartGeneration} disabled={selectedTopics.length === 0} className="w-full py-3 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 disabled:bg-slate-400">
                            Empezar Simulacro
                        </button>
                    </div>
                );
            case 'generating':
                return (
                     <div className="text-center">
                        <SparkIcon className="w-16 h-16 text-blue-500 animate-pulse mx-auto" />
                        <h2 className="mt-4 text-xl font-semibold">Generando tu examen personalizado...</h2>
                        <p className="mt-2 text-slate-500">Esto puede tardar unos segundos.</p>
                    </div>
                );
            case 'in_progress':
                return (
                    <div className="max-w-4xl mx-auto">
                        <div className="sticky top-0 bg-white dark:bg-slate-900 py-4 mb-6 z-10 border-b dark:border-slate-800">
                           <div className="flex justify-between items-center">
                             <h2 className="text-2xl font-bold">{exam?.title}</h2>
                             <div className="text-xl font-bold bg-slate-200 dark:bg-slate-700 px-4 py-2 rounded-lg">{formatTime(timeLeft)}</div>
                           </div>
                        </div>
                        <div className="space-y-8">
                            {exam?.questions.map((q, index) => (
                                <div key={q.id} className="p-6 bg-slate-50 dark:bg-slate-800/50 rounded-xl">
                                    <p className="font-semibold mb-4">{index + 1}. {q.question}</p>
                                    <div className="space-y-2">
                                        {q.options.map(opt => (
                                            <label key={opt.id} className={`flex items-center space-x-3 p-3 rounded-md cursor-pointer transition-colors ${answers[q.id]?.selectedOptions[0] === opt.id ? 'bg-blue-200 dark:bg-blue-900' : 'hover:bg-slate-200 dark:hover:bg-slate-700'}`}>
                                                <input type="radio" name={q.id} value={opt.id} onChange={() => handleOptionSelect(q.id, opt.id)} className="form-radio" />
                                                <span>{opt.text}</span>
                                            </label>
                                        ))}
                                    </div>
                                </div>
                            ))}
                        </div>
                        <button onClick={handleFinishExam} className="mt-8 w-full py-3 bg-green-600 text-white font-bold rounded-lg hover:bg-green-700">
                            Finalizar y Corregir
                        </button>
                    </div>
                );
            case 'results':
                 return (
                    <div className="max-w-4xl mx-auto text-center">
                        <h2 className="text-3xl font-bold mb-4">Resultados del Simulacro</h2>
                        <p className="text-5xl font-bold mb-2" style={{ color: score >= 5 ? '#22c55e' : '#ef4444' }}>{score.toFixed(2)} / 10</p>
                        <p className="text-lg mb-8">{correctCount} de {exam?.questions.length} preguntas correctas.</p>
                        <div className="mb-8">
                           <button onClick={() => setStage('config')} className="px-6 py-2 bg-blue-500 text-white font-semibold rounded-lg">
                                Nuevo Simulacro
                           </button>
                        </div>
                        <div className="text-left space-y-6">
                            <h3 className="text-2xl font-bold">Revisión de Preguntas</h3>
                            {exam?.questions.map(q => {
                                const userAnswer = answers[q.id]?.selectedOptions[0];
                                const isCorrect = userAnswer === q.correct_option_id;
                                return (
                                <div key={q.id} className="p-4 border rounded-lg dark:border-slate-700">
                                    <p className="font-semibold">{q.question}</p>
                                    <p className={`mt-2 text-sm ${isCorrect ? 'text-green-600' : 'text-red-600'}`}>
                                        Tu respuesta: {userAnswer ? q.options.find(o=>o.id === userAnswer)?.text : 'No contestada'} - {isCorrect ? 'Correcta' : 'Incorrecta'}
                                    </p>
                                    {!isCorrect && <p className="text-sm">Respuesta correcta: {q.options.find(o=>o.id === q.correct_option_id)?.text}</p>}
                                    <details className="mt-2 text-sm">
                                        <summary className="cursor-pointer font-semibold">Ver explicación</summary>
                                        <p className="mt-1 p-2 bg-slate-100 dark:bg-slate-800 rounded">{q.explanation}</p>
                                    </details>
                                </div>
                                )
                            })}
                        </div>
                    </div>
                );
        }
    };

    return (
        <div className="flex flex-col h-full bg-white dark:bg-slate-900">
            <header className="p-4 border-b border-slate-200 dark:border-slate-800">
                <h1 className="text-xl font-bold text-slate-800 dark:text-slate-100">Simulacros de Examen</h1>
                <p className="text-sm text-slate-500 dark:text-slate-400">Ponte a prueba con exámenes generados por IA.</p>
            </header>
            <div className="flex-1 overflow-y-auto p-6 lg:p-8 flex justify-center items-center">
                {renderContent()}
            </div>
        </div>
    );
};

export default MockExamView;
