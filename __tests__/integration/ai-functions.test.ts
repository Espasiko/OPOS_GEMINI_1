import { describe, it, expect, vi, beforeEach } from 'vitest';
import * as backendService from '../../services/backendService';

describe('AI Functions Integration', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('Summary Generation', () => {
    it('should generate summary from text', async () => {
      const mockSummary = {
        summary: 'This is a summary',
        keyPoints: ['Point 1', 'Point 2']
      };

      vi.spyOn(backendService, 'generateSummary').mockResolvedValue(mockSummary);

      const result = await backendService.generateSummary(
        'Long text to summarize',
        'groq'
      );

      expect(result).toHaveProperty('summary');
      expect(result.summary).toBeTruthy();
    });

    it('should handle empty text', async () => {
      vi.spyOn(backendService, 'generateSummary').mockRejectedValue(
        new Error('Empty text')
      );

      await expect(
        backendService.generateSummary('', 'groq')
      ).rejects.toThrow();
    });
  });

  describe('Mind Map Generation', () => {
    it('should generate mind map structure', async () => {
      const mockMindMap = {
        title: 'Main Topic',
        children: [
          { title: 'Subtopic 1', children: [] },
          { title: 'Subtopic 2', children: [] }
        ]
      };

      vi.spyOn(backendService, 'generateMindMap').mockResolvedValue(mockMindMap);

      const result = await backendService.generateMindMap(
        'Topic to map',
        'groq'
      );

      expect(result).toHaveProperty('title');
      expect(result).toHaveProperty('children');
      expect(Array.isArray(result.children)).toBe(true);
    });
  });

  describe('Flashcards Generation', () => {
    it('should generate flashcards array', async () => {
      const mockFlashcards = [
        { front: 'Question 1', back: 'Answer 1' },
        { front: 'Question 2', back: 'Answer 2' }
      ];

      vi.spyOn(backendService, 'generateFlashcards').mockResolvedValue(mockFlashcards);

      const result = await backendService.generateFlashcards(
        'Content for flashcards',
        'groq'
      );

      expect(Array.isArray(result)).toBe(true);
      expect(result.length).toBeGreaterThan(0);
      expect(result[0]).toHaveProperty('front');
      expect(result[0]).toHaveProperty('back');
    });

    it('should handle minimum flashcards count', async () => {
      const mockFlashcards = [
        { front: 'Q1', back: 'A1' },
        { front: 'Q2', back: 'A2' },
        { front: 'Q3', back: 'A3' }
      ];

      vi.spyOn(backendService, 'generateFlashcards').mockResolvedValue(mockFlashcards);

      const result = await backendService.generateFlashcards(
        'Content',
        'groq',
        3
      );

      expect(result.length).toBeGreaterThanOrEqual(3);
    });
  });

  describe('Schema Generation', () => {
    it('should generate schema structure', async () => {
      const mockSchema = {
        title: 'Schema Title',
        sections: [
          { title: 'Section 1', content: 'Content 1' },
          { title: 'Section 2', content: 'Content 2' }
        ]
      };

      vi.spyOn(backendService, 'generateSchema').mockResolvedValue(mockSchema);

      const result = await backendService.generateSchema(
        'Topic for schema',
        'groq'
      );

      expect(result).toHaveProperty('title');
      expect(result).toHaveProperty('sections');
      expect(Array.isArray(result.sections)).toBe(true);
    });
  });

  describe('Study Plan Generation', () => {
    it('should generate study plan', async () => {
      const mockPlan = {
        title: 'Study Plan',
        weeks: [
          { week: 1, topics: ['Topic 1', 'Topic 2'] },
          { week: 2, topics: ['Topic 3', 'Topic 4'] }
        ]
      };

      vi.spyOn(backendService, 'generateStudyPlan').mockResolvedValue(mockPlan);

      const result = await backendService.generateStudyPlan(
        'Subject to study',
        'groq',
        4
      );

      expect(result).toHaveProperty('title');
      expect(result).toHaveProperty('weeks');
      expect(Array.isArray(result.weeks)).toBe(true);
    });
  });

  describe('Practical Case Generation', () => {
    it('should generate practical case', async () => {
      const mockCase = {
        title: 'Case Title',
        scenario: 'Case scenario description',
        questions: ['Question 1', 'Question 2'],
        solution: 'Solution explanation'
      };

      vi.spyOn(backendService, 'generatePracticalCase').mockResolvedValue(mockCase);

      const result = await backendService.generatePracticalCase(
        'Topic for case',
        'groq'
      );

      expect(result).toHaveProperty('title');
      expect(result).toHaveProperty('scenario');
      expect(result).toHaveProperty('questions');
      expect(result).toHaveProperty('solution');
    });
  });
});
