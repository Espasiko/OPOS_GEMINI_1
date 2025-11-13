export enum AppView {
  CHAT = 'CHAT',
  CASE_GENERATOR = 'CASE_GENERATOR',
  SEARCH = 'SEARCH',
  SYLLABUS = 'SYLLABUS',
  MIND_MAP = 'MIND_MAP',
  SCHEMA = 'SCHEMA',
  SUMMARY = 'SUMMARY',
  COMPARATOR = 'COMPARATOR',
  STUDY_PLAN = 'STUDY_PLAN',
  MOCK_EXAM = 'MOCK_EXAM',
  FLASHCARDS = 'FLASHCARDS',
  PROGRESS = 'PROGRESS',
  USER_GUIDE = 'USER_GUIDE',
  SETTINGS = 'SETTINGS',
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'model';
  text: string;
}

export interface Conversation {
  id: string;
  title: string;
  messages: ChatMessage[];
}

export interface PracticalCaseOption {
  id: string;
  text: string;
}

export interface PracticalCaseQuestion {
  id: string;
  question: string;
  options: PracticalCaseOption[];
  correct_option_id: string;
  explanation: string;
}

export interface PracticalCase {
  topic: string;
  scenario: string;
  questions: PracticalCaseQuestion[];
}

export interface CaseAnswer {
    [questionId: string]: {
        selectedOptions: string[];
        attempts: number;
        showExplanation: boolean;
    }
}

export interface GroundingSource {
    uri: string;
    title: string;
}

// Types for Mind Map
export interface MindMapNode {
    id: string;
    text: string;
    children: MindMapNode[];
}

// Types for Study Plan
export interface StudyPlanInput {
    availability: string;
    duration: 'semanal' | 'mensual' | 'trimestral';
    includeTracking: boolean;
    includeSuggestions: boolean;
}

// Types for Mock Exam
export interface MockExam {
    title: string;
    questions: PracticalCaseQuestion[];
}

// Types for Flashcards
export interface Flashcard {
    id: string;
    front: string;
    back: string;
}
