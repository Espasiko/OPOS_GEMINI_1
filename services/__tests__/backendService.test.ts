/**
 * Tests for Backend Service
 * Sprint 7 - Fase 2
 */

import { describe, it, expect, beforeAll, vi } from 'vitest';
import {
  checkBackendHealth,
  checkChatHealth,
  checkUploadHealth,
  sendChatMessage,
  uploadFile,
  generatePracticalCase,
  generateMindMap,
  generateFlashcards,
  generateSchema,
  generateSummary,
  compareTexts,
  generateStudyPlan,
  checkAIHealth,
} from '../backendService';

// Mock fetch globally
global.fetch = vi.fn();

describe('Backend Service', () => {
  beforeAll(() => {
    // Reset mocks before each test
    vi.clearAllMocks();
  });

  describe('Health Checks', () => {
    it('should check backend health', async () => {
      const mockResponse = {
        status: 'healthy',
        services: {
          rag: 'up',
          mistral: 'up',
          upload: 'up',
        },
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await checkBackendHealth();
      expect(result).toEqual(mockResponse);
      expect(global.fetch).toHaveBeenCalledWith(expect.stringContaining('/health'));
    });

    it('should check chat health', async () => {
      const mockResponse = {
        status: 'healthy',
        mistral: 'up',
        rag: 'up',
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await checkChatHealth();
      expect(result).toEqual(mockResponse);
      expect(global.fetch).toHaveBeenCalledWith(expect.stringContaining('/chat/health'));
    });

    it('should check upload health', async () => {
      const mockResponse = {
        status: 'healthy',
        cached_documents: 0,
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await checkUploadHealth();
      expect(result).toEqual(mockResponse);
      expect(global.fetch).toHaveBeenCalledWith(expect.stringContaining('/upload/health'));
    });
  });

  describe('Chat Operations', () => {
    it('should send chat message', async () => {
      const mockResponse = {
        response: 'Test response',
        sources: [],
        conversation_id: 'test-123',
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await sendChatMessage({
        message: 'Test message',
        conversation_id: 'test-123',
        use_rag: false,
      });

      expect(result).toEqual(mockResponse);
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/chat/message'),
        expect.objectContaining({
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        })
      );
    });

    it('should handle chat errors', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: false,
        statusText: 'Internal Server Error',
        json: async () => ({ detail: 'Test error' }),
      });

      await expect(
        sendChatMessage({
          message: 'Test',
          conversation_id: 'test',
        })
      ).rejects.toThrow();
    });
  });

  describe('Upload Operations', () => {
    it('should upload file', async () => {
      const mockFile = new File(['test content'], 'test.txt', { type: 'text/plain' });
      const mockResponse = {
        document_id: 'doc-123',
        filename: 'test.txt',
        text_length: 12,
        indexed: false,
        text_preview: 'test content',
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await uploadFile(mockFile);
      expect(result).toEqual(mockResponse);
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/upload/file'),
        expect.objectContaining({
          method: 'POST',
        })
      );
    });

    it('should handle upload errors', async () => {
      const mockFile = new File(['test'], 'test.txt', { type: 'text/plain' });

      (global.fetch as any).mockResolvedValueOnce({
        ok: false,
        statusText: 'Bad Request',
        json: async () => ({ detail: 'Unsupported file type' }),
      });

      await expect(uploadFile(mockFile)).rejects.toThrow();
    });
  });

  describe('AI Functions (Sprint 9)', () => {
    it('should generate practical case', async () => {
      const mockResponse = {
        scenario: 'Test scenario',
        questions: [
          { question: 'Question 1', points: 5 },
          { question: 'Question 2', points: 5 },
        ],
        total_points: 10,
        estimated_time: 30,
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await generatePracticalCase({
        topic: 'IT',
        difficulty: 'medium',
        provider: 'groq',
      });

      expect(result).toEqual(mockResponse);
      expect(result.questions).toHaveLength(2);
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/ai/practical-case'),
        expect.objectContaining({ method: 'POST' })
      );
    });

    it('should generate mind map', async () => {
      const mockResponse = {
        root: {
          label: 'Test Topic',
          children: [
            { label: 'Subtopic 1' },
            { label: 'Subtopic 2' },
          ],
        },
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await generateMindMap({
        topic: 'Test Topic',
        depth: 2,
        provider: 'groq',
      });

      expect(result).toEqual(mockResponse);
      expect(result.root.children).toHaveLength(2);
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/ai/mind-map'),
        expect.objectContaining({ method: 'POST' })
      );
    });

    it('should generate flashcards', async () => {
      const mockResponse = {
        cards: [
          { front: 'Question 1', back: 'Answer 1', difficulty: 'easy' },
          { front: 'Question 2', back: 'Answer 2', difficulty: 'medium' },
        ],
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await generateFlashcards({
        topic: 'Test',
        count: 2,
        provider: 'groq',
      });

      expect(result).toEqual(mockResponse);
      expect(result.cards).toHaveLength(2);
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/ai/flashcards'),
        expect.objectContaining({ method: 'POST' })
      );
    });

    it('should generate schema', async () => {
      const mockResponse = {
        title: 'Test Schema',
        sections: [
          {
            title: 'Section 1',
            content: ['Point 1', 'Point 2'],
          },
        ],
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await generateSchema({
        topic: 'Test',
        format: 'outline',
        provider: 'groq',
      });

      expect(result).toEqual(mockResponse);
      expect(result.sections).toHaveLength(1);
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/ai/schema'),
        expect.objectContaining({ method: 'POST' })
      );
    });

    it('should generate summary', async () => {
      const mockResponse = {
        summary: 'Test summary',
        key_points: ['Point 1', 'Point 2'],
        word_count: 50,
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await generateSummary({
        text: 'Long text to summarize',
        length: 'short',
        provider: 'groq',
      });

      expect(result).toEqual(mockResponse);
      expect(result.key_points).toHaveLength(2);
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/ai/summary'),
        expect.objectContaining({ method: 'POST' })
      );
    });

    it('should compare texts', async () => {
      const mockResponse = {
        similarities: ['Similar point 1'],
        differences: ['Different point 1'],
        conclusion: 'Test conclusion',
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await compareTexts({
        text1: 'Text 1',
        text2: 'Text 2',
        provider: 'groq',
      });

      expect(result).toEqual(mockResponse);
      expect(result.similarities).toHaveLength(1);
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/ai/compare'),
        expect.objectContaining({ method: 'POST' })
      );
    });

    it('should generate study plan', async () => {
      const mockResponse = {
        title: 'Test Study Plan',
        total_weeks: 4,
        total_hours: 40,
        weeks: [
          {
            week: 1,
            topics: ['Topic 1'],
            activities: ['Activity 1'],
            goals: ['Goal 1'],
          },
        ],
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await generateStudyPlan({
        topic: 'Test',
        duration_weeks: 4,
        hours_per_week: 10,
        provider: 'groq',
      });

      expect(result).toEqual(mockResponse);
      expect(result.weeks).toHaveLength(1);
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/ai/study-plan'),
        expect.objectContaining({ method: 'POST' })
      );
    });

    it('should check AI health', async () => {
      const mockResponse = {
        status: 'healthy',
        providers_available: 7,
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await checkAIHealth();
      expect(result).toEqual(mockResponse);
      expect(global.fetch).toHaveBeenCalledWith(expect.stringContaining('/ai/health'));
    });

    it('should handle AI function errors', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: false,
        statusText: 'Internal Server Error',
        json: async () => ({ detail: 'Provider error' }),
      });

      await expect(
        generatePracticalCase({
          topic: 'Test',
          difficulty: 'easy',
        })
      ).rejects.toThrow();
    });
  });
});
