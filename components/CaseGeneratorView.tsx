import React, { useState, useCallback } from 'react';
import { generatePracticalCase } from '../services/geminiService';
import { PracticalCase, PracticalCaseQuestion, PracticalCaseOption, CaseAnswer } from '../types';
import { BrainIcon } from './icons/BrainIcon';
import { ProgressData } from '../App';

interface CaseGeneratorViewProps {
    currentCase: PracticalCase | null;
    setCurrentCase: React.Dispatch<React.SetStateAction<PracticalCase | null>>;
    caseAnswers: CaseAnswer;
    setCaseAnswers: React.Dispatch<React.SetStateAction<CaseAnswer>>;
    isLoading: boolean;
    setIsLoading: React.Dispatch<React.SetStateAction<boolean>>;
    addProgressData: (data: ProgressData) => void;
}

const QuestionView: React.FC<{
    question: PracticalCaseQuestion;
    topic: string;
    answers: CaseAnswer[string];
    onSelect: (questionId: string, optionId: string) => void;
}> = ({ question, topic, answers, onSelect }) => {
    
    const { selectedOptions = [], attempts = 0, showExplanation = false } = answers || {};

    const getOptionClasses = (option: PracticalCaseOption) => {
        const isSelected = selectedOptions.includes(option.id);
        
        if (showExplanation) {
          if (option.id === question.correct_option_id) {
            return 'bg-green-100 dark:bg-green-900 border-green-500 dark:border-green-400 ring-2 ring-green-500 cursor-default';
          }
          if (isSelected) {
            return 'bg-red-100 dark:bg-red-900 border-red-500 dark:border-red-400 ring-2 ring-red-500 cursor-default';
          }
          return 'bg-slate-100 dark:bg-slate-800 opacity-50 cursor-default';
        }
    
        if (isSelected) {
            return 'bg-red-100 dark:bg-red-900 border-red-400 cursor-not-allowed opacity-70';
        }
    
        return 'hover:bg-blue-100 dark:hover:bg-slate-700 cursor-pointer';
    };

    return (
        <div className="p-6 bg-white dark:bg-slate-800/50 rounded-xl shadow-sm">
            <div className='flex justify-between items-center mb-4'>
                <h3 className="text-lg font-semibold text-slate-800 dark:text-slate-100">{question.id.replace('q', '')}. {question.question}</h3>
                {!showExplanation && <span className="text-sm font-medium text-slate-500 dark:text-slate-400 bg-slate-100 dark:bg-slate-700 px-3 py-1 rounded-full">Intentos: {2 - attempts}</span>}
            </div>
            <div className="space-y-3">
                {question.options.map(option => (
                    <div key={option.id} onClick={() => onSelect(question.id, option.id)} className={`p-4 border dark:border-slate-700 rounded-lg transition-all duration-300 flex items-start space-x-4 ${getOptionClasses(option)}`}>
                       <div className="font-bold text-slate-700 dark:text-slate-200 flex-shrink-0">{option.id}.</div>
                       <div className="text-slate-700 dark:text-slate-300">{option.text}</div>
                    </div>
                ))}
            </div>
             {attempts === 1 && !showExplanation && <div className="mt-4 text-center text-red-600 dark:text-red-400 font-semibold">Respuesta incorrecta. ¡Te queda un intento!</div>}
             {showExplanation && (
                <div className="mt-6 p-4 bg-amber-50 dark:bg-amber-900/40 border-l-4 border-amber-400 rounded-r-lg animate-fade-in">
                    <h4 className="font-semibold text-amber-800 dark:text-amber-200 mb-2">Explicación:</h4>
                    <p className="text-sm text-amber-700 dark:text-amber-300 leading-relaxed whitespace-pre-wrap">{question.explanation}</p>
                </div>
            )}
        </div>
    );
};


