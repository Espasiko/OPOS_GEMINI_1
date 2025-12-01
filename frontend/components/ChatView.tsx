import React, { useState, useEffect, useRef, useCallback } from 'react';
import { sendChatMessageStream } from '../services/backendService';
import { useModel } from '../contexts/ModelContext';
import { ChatMessage, Conversation } from '../types';
import { SparkIcon } from './icons/SparkIcon';
import { PlusIcon } from './icons/PlusIcon';
import { ChatIcon } from './icons/ChatIcon';
import InputSourceSelector, { extractTextFromFile } from './InputSourceSelector';

/**
 * Muestra la vista del Chat Explicativo.
 * Este componente gestiona múltiples conversaciones, persistiendo el historial en localStorage.
 * Cada conversación tiene su propia instancia de chat para mantener el contexto.
 * Permite al usuario enviar mensajes de texto o cargar contexto desde archivos/URLs
 * para que la IA los analice y responda preguntas sobre ellos.
 * Las respuestas del modelo se reciben en streaming para una experiencia de usuario fluida.
 */
const ChatView: React.FC = () => {
  const BACKEND_URL = (import.meta as any).env?.VITE_BACKEND_URL || 'http://localhost:8000';
  const { selectedModel } = useModel();
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConvId, setActiveConvId] = useState<string>('');
  const [userInput, setUserInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [inputError, setInputError] = useState<string | null>(null);
  const [currentUsage, setCurrentUsage] = useState<{tokens: number; cost: number} | null>(null);

  const createNewConversation = useCallback(() => {
    const newId = `conv-${Date.now()}`;
    const newConv: Conversation = {
      id: newId,
      title: 'Nueva Conversación',
      messages: [
        {
          id: `init-${newId}`,
          role: 'model',
          text: '¡Hola! Soy tu tutor experto en legislación de la Seguridad Social. Pregúntame cualquier duda que tengas o envíame un caso práctico para que te lo explique.',
        },
      ],
    };
    setConversations(prev => [newConv, ...prev]);
    setActiveConvId(newId);
  }, []);

  useEffect(() => {
    const storedConversations = localStorage.getItem('chat_conversations');
    if (storedConversations) {
      const parsed = JSON.parse(storedConversations);
      if (Array.isArray(parsed) && parsed.length > 0) {
        setConversations(parsed);
        setActiveConvId(parsed[0].id);
        return;
      }
    }
    createNewConversation();
  }, [createNewConversation]);

  useEffect(() => {
    if (conversations.length > 0) {
      localStorage.setItem('chat_conversations', JSON.stringify(conversations));
    }
  }, [conversations]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [conversations, activeConvId]);

  const handleSendMessage = useCallback(
    async (e: React.FormEvent, textToSend?: string) => {
      e.preventDefault();
      const messageText = textToSend || userInput;
      if (!messageText.trim() || isLoading || !activeConvId) return;

      const userMessage: ChatMessage = {
        id: `user-${Date.now()}`,
        role: 'user',
        text: messageText,
      };

      const activeConv = conversations.find(c => c.id === activeConvId);
      const isFirstUserMessage = activeConv?.messages.filter(m => m.role === 'user').length === 0;

      setConversations(prev =>
        prev.map(conv =>
          conv.id === activeConvId
            ? {
                ...conv,
                title:
                  isFirstUserMessage && messageText.length > 0
                    ? messageText.substring(0, 30) + (messageText.length > 30 ? '...' : '')
                    : conv.title,
                messages: [...conv.messages, userMessage],
              }
            : conv
        )
      );

      setUserInput('');
      setIsLoading(true);

      const modelResponseId = `model-${Date.now()}`;
      setConversations(prev =>
        prev.map(conv =>
          conv.id === activeConvId
            ? {
                ...conv,
                messages: [...conv.messages, { id: modelResponseId, role: 'model', text: '' }],
              }
            : conv
        )
      );

      try {
        // Use backend service with streaming
        const stream = sendChatMessageStream({
          message: messageText,
          conversation_id: activeConvId,
          use_rag: true,
          provider: selectedModel,
          top_k: 5,
          min_score: 0.5,
        });

        for await (const chunk of stream) {
          // Check if chunk is sources metadata (skip it from display)
          if (chunk.startsWith('{') && chunk.includes('"type":"sources"')) {
            // Sources received, we could store them separately if needed
            continue;
          }
          
          // Check if chunk is usage metadata
          if (chunk.startsWith('{') && chunk.includes('"usage"')) {
            try {
              const usageData = JSON.parse(chunk);
              if (usageData.usage) {
                setCurrentUsage({
                  tokens: usageData.usage.total_tokens || 0,
                  cost: usageData.usage.total_cost_eur || 0
                });
              }
            } catch (e) {
              // Ignore parse errors
            }
            continue;
          }

          setConversations(prev =>
            prev.map(conv => {
              if (conv.id === activeConvId) {
                return {
                  ...conv,
                  messages: conv.messages.map(msg =>
                    msg.id === modelResponseId ? { ...msg, text: msg.text + chunk } : msg
                  ),
                };
              }
              return conv;
            })
          );
        }
      } catch (error) {
        console.error('Error sending message:', error);
        setConversations(prev =>
          prev.map(conv => {
            if (conv.id === activeConvId) {
              return {
                ...conv,
                messages: conv.messages.map(msg =>
                  msg.id === modelResponseId
                    ? {
                        ...msg,
                        text: 'Lo siento, ha ocurrido un error. Por favor, inténtalo de nuevo.',
                      }
                    : msg
                ),
              };
            }
            return conv;
          })
        );
      } finally {
        setIsLoading(false);
        // Reset usage after a delay so user can see it
        setTimeout(() => setCurrentUsage(null), 5000);
      }
    },
    [userInput, isLoading, activeConvId, conversations, selectedModel]
  );

  const handleDataSourceSubmit = async (
    source: { type: 'file'; content: File } | { type: 'url'; content: string }
  ) => {
    setIsLoading(true);
    setInputError(null);
    try {
      let textContent = '';
      let contextMessage = '';
      if (source.type === 'file') {
        textContent = await extractTextFromFile(source.content);
        contextMessage = `Analiza el siguiente texto del documento "${source.content.name}" y responde a mis preguntas sobre él:\n\n---\n${textContent}`;
      } else if (source.type === 'url') {
        // For URLs, we'll just send the URL and let the backend handle it
        // Or we can use a simple fetch
        const response = await fetch(source.content);
        textContent = await response.text();
        contextMessage = `Analiza el siguiente texto de la URL "${source.content}" y responde a mis preguntas sobre él:\n\n---\n${textContent}`;
      }
      // This will trigger a message send with the context.
      handleSendMessage({ preventDefault: () => {} } as React.FormEvent, contextMessage);
    } catch (err: any) {
      setInputError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectConversation = (id: string) => {
    if (id !== activeConvId) {
      setActiveConvId(id);
    }
  };

  const activeMessages = conversations.find(c => c.id === activeConvId)?.messages || [];

  return (
    <div className="flex h-full bg-white dark:bg-slate-900">
      <aside className="w-64 flex-shrink-0 bg-slate-50 dark:bg-slate-950/70 border-r border-slate-200 dark:border-slate-800 flex flex-col">
        <div className="p-4 border-b border-slate-200 dark:border-slate-800">
          <button
            onClick={createNewConversation}
            className="w-full flex items-center justify-center space-x-2 px-3 py-2 bg-blue-500 text-white rounded-lg text-sm font-medium hover:bg-blue-600 transition-colors"
          >
            <PlusIcon className="w-5 h-5" />
            <span>Nuevo Chat</span>
          </button>
        </div>
        <div className="flex-1 overflow-y-auto p-2">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider px-2 mb-2">
            Historial
          </h2>
          <ul className="space-y-1">
            {conversations.map(conv => (
              <li key={conv.id}>
                <button
                  onClick={() => handleSelectConversation(conv.id)}
                  className={`w-full text-left px-3 py-2 text-sm rounded-md truncate transition-colors flex items-center space-x-2 ${
                    activeConvId === conv.id
                      ? 'bg-slate-200 dark:bg-slate-800 font-semibold text-slate-800 dark:text-slate-100'
                      : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/50'
                  }`}
                >
                  <ChatIcon className="w-4 h-4 flex-shrink-0" />
                  <span>{conv.title}</span>
                </button>
              </li>
            ))}
          </ul>
        </div>
      </aside>
      <div className="flex flex-col flex-1 h-full">
        <header className="p-4 border-b border-slate-200 dark:border-slate-800">
          <h1 className="text-xl font-bold text-slate-800 dark:text-slate-100">Chat Explicativo</h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Tu tutor IA para resolver dudas al instante.
          </p>
        </header>
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {activeMessages.map(msg => (
            <div key={msg.id} className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : ''}`}>
              {msg.role === 'model' && (
                <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white flex-shrink-0">
                  <SparkIcon className="w-5 h-5" />
                </div>
              )}
              <div
                className={`max-w-3xl p-4 rounded-2xl shadow-sm ${msg.role === 'user' ? 'bg-blue-500 text-white rounded-br-none' : 'bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 rounded-bl-none'}`}
              >
                <div
                  className="prose prose-sm dark:prose-invert max-w-none prose-p:my-2"
                  dangerouslySetInnerHTML={{ __html: msg.text.replace(/\n/g, '<br />') }}
                ></div>
                {msg.text === '' && isLoading && (
                  <div className="flex items-center space-x-2">
                    <span className="w-2 h-2 bg-slate-500 rounded-full animate-pulse delay-75"></span>
                    <span className="w-2 h-2 bg-slate-500 rounded-full animate-pulse delay-150"></span>
                    <span className="w-2 h-2 bg-slate-500 rounded-full animate-pulse delay-300"></span>
                  </div>
                )}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
        {currentUsage && (
          <div className="px-4 py-2 bg-slate-50 dark:bg-slate-800 border-t border-slate-200 dark:border-slate-700">
            <div className="text-xs text-slate-500 dark:text-slate-400 flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <span className="flex items-center">
                <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10 3.5a1.5 1.5 0 013 0V4a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-.5a1.5 1.5 0 000 3h.5a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-.5a1.5 1.5 0 00-3 0v.5a1 1 0 01-1 1H6a1 1 0 01-1-1v-3a1 1 0 00-1-1h-.5a1.5 1.5 0 010-3H4a1 1 0 001-1V6a1 1 0 011-1h3a1 1 0 001-1v-.5z" />
                </svg>
                {currentUsage.tokens.toLocaleString()} tokens
              </span>
              <span className="flex items-center">
                <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z" />
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clipRule="evenodd" />
                </svg>
                €{currentUsage.cost.toFixed(6)}
              </span>
              </div>
              <div>
                <a
                  href={`${BACKEND_URL}/chat/usage/export`}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center px-2 py-1 rounded-md border border-slate-300 dark:border-slate-600 hover:bg-slate-100 dark:hover:bg-slate-700 text-xs"
                >
                  Exportar uso (CSV)
                </a>
              </div>
            </div>
          </div>
        )}
        <div className="p-4 border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900">
          <InputSourceSelector
            onTextSubmit={handleDataSourceSubmit}
            isLoading={isLoading}
            error={inputError}
            showTextField={false}
          />
          <form onSubmit={handleSendMessage} className="relative mt-2">
            <textarea
              value={userInput}
              onChange={e => setUserInput(e.target.value)}
              placeholder="Escribe tu pregunta aquí, o sube un documento arriba..."
              disabled={isLoading}
              rows={1}
              onKeyDown={e => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  handleSendMessage(e);
                }
              }}
              className="w-full px-4 py-3 pr-12 bg-slate-100 dark:bg-slate-800 border border-transparent rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 dark:text-white transition-all resize-none leading-tight"
            />
            <button
              type="submit"
              disabled={isLoading || !userInput.trim()}
              className="absolute right-2 top-1/2 -translate-y-1/2 w-9 h-9 flex items-center justify-center bg-blue-500 text-white rounded-full disabled:bg-slate-400 dark:disabled:bg-slate-600 hover:bg-blue-600 transition-colors"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
              </svg>
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ChatView;
