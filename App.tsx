import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ChatView from './components/ChatView';
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
import { AppView, PracticalCase, CaseAnswer, MindMapNode } from './types';

export interface ProgressData {
  questionId: string;
  isCorrect: boolean;
  timestamp: number;
  topic: string;
}

// Custom hook for localStorage persistence
function usePersistentState<T>(key: string, initialState: T): [T, React.Dispatch<React.SetStateAction<T>>] {
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


const App: React.FC = () => {
  const [currentView, setCurrentView] = useState<AppView>(AppView.CHAT);

  // State lifted for persistence across views and sessions
  const [currentCase, setCurrentCase] = usePersistentState<PracticalCase | null>('caseGenerator_currentCase', null);
  const [caseAnswers, setCaseAnswers] = usePersistentState<CaseAnswer>('caseGenerator_caseAnswers', {});
  const [caseIsLoading, setCaseIsLoading] = useState<boolean>(false);
  
  const [progressData, setProgressData] = usePersistentState<ProgressData[]>('progressTracker_data', []);

  // States for other persistent views
  const [mindMapState, setMindMapState] = usePersistentState<{ topic: string; map: MindMapNode | null }>('mindMap_lastState', { topic: '', map: null });
  const [schemaState, setSchemaState] = usePersistentState<{ topic: string; schema: string }>('schema_lastState', { topic: '', schema: '' });
  const [summaryState, setSummaryState] = usePersistentState<{ text: string; summary: string }>('summary_lastState', { text: '', summary: '' });
  const [comparatorState, setComparatorState] = usePersistentState<{ textA: string; textB: string; comparison: string }>('comparator_lastState', { textA: '', textB: '', comparison: '' });


  const renderView = () => {
    switch (currentView) {
      case AppView.CHAT:
        return <ChatView />;
      case AppView.CASE_GENERATOR:
        return (
          <CaseGeneratorView 
            currentCase={currentCase}
            setCurrentCase={setCurrentCase}
            caseAnswers={caseAnswers}
            setCaseAnswers={setCaseAnswers}
            isLoading={caseIsLoading}
            setIsLoading={setCaseIsLoading}
            addProgressData={(data) => setProgressData(prev => [...prev, data])}
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
        return <ComparatorView savedState={comparatorState} setSavedState={setComparatorState} />;
      case AppView.MOCK_EXAM:
        return <MockExamView addProgressData={(data) => setProgressData(prev => [...prev, ...data])} />;
       case AppView.FLASHCARDS:
        return <FlashcardsView />;
      default:
        return <ChatView />;
    }
  };

  return (
    <div className="flex h-screen w-screen text-slate-800 dark:text-slate-200 bg-slate-50 dark:bg-slate-900 overflow-hidden">
      <Sidebar currentView={currentView} setCurrentView={setCurrentView} />
      <main className="flex-1 flex flex-col h-full overflow-y-auto">
        {renderView()}
      </main>
    </div>
  );
};

export default App;