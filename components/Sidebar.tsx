import React from 'react';
import { AppView } from '../types';
import { SparkIcon } from './icons/SparkIcon';
import { ChatIcon } from './icons/ChatIcon';
import { SearchIcon } from './icons/SearchIcon';
import { BrainIcon } from './icons/BrainIcon';
import { BookIcon } from './icons/BookIcon';
import { MapIcon } from './icons/MapIcon';
import { CalendarIcon } from './icons/CalendarIcon';
import { ChartBarIcon } from './icons/ChartBarIcon';
import { QuestionMarkCircleIcon } from './icons/QuestionMarkCircleIcon';
import { CogIcon } from './icons/CogIcon';
import { SchemaIcon } from './icons/SchemaIcon';
import { SummaryIcon } from './icons/SummaryIcon';
import { CompareIcon } from './icons/CompareIcon';
import { ExamIcon } from './icons/ExamIcon';
import { FlashcardIcon } from './icons/FlashcardIcon';

interface SidebarProps {
  currentView: AppView;
  setCurrentView: (view: AppView) => void;
}

const NavButton: React.FC<{
    isActive: boolean;
    onClick: () => void;
    label: string;
    icon: React.ReactNode;
}> = ({ isActive, onClick, label, icon }) => (
    <button
        onClick={onClick}
        className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors duration-200 ${
            isActive
            ? 'bg-blue-500 text-white shadow-md'
            : 'text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800'
        }`}
    >
        {icon}
        <span>{label}</span>
    </button>
);


const Sidebar: React.FC<SidebarProps> = ({ currentView, setCurrentView }) => {
  const primaryNavItems = [
    { view: AppView.CHAT, label: 'Chat Explicativo', icon: <ChatIcon className="h-5 w-5" /> },
    { view: AppView.CASE_GENERATOR, label: 'Generador de Casos', icon: <BrainIcon className="h-5 w-5" /> },
    { view: AppView.MOCK_EXAM, label: 'Simulacros de Examen', icon: <ExamIcon className="h-5 w-5" /> },
    { view: AppView.SEARCH, label: 'Búsqueda Actualizada', icon: <SearchIcon className="h-5 w-5" /> },
    { view: AppView.SYLLABUS, label: 'Temario Oficial', icon: <BookIcon className="h-5 w-5" /> },
  ];

  const toolsNavItems = [
    { view: AppView.MIND_MAP, label: 'Mapas Mentales', icon: <MapIcon className="h-5 w-5" /> },
    { view: AppView.SCHEMA, label: 'Esquemas', icon: <SchemaIcon className="h-5 w-5" /> },
    { view: AppView.SUMMARY, label: 'Resúmenes', icon: <SummaryIcon className="h-5 w-5" /> },
    { view: AppView.COMPARATOR, label: 'Comparador de Leyes', icon: <CompareIcon className="h-5 w-5" /> },
    { view: AppView.FLASHCARDS, label: 'Tarjetas y Memes', icon: <FlashcardIcon className="h-5 w-5" /> },
    { view: AppView.STUDY_PLAN, label: 'Plan de Estudios', icon: <CalendarIcon className="h-5 w-5" /> },
    { view: AppView.PROGRESS, label: 'Mi Progreso', icon: <ChartBarIcon className="h-5 w-5" /> },
  ];

  const footerNavItems = [
    { view: AppView.USER_GUIDE, label: 'Guía de Uso', icon: <QuestionMarkCircleIcon className="h-5 w-5" /> },
    { view: AppView.SETTINGS, label: 'Configuración', icon: <CogIcon className="h-5 w-5" /> },
  ];

  return (
    <nav className="flex flex-col w-64 bg-slate-100 dark:bg-slate-950 border-r border-slate-200 dark:border-slate-800 p-4">
      <div className="flex items-center space-x-2 px-2 mb-8">
        <SparkIcon className="h-8 w-8 text-blue-500" />
        <span className="text-xl font-bold text-slate-800 dark:text-slate-100">OpositaIA</span>
      </div>
      
      <div className="flex-grow flex flex-col justify-between overflow-y-auto pr-2">
        <div className="space-y-6">
            <div>
                <h3 className="px-3 mb-2 text-xs font-semibold uppercase text-slate-400 tracking-wider">Principal</h3>
                <ul className="space-y-2">
                    {primaryNavItems.map((item) => (
                        <li key={item.view}><NavButton isActive={currentView === item.view} onClick={() => setCurrentView(item.view)} label={item.label} icon={item.icon} /></li>
                    ))}
                </ul>
            </div>
            <div>
                <h3 className="px-3 mb-2 text-xs font-semibold uppercase text-slate-400 tracking-wider">Herramientas</h3>
                <ul className="space-y-2">
                    {toolsNavItems.map((item) => (
                        // FIX: Corrected typo from item.vew to item.view
                        <li key={item.view}><NavButton isActive={currentView === item.view} onClick={() => setCurrentView(item.view)} label={item.label} icon={item.icon} /></li>
                    ))}
                </ul>
            </div>
        </div>
        
        <div>
            <ul className="space-y-2 pt-4 border-t border-slate-200 dark:border-slate-800">
                 {footerNavItems.map((item) => (
                    <li key={item.view}><NavButton isActive={currentView === item.view} onClick={() => setCurrentView(item.view)} label={item.label} icon={item.icon} /></li>
                ))}
            </ul>
             <div className="text-xs text-slate-400 dark:text-slate-500 text-center mt-4">
                &copy; {new Date().getFullYear()} OpositaIA
             </div>
        </div>
      </div>
    </nav>
  );
};

export default Sidebar;