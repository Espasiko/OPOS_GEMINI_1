# Implementation Plan: Audio Quiz Generator

## 1. Overview

Create an audio-based quiz feature that reads legal questions aloud and allows users to answer verbally or by clicking. This enhances accessibility and provides an alternative study method.

**User Benefit**: Hands-free study mode, better for auditory learners, accessibility improvement

**Technical Approach**: Use Web Speech API for text-to-speech, integrate with existing quiz generation from Gemini API

## 2. AI Agent Definition

### Model Selection
- **Model**: `gemini-2.5-flash`
- **Justification**: Quick quiz generation for interactive experience. Flash model provides fast response times needed for real-time quiz flow.

### Agent Configuration
```typescript
{
  model: 'gemini-2.5-flash',
  generationConfig: {
    responseMimeType: "application/json",
    responseSchema: {
      type: "object",
      properties: {
        questions: {
          type: "array",
          items: {
            type: "object",
            properties: {
              question: { type: "string" },
              options: {
                type: "array",
                items: { type: "string" }
              },
              correctAnswer: { type: "number" },
              explanation: { type: "string" }
            }
          }
        }
      }
    }
  }
}
```

### System Instruction / Prompt
```
You are an expert quiz generator for Spanish Social Security law exam preparation.

Task: Generate 5 multiple-choice questions on the topic: {topic}

Requirements:
- Questions must be clear and concise for audio reading
- 4 options per question (A, B, C, D)
- One correct answer
- Brief explanation for each answer
- Questions should test understanding, not just memorization
- Use formal Spanish appropriate for legal context

Output format: JSON with questions array
```

## 3. Implementation Steps

### Step 0: Create Feature Branch
- **Branch Name**: `feature/audio-quiz`
- **Commands**:
  ```bash
  git checkout -b feature/audio-quiz
  ```

### Step 1: Define Types
- **File**: `types.ts`
- **Action**: Add audio quiz types
- **Types to Add**:
  ```typescript
  export interface AudioQuizQuestion {
    id: string;
    question: string;
    options: string[];
    correctAnswer: number;
    explanation: string;
    userAnswer?: number;
  }
  
  export interface AudioQuizState {
    questions: AudioQuizQuestion[];
    currentQuestionIndex: number;
    score: number;
    isPlaying: boolean;
    isComplete: boolean;
  }
  
  // Update AppView enum
  export enum AppView {
    // ... existing views
    AUDIO_QUIZ = 'AUDIO_QUIZ'
  }
  ```

### Step 2: Implement Service Function
- **File**: `services/geminiService.ts`
- **Function Signature**:
  ```typescript
  export async function generateAudioQuiz(
    topic: string,
    questionCount: number = 5
  ): Promise<AudioQuizQuestion[]>
  ```
- **Implementation Steps**:
  1. Get gemini-2.5-flash model instance
  2. Build prompt with topic and question count
  3. Call generateContent() with JSON schema
  4. Parse response
  5. Add unique IDs to questions
  6. Return questions array
  7. Handle errors (network, API, parsing)

### Step 3: Create Component
- **File**: `components/AudioQuiz.tsx`
- **Component Structure**:
  ```typescript
  interface AudioQuizProps {
    onClose: () => void;
  }
  
  export const AudioQuiz: React.FC<AudioQuizProps> = ({ onClose }) => {
    // State
    const [topic, setTopic] = useState('');
    const [loading, setLoading] = useState(false);
    const [quizState, setQuizState] = useState<AudioQuizState | null>(null);
    const [error, setError] = useState('');
    
    // Speech synthesis
    const speak = (text: string) => {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'es-ES';
      window.speechSynthesis.speak(utterance);
    };
    
    // Handlers
    const handleStartQuiz = async () => { /* ... */ };
    const handleAnswer = (answerIndex: number) => { /* ... */ };
    const handleNextQuestion = () => { /* ... */ };
    const handlePlayAudio = () => { /* ... */ };
    
    return (
      <div className="container mt-4">
        {/* UI implementation */}
      </div>
    );
  };
  ```

- **State Management**:
  - `topic`: User input for quiz topic
  - `loading`: API call in progress
  - `quizState`: Current quiz state (questions, progress, score)
  - `error`: Error message if any
  - `isPlaying`: Audio currently playing

- **UI Elements**:
  1. **Setup Screen** (before quiz starts):
     - Topic input field
     - "Start Audio Quiz" button
     - Instructions
  
  2. **Quiz Screen** (during quiz):
     - Question text (large, readable)
     - "Play Audio" button (🔊 icon)
     - 4 option buttons (A, B, C, D)
     - Progress indicator (Question 1/5)
     - Score display
  
  3. **Result Screen** (after quiz):
     - Final score
     - Review of questions with correct answers
     - "Start New Quiz" button
     - "Back to Menu" button

