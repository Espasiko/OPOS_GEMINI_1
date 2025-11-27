import { describe, it, expect } from 'vitest';
import { 
  formatMarkdownToText,
  formatTextToMarkdown,
  formatMindMapData,
  formatFlashcardsData 
} from '../formatters';

describe('Formatters Utility', () => {
  describe('formatMarkdownToText', () => {
    it('should remove markdown headers', () => {
      const input = '# Title\n## Subtitle\nContent';
      const output = formatMarkdownToText(input);
      expect(output).not.toContain('#');
      expect(output).toContain('Title');
    });

    it('should remove markdown bold', () => {
      const input = '**Bold text**';
      const output = formatMarkdownToText(input);
      expect(output).toBe('Bold text');
    });

    it('should remove markdown italic', () => {
      const input = '*Italic text*';
      const output = formatMarkdownToText(input);
      expect(output).toBe('Italic text');
    });

    it('should handle empty string', () => {
      expect(formatMarkdownToText('')).toBe('');
    });
  });

  describe('formatTextToMarkdown', () => {
    it('should convert plain text to markdown', () => {
      const input = 'Simple text';
      const output = formatTextToMarkdown(input);
      expect(output).toContain(input);
    });

    it('should preserve line breaks', () => {
      const input = 'Line 1\nLine 2\nLine 3';
      const output = formatTextToMarkdown(input);
      expect(output.split('\n').length).toBeGreaterThanOrEqual(3);
    });
  });

  describe('formatMindMapData', () => {
    it('should parse mind map JSON', () => {
      const json = {
        title: 'Main Topic',
        children: [
          { title: 'Subtopic 1' },
          { title: 'Subtopic 2' }
        ]
      };
      
      const result = formatMindMapData(JSON.stringify(json));
      expect(result).toHaveProperty('title');
      expect(result.children).toHaveLength(2);
    });

    it('should handle invalid JSON', () => {
      const result = formatMindMapData('invalid json');
      expect(result).toHaveProperty('title');
      expect(result.title).toContain('Error');
    });

    it('should handle empty input', () => {
      const result = formatMindMapData('');
      expect(result).toHaveProperty('title');
    });
  });

  describe('formatFlashcardsData', () => {
    it('should parse flashcards array', () => {
      const json = [
        { front: 'Question 1', back: 'Answer 1' },
        { front: 'Question 2', back: 'Answer 2' }
      ];
      
      const result = formatFlashcardsData(JSON.stringify(json));
      expect(result).toHaveLength(2);
      expect(result[0]).toHaveProperty('front');
      expect(result[0]).toHaveProperty('back');
    });

    it('should handle invalid JSON', () => {
      const result = formatFlashcardsData('invalid');
      expect(Array.isArray(result)).toBe(true);
      expect(result.length).toBeGreaterThan(0);
    });

    it('should handle empty array', () => {
      const result = formatFlashcardsData('[]');
      expect(result).toHaveLength(0);
    });
  });
});
