import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ModelSelector from './components/ModelSelector';
import { ModelProvider } from './contexts/ModelContext';
import ChatView from './components/ChatView';
import UsageStats from './components/UsageStats';
import CaseGeneratorView from './components/CaseGeneratorView';
import SearchGroundingView from './components/SearchGroundingView';
import SyllabusView from './components/SyllabusView';
import MindMapView from './components/MindMapView';
import StudyPlanView from './components/StudyPlanView';
import ProgressView from './components/ProgressView';
import UserGuideView from './components/UserGuideView';
import SettingsView from './components/SettingsView';
import SchemaView from './components/SchemaView';
import SummaryView from './components/SummaryView';
import ComparatorView from './components/ComparatorView';
import MockExamView from './components/MockExamView';
import FlashcardsView from './components/FlashcardsView';
import { VPSTestView } from './components/VPSTestView';
import BackendTestView from './components/BackendTestView';
import { AppView, PracticalCase, CaseAnswer, MindMapNode } from './types';

export interface ProgressData {
  questionId: string;
  isCorrect: boolean;
  timestamp: number;
  topic: string;
}

/**
 * Un custom hook que persiste el estado en `window.localStorage`.
 * Lee el valor inicial de localStorage y actualiza localStorage cada vez que el estado cambia.
 * @param {string} key La clave a usar en localStorage.
 * @param {T} initialState El estado inicial si no se encuentra nada en localStorage.
 * @returns {[T, React.Dispatch<React.SetStateAction<T>>]} Un array con el estado y la función para actualizarlo.
 */
function usePersistentState<T>(
  key: string,
  initialState: T
): [T, React.Dispatch<React.SetStateAction<T>>] {
  const [state, setState] = useState<T>(() => {
    try {
      const storedValue = window.localStorage.getItem(key);
      return storedValue ? JSON.parse(storedValue) : initialState;
    } catch (error) {
      console.error(`Error reading localStorage key “${key}”:`, error);
      return initialState;
    }
  });

  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(state));
    } catch (error) {
      console.error(`Error setting localStorage key “${key}”:`, error);
    }
  }, [key, state]);

  return [state, setState];
}

/**
 * El componente principal de la aplicación OpositaIA.
 * Actúa como el contenedor principal, gestionando el estado global como la vista actual
 * y los datos persistentes entre sesiones (a través del hook `usePersistentState`).
 * Funciona como un enrutador simple, renderizando el componente de la vista apropiado
 * basado en el estado `currentView`.
 */
const App: React.FC = () => {
  const [currentView, setCurrentView] = useState<AppView>(AppView.CHAT);
  const [selectedModel, setSelectedModel] = usePersistentState<string>('selectedModel', 'groq-8b');

  // State lifted for persistence across views and sessions
  const [currentCase, setCurrentCase] = usePersistentState<PracticalCase | null>(
    'caseGenerator_currentCase',
    null
  );
  const [caseAnswers, setCaseAnswers] = usePersistentState<CaseAnswer>(
    'caseGenerator_caseAnswers',
    {}
  );
  const [caseIsLoading, setCaseIsLoading] = useState<boolean>(false);

  const [progressData, setProgressData] = usePersistentState<ProgressData[]>(
    'progressTracker_data',
    []
  );

  // States for other persistent views
  const [mindMapState, setMindMapState] = usePersistentState<{
    topic: string;
    map: MindMapNode | null;
  }>('mindMap_lastState', { topic: '', map: null });
  const [schemaState, setSchemaState] = usePersistentState<{ topic: string; schema: string }>(
    'schema_lastState',
    { topic: '', schema: '' }
  );
  const [summaryState, setSummaryState] = usePersistentState<{ text: string; summary: string }>(
    'summary_lastState',
    { text: '', summary: '' }
  );
  const [comparisonResult, setComparisonResult] = usePersistentState<string>(
    'comparator_lastResult',
    ''
  ); // FIX: Persist only the result for the comparator to avoid exceeding localStorage quota with two large text inputs.

  const renderView = () => {
    switch (currentView) {
      case AppView.CHAT:
        return <ChatView />;
      case AppView.USAGE_STATS:
        return <UsageStats />;
      case AppView.CASE_GENERATOR:
        return (
          <CaseGeneratorView
            currentCase={currentCase}
            setCurrentCase={setCurrentCase}
            caseAnswers={caseAnswers}
            setCaseAnswers={setCaseAnswers}
            isLoading={caseIsLoading}
            setIsLoading={setCaseIsLoading}
            addProgressData={data => setProgressData(prev => [...prev, data])}
          />
        );
      case AppView.SEARCH:
        return <SearchGroundingView />;
      case AppView.SYLLABUS:
        return <SyllabusView />;
      case AppView.MIND_MAP:
        return <MindMapView savedState={mindMapState} setSavedState={setMindMapState} />;
      case AppView.STUDY_PLAN:
        return <StudyPlanView />;
      case AppView.PROGRESS:
        return <ProgressView progressData={progressData} />;
      case AppView.USER_GUIDE:
        return <UserGuideView />;
      case AppView.SETTINGS:
        return <SettingsView />;
      case AppView.SCHEMA:
        return <SchemaView savedState={schemaState} setSavedState={setSchemaState} />;
      case AppView.SUMMARY:
        return <SummaryView savedState={summaryState} setSavedState={setSummaryState} />;
      case AppView.COMPARATOR:
        return (
          <ComparatorView
            savedComparison={comparisonResult}
            setSavedComparison={setComparisonResult}
          />
        );
      case AppView.MOCK_EXAM:
        return (
          <MockExamView addProgressData={data => setProgressData(prev => [...prev, ...data])} />
        );
      case AppView.FLASHCARDS:
        return <FlashcardsView />;
      case AppView.VPS_TEST:
        return <VPSTestView />;
      case AppView.BACKEND_TEST:
        return <BackendTestView />;
      default:
        return <ChatView />;
    }
  };

  return (
    <ModelProvider value={{ selectedModel, setSelectedModel }}>
      <div className="flex h-screen w-screen text-slate-800 dark:text-slate-200 bg-slate-50 dark:bg-slate-900 overflow-hidden">
        <Sidebar currentView={currentView} setCurrentView={setCurrentView} />
        <main className="flex-1 flex flex-col h-full overflow-hidden">
          <div className="flex items-center justify-end px-6 py-3 border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900">
            <ModelSelector value={selectedModel} onChange={setSelectedModel} />
          </div>
          <div className="flex-1 overflow-y-auto">{renderView()}</div>
        </main>
      </div>
    </ModelProvider>
  );
};

export default App;