### Step 4: Update App.tsx
- **Actions**:
  1. Import AudioQuiz component:
     ```typescript
     import { AudioQuiz } from './components/AudioQuiz';
     ```
  
  2. Add to view switch statement:
     ```typescript
     case AppView.AUDIO_QUIZ:
       return <AudioQuiz onClose={() => setCurrentView(AppView.CHAT)} />;
     ```
  
  3. Add navigation button in sidebar:
     ```typescript
     <button
       className="btn btn-outline-primary w-100 mb-2"
       onClick={() => setCurrentView(AppView.AUDIO_QUIZ)}
     >
       🎧 Audio Quiz
     </button>
     ```

### Step 5: Update Documentation

#### Update `/docs/AI_AGENTS.md`
Add new section after existing quiz sections:

```markdown
### 6. `generateAudioQuiz()`

*   **Función:** `generateAudioQuiz(topic, questionCount)`
*   **Agente/Personalidad:** "Generador de quiz experto para examen de Seguridad Social española."
*   **Modelo:** `gemini-2.5-flash`
*   **Justificación:** Se necesita generación rápida de preguntas para una experiencia interactiva fluida. El modelo Flash proporciona tiempos de respuesta rápidos necesarios para el flujo del quiz en tiempo real. Las preguntas deben ser claras y concisas para lectura de audio.
*   **Configuración Clave:**
    *   `model: 'gemini-2.5-flash'`
    *   `responseMimeType: "application/json"`
    *   `responseSchema`: Define la estructura para preguntas, opciones, respuesta correcta y explicación.
    *   Preguntas optimizadas para lectura en voz alta (claras, concisas, sin ambigüedades).
```

#### Update `/docs/DATA_MODEL.md`
Add new interfaces:

```markdown
### Audio Quiz Structures

*   **`AudioQuizQuestion`**: Representa una pregunta del quiz de audio.
    *   `id`: Identificador único.
    *   `question`: Texto de la pregunta.
    *   `options`: Array de 4 opciones de respuesta.
    *   `correctAnswer`: Índice de la respuesta correcta (0-3).
    *   `explanation`: Explicación de la respuesta correcta.
    *   `userAnswer`: Respuesta del usuario (opcional).

*   **`AudioQuizState`**: Estado del quiz de audio.
    *   `questions`: Array de preguntas.
    *   `currentQuestionIndex`: Índice de la pregunta actual.
    *   `score`: Puntuación actual.
    *   `isPlaying`: Si el audio está reproduciéndose.
    *   `isComplete`: Si el quiz ha terminado.
```

#### Update `README.md`
Add to features list:

```markdown
*   **Audio Quiz:** Quiz interactivo con lectura de preguntas en voz alta para estudio manos libres y mejor accesibilidad.
```

## 4. Testing Checklist

### Manual Testing
- [ ] Topic input accepts text
- [ ] "Start Quiz" button triggers API call
- [ ] Loading state displays during generation
- [ ] Questions load successfully
- [ ] Audio playback works (🔊 button)
- [ ] Audio reads question in Spanish
- [ ] Option buttons are clickable
- [ ] Correct answer highlights in green
- [ ] Wrong answer highlights in red
- [ ] Score updates correctly
- [ ] Progress indicator updates (1/5, 2/5, etc.)
- [ ] "Next Question" button works
- [ ] Final score displays correctly
- [ ] "Start New Quiz" resets state
- [ ] "Back to Menu" returns to main view
- [ ] Responsive on mobile/tablet/desktop

### Edge Cases
- [ ] Empty topic input (show validation error)
- [ ] Very long topic name (truncate or handle)
- [ ] Network error during generation (show error message)
- [ ] Audio not supported in browser (show fallback message)
- [ ] Rapid clicking on answer buttons (disable during processing)
- [ ] Browser back button (handle gracefully)

## 5. Error Handling

### API Errors
```typescript
const handleStartQuiz = async () => {
  if (!topic.trim()) {
    setError('Please enter a topic');
    return;
  }
  
  setLoading(true);
  setError('');
  
  try {
    const questions = await geminiService.generateAudioQuiz(topic, 5);
    setQuizState({
      questions,
      currentQuestionIndex: 0,
      score: 0,
      isPlaying: false,
      isComplete: false
    });
  } catch (error) {
    console.error('Error generating audio quiz:', error);
    setError('Failed to generate quiz. Please try again.');
  } finally {
    setLoading(false);
  }
};
```

