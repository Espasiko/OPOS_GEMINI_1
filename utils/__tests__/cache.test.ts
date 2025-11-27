import { describe, it, expect, beforeEach, vi } from 'vitest';
import { CacheManager } from '../cache';

describe('Cache Utility', () => {
  let cache: CacheManager;

  beforeEach(() => {
    cache = new CacheManager();
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('should store and retrieve values', () => {
    cache.set('key1', 'value1');
    expect(cache.get('key1')).toBe('value1');
  });

  it('should return null for non-existent keys', () => {
    expect(cache.get('nonexistent')).toBe(null);
  });

  it('should expire values after TTL', () => {
    cache.set('key1', 'value1', 1000); // 1 second TTL
    
    expect(cache.get('key1')).toBe('value1');
    
    // Advance time by 1.5 seconds
    vi.advanceTimersByTime(1500);
    
    expect(cache.get('key1')).toBe(null);
  });

  it('should clear all cache', () => {
    cache.set('key1', 'value1');
    cache.set('key2', 'value2');
    
    cache.clear();
    
    expect(cache.get('key1')).toBe(null);
    expect(cache.get('key2')).toBe(null);
  });

  it('should handle complex objects', () => {
    const obj = { name: 'test', data: [1, 2, 3] };
    cache.set('obj', obj);
    
    expect(cache.get('obj')).toEqual(obj);
  });

  it('should update existing keys', () => {
    cache.set('key1', 'value1');
    cache.set('key1', 'value2');
    
    expect(cache.get('key1')).toBe('value2');
  });

  it('should handle default TTL', () => {
    cache.set('key1', 'value1'); // Uses default TTL (5 min)
    
    expect(cache.get('key1')).toBe('value1');
    
    // Advance time by 4 minutes (should still exist)
    vi.advanceTimersByTime(4 * 60 * 1000);
    expect(cache.get('key1')).toBe('value1');
    
    // Advance time by 2 more minutes (should expire)
    vi.advanceTimersByTime(2 * 60 * 1000);
    expect(cache.get('key1')).toBe(null);
  });
});
