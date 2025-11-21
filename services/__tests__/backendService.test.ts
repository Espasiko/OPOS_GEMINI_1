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
});