### Speech Synthesis Errors
```typescript
const speak = (text: string) => {
  if (!window.speechSynthesis) {
    setError('Audio not supported in this browser');
    return;
  }
  
  try {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'es-ES';
    utterance.onerror = (event) => {
      console.error('Speech synthesis error:', event);
      setError('Audio playback failed');
    };
    window.speechSynthesis.speak(utterance);
  } catch (error) {
    console.error('Error in speech synthesis:', error);
    setError('Could not play audio');
  }
};
```

### User-Facing Messages
- Loading: "Generating audio quiz..."
- Success: Display quiz interface
- Error: "Error: [specific message]"
- No audio support: "Audio not available in this browser. You can still read the questions."

## 6. UI/UX Considerations

### Bootstrap Components
- **Forms**: `form-control`, `form-label` for topic input
- **Buttons**: 
  - Primary: `btn btn-primary` (Start Quiz, Play Audio)
  - Success: `btn btn-success` (Correct answer)
  - Danger: `btn btn-danger` (Wrong answer)
  - Secondary: `btn btn-secondary` (Next, Back)
- **Cards**: `card`, `card-body` for question display
- **Badges**: `badge bg-primary` for progress (Question 1/5)
- **Alerts**: `alert alert-info` for instructions

### Loading States
- Spinner during quiz generation: `spinner-border`
- Disable buttons during loading
- Show "Generating quiz..." message

### Audio Feedback
- 🔊 icon for play audio button
- Visual feedback when audio is playing (pulsing icon)
- Auto-play option (optional enhancement)

### Responsive Design
- Large, readable text for questions
- Touch-friendly buttons (min 44px height)
- Stack options vertically on mobile
- Horizontal layout on desktop

### Accessibility
- ARIA labels for buttons
- Keyboard navigation support
- High contrast for answer feedback
- Screen reader friendly

## 7. Implementation Order

1. ✅ Create feature branch `feature/audio-quiz`
2. ✅ Define types in `types.ts` (AudioQuizQuestion, AudioQuizState, AppView.AUDIO_QUIZ)
3. ✅ Implement `generateAudioQuiz()` in `geminiService.ts`
4. ✅ Create `components/AudioQuiz.tsx` with full UI
5. ✅ Update `App.tsx` routing and navigation
6. ✅ Test manually with checklist
7. ✅ Update `/docs/AI_AGENTS.md`
8. ✅ Update `/docs/DATA_MODEL.md`
9. ✅ Update `README.md`
10. ✅ Final testing and refinement
11. ✅ Commit with message: `[AudioQuiz] Add: Audio quiz generator with speech synthesis`
12. ✅ Push and create PR

## 8. Dependencies

### Existing Dependencies
- React, TypeScript
- Google Gemini API (`gemini-2.5-flash`)
- Bootstrap for UI

### Browser APIs
- **Web Speech API** (speechSynthesis)
  - Built into modern browsers
  - No installation needed
  - Fallback: Show text-only mode if not supported

### New Dependencies
- None (using native browser APIs)

## 9. Notes

- Web Speech API is supported in most modern browsers (Chrome, Edge, Safari, Firefox)
- Spanish voice (`es-ES`) should be available by default
- Consider adding voice selection option in future
- Audio playback is asynchronous - handle state carefully
- Test on different browsers for compatibility
- Consider adding keyboard shortcuts (Space to play audio, 1-4 for answers)

## 10. Next Steps After Implementation

1. Manual testing with full checklist
2. Test on different browsers (Chrome, Firefox, Safari, Edge)
3. Test on mobile devices
4. Documentation review
5. Code self-review
6. Commit and push
7. Create PR with description
8. Consider future enhancements:
   - Voice selection (male/female, different accents)
   - Speech recognition for verbal answers
   - Adjustable speech rate
   - Background music option
   - Save quiz history

## 11. Rollback Plan

If issues arise:
```bash
git checkout main
git branch -D feature/audio-quiz
```

Or if partially implemented:
```bash
git reset --hard HEAD~1  # Undo last commit
```

## 12. Success Criteria

- [ ] Quiz generates successfully from topic input
- [ ] Audio plays questions in clear Spanish
- [ ] User can answer by clicking options
- [ ] Correct/incorrect feedback is immediate and clear
- [ ] Score tracking works accurately
- [ ] Progress indicator updates correctly
- [ ] Final results display properly
- [ ] No console errors
- [ ] Responsive on all screen sizes
- [ ] Documentation fully updated
- [ ] Code follows OpositaIA standards
- [ ] User experience is smooth and intuitive
- [ ] Error handling is robust
- [ ] Accessibility requirements met

## 13. Future Enhancements (Not in This Implementation)

- Speech recognition for verbal answers
- Adjustable speech rate and voice selection
- Quiz history and statistics
- Timed mode with countdown
- Multiplayer mode
- Custom quiz creation
- Export quiz results
- Integration with study plan
