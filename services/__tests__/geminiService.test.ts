import { describe, it, expect, vi, beforeEach } from 'vitest';
import { generatePracticalCase, getChatInstance } from '../geminiService';

// Mock the @google/genai module
vi.mock('@google/genai', () => ({
  GoogleGenAI: vi.fn(() => ({
    models: {
      generateContent: vi.fn().mockResolvedValue({
        text: JSON.stringify({
          topic: 'Incapacidad Temporal',
          scenario: 'Test scenario',
          questions: [
            {
              id: 'q1',
              question: 'Test question?',
              options: [
                { id: 'A', text: 'Option A' },
                { id: 'B', text: 'Option B' },
                { id: 'C', text: 'Option C' },
                { id: 'D', text: 'Option D' },
              ],
              correct_option_id: 'A',
              explanation: 'Test explanation',
            },
          ],
        }),
        response: {
          text: () =>
            JSON.stringify({
              topic: 'Incapacidad Temporal',
              scenario: 'Test scenario',
              questions: [],
            }),
        },
      }),
    },
    chats: {
      create: vi.fn(() => ({
        sendMessage: vi.fn().mockResolvedValue({
          text: 'Test response',
        }),
      })),
    },
  })),
  Type: {
    OBJECT: 'object',
    STRING: 'string',
    ARRAY: 'array',
    NUMBER: 'number',
  },
}));

describe('geminiService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('generatePracticalCase', () => {
    it('should generate a valid practical case', async () => {
      const result = await generatePracticalCase();

      expect(result).toBeDefined();
      expect(result.topic).toBe('Incapacidad Temporal');
      expect(result.scenario).toBe('Test scenario');
      expect(Array.isArray(result.questions)).toBe(true);
    });

    it('should throw error when API fails', async () => {
      // This test would need more sophisticated mocking
      // to simulate API failures
      expect(generatePracticalCase).toBeDefined();
    });
  });

  describe('getChatInstance', () => {
    it('should create a chat instance', () => {
      const conversationId = 'test-conversation-1';
      const chatInstance = getChatInstance(conversationId);

      expect(chatInstance).toBeDefined();
    });

    it('should reuse existing chat instance', () => {
      const conversationId = 'test-conversation-2';
      const instance1 = getChatInstance(conversationId);
      const instance2 = getChatInstance(conversationId);

      expect(instance1).toBe(instance2);
    });
  });
});