const CaseGeneratorView: React.FC<CaseGeneratorViewProps> = ({ currentCase, setCurrentCase, caseAnswers, setCaseAnswers, isLoading, setIsLoading, addProgressData }) => {
  const [error, setError] = useState<string | null>(null);

  const fetchNewCase = useCallback(() => {
    setIsLoading(true);
    setError(null);
    setCurrentCase(null);
    setCaseAnswers({});

    generatePracticalCase()
      .then(newCase => {
        setCurrentCase(newCase);
        const initialAnswers: CaseAnswer = {};
        newCase.questions.forEach(q => {
            initialAnswers[q.id] = { selectedOptions: [], attempts: 0, showExplanation: false };
        });
        setCaseAnswers(initialAnswers);
      })
      .catch((err: Error) => setError(err.message))
      .finally(() => setIsLoading(false));
  }, [setIsLoading, setCurrentCase, setCaseAnswers]);

  const handleOptionSelect = (questionId: string, optionId: string) => {
    const questionState = caseAnswers[questionId];
    if (questionState.showExplanation || questionState.attempts >= 2) return;

    const newAttempts = questionState.attempts + 1;
    const isCorrect = currentCase?.questions.find(q => q.id === questionId)?.correct_option_id === optionId;
    
    const shouldShowExplanation = isCorrect || newAttempts >= 2;

    if (shouldShowExplanation) {
        addProgressData({
            questionId: `${currentCase?.topic}-${questionId}`,
            isCorrect: isCorrect,
            timestamp: Date.now(),
            topic: currentCase?.topic || 'General'
        });
    }

    setCaseAnswers(prev => ({
        ...prev,
        [questionId]: {
            selectedOptions: [...questionState.selectedOptions, optionId],
            attempts: newAttempts,
            showExplanation: shouldShowExplanation,
        }
    }));
  };
  
  const renderContent = () => {
    if (isLoading) {
      return (
        <div className="flex flex-col items-center justify-center h-full text-center">
            <BrainIcon className="w-16 h-16 text-blue-500 animate-pulse" />
            <h2 className="mt-4 text-xl font-semibold text-slate-700 dark:text-slate-300">Generando caso práctico con Gemini Pro...</h2>
            <p className="mt-2 text-slate-500 dark:text-slate-400">El modelo está usando su "modo de pensamiento" para crear un desafío realista y complejo. Esto puede tardar unos segundos.</p>
        </div>
      );
    }
    if (error) {
      return <div className="text-red-500 bg-red-100 dark:bg-red-900 p-4 rounded-lg">{error}</div>;
    }
    if (currentCase) {
      return (
        <div className="max-w-4xl mx-auto space-y-8">
            <div className="p-6 bg-slate-50 dark:bg-slate-800 rounded-xl shadow-sm">
                <span className="inline-block bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-sm font-medium px-3 py-1 rounded-full mb-3">{currentCase.topic}</span>
                <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100 mb-2">Escenario:</h2>
                <p className="text-slate-600 dark:text-slate-300 leading-relaxed whitespace-pre-wrap">{currentCase.scenario}</p>
            </div>
            
            <div className="space-y-6">
                {currentCase.questions.map((q) => (
                    <QuestionView 
                        key={q.id}
                        question={q}
                        topic={currentCase.topic}
                        answers={caseAnswers[q.id]}
                        onSelect={handleOptionSelect}
                    />
                ))}
            </div>
        </div>
      );
    }
    return (
        <div className="flex flex-col items-center justify-center h-full text-center">
            <BrainIcon className="w-16 h-16 text-blue-500" />
            <h2 className="mt-4 text-2xl font-semibold text-slate-700 dark:text-slate-300">Listo para ponerte a prueba</h2>
            <p className="mt-2 text-slate-500 dark:text-slate-400">Haz clic en "Nuevo Caso" para generar un supuesto práctico único y desafiante.</p>
        </div>
    );
  };

  return (
    <div className="flex flex-col h-full bg-white dark:bg-slate-900">
      <header className="p-4 border-b border-slate-200 dark:border-slate-800 flex justify-between items-center">
        <div>
            <h1 className="text-xl font-bold text-slate-800 dark:text-slate-100">Generador de Casos Prácticos</h1>
            <p className="text-sm text-slate-500 dark:text-slate-400">Casos prácticos con múltiples preguntas, como en el examen oficial.</p>
        </div>
        <button
            onClick={fetchNewCase}
            disabled={isLoading}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg font-semibold hover:bg-blue-600 disabled:bg-slate-400 dark:disabled:bg-slate-600 transition-colors flex items-center space-x-2"
        >
            <svg xmlns="http://www.w3.org/2000/svg" className={`h-5 w-5 ${isLoading ? 'animate-spin' : ''}`} viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 110 2H4a1 1 0 01-1-1V4a1 1 0 011-1zm10 8a1 1 0 011-1v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 011.885-.666A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 111.885-.666A5.002 5.002 0 008.001 17H11a1 1 0 110 2h-3a1 1 0 01-1-1v-5a1 1 0 011-1z" clipRule="evenodd" />
            </svg>
            <span>{isLoading ? 'Generando...' : 'Nuevo Caso'}</span>
        </button>
      </header>

      <div className="flex-1 overflow-y-auto p-6 lg:p-8">
        {renderContent()}
      </div>
    </div>
  );
};

export default CaseGeneratorView;