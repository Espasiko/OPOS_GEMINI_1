import { describe, it, expect } from 'vitest';
import { 
  getProviderInfo,
  isProviderConfigured,
  getAvailableProviders,
  getProviderSpeed,
  getProviderCost 
} from '../providers';

describe('Providers Utility', () => {
  describe('getProviderInfo', () => {
    it('should return info for groq', () => {
      const info = getProviderInfo('groq');
      expect(info).toHaveProperty('name');
      expect(info).toHaveProperty('speed');
      expect(info).toHaveProperty('cost');
      expect(info.name).toBe('Groq');
    });

    it('should return info for deepseek', () => {
      const info = getProviderInfo('deepseek');
      expect(info.name).toBe('DeepSeek');
    });

    it('should return info for gemini', () => {
      const info = getProviderInfo('gemini');
      expect(info.name).toBe('Gemini');
    });

    it('should handle unknown provider', () => {
      const info = getProviderInfo('unknown');
      expect(info).toHaveProperty('name');
      expect(info.name).toContain('Unknown');
    });
  });

  describe('isProviderConfigured', () => {
    it('should check if provider is configured', () => {
      const result = isProviderConfigured('groq');
      expect(typeof result).toBe('boolean');
    });

    it('should return false for unknown provider', () => {
      const result = isProviderConfigured('nonexistent');
      expect(result).toBe(false);
    });
  });

  describe('getAvailableProviders', () => {
    it('should return array of providers', () => {
      const providers = getAvailableProviders();
      expect(Array.isArray(providers)).toBe(true);
      expect(providers.length).toBeGreaterThan(0);
    });

    it('should include main providers', () => {
      const providers = getAvailableProviders();
      const names = providers.map(p => p.id);
      expect(names).toContain('groq');
      expect(names).toContain('deepseek');
      expect(names).toContain('gemini');
    });

    it('should return providers with required fields', () => {
      const providers = getAvailableProviders();
      providers.forEach(provider => {
        expect(provider).toHaveProperty('id');
        expect(provider).toHaveProperty('name');
        expect(provider).toHaveProperty('speed');
        expect(provider).toHaveProperty('cost');
      });
    });
  });

  describe('getProviderSpeed', () => {
    it('should return speed rating', () => {
      const speed = getProviderSpeed('groq');
      expect(['fast', 'medium', 'slow']).toContain(speed);
    });

    it('should return groq as fast', () => {
      const speed = getProviderSpeed('groq');
      expect(speed).toBe('fast');
    });
  });

  describe('getProviderCost', () => {
    it('should return cost rating', () => {
      const cost = getProviderCost('deepseek');
      expect(['free', 'cheap', 'medium', 'expensive']).toContain(cost);
    });

    it('should return deepseek as cheap', () => {
      const cost = getProviderCost('deepseek');
      expect(cost).toBe('cheap');
    });
  });
});
