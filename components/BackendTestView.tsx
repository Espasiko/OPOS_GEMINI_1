import React, { useState } from 'react';
import {
  checkBackendHealth,
  checkChatHealth,
  checkUploadHealth,
  sendChatMessage,
  uploadFile,
  getBackendInfo,
} from '../services/backendService';

/**
 * Backend Test View - Sprint 7
 * 
 * Component to test backend connectivity and functionality
 */
const BackendTestView: React.FC = () => {
  const [results, setResults] = useState<Record<string, any>>({});
  const [loading, setLoading] = useState<Record<string, boolean>>({});
  const [testMessage, setTestMessage] = useState('¿Qué es la incapacidad temporal?');

  const runTest = async (testName: string, testFn: () => Promise<any>) => {
    setLoading(prev => ({ ...prev, [testName]: true }));
    try {
      const result = await testFn();
      setResults(prev => ({
        ...prev,
        [testName]: { success: true, data: result },
      }));
    } catch (error: any) {
      setResults(prev => ({
        ...prev,
        [testName]: { success: false, error: error.message },
      }));
    } finally {
      setLoading(prev => ({ ...prev, [testName]: false }));
    }
  };

  const tests = [
    {
      name: 'Backend Info',
      fn: () => getBackendInfo(),
    },
    {
      name: 'Backend Health',
      fn: () => checkBackendHealth(),
    },
    {
      name: 'Chat Health',
      fn: () => checkChatHealth(),
    },
    {
      name: 'Upload Health',
      fn: () => checkUploadHealth(),
    },
    {
      name: 'Chat Message (No RAG)',
      fn: () =>
        sendChatMessage({
          message: testMessage,
          conversation_id: 'test-' + Date.now(),
          use_rag: false,
        }),
    },
    {
      name: 'Chat Message (With RAG)',
      fn: () =>
        sendChatMessage({
          message: testMessage,
          conversation_id: 'test-' + Date.now(),
          use_rag: true,
          top_k: 3,
        }),
    },
  ];

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    await runTest('File Upload', () => uploadFile(file));
  };

  const runAllTests = async () => {
    for (const test of tests) {
      await runTest(test.name, test.fn);
      // Small delay between tests
      await new Promise(resolve => setTimeout(resolve, 500));
    }
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-800 dark:text-slate-100 mb-2">
          🧪 Backend Connectivity Tests
        </h1>
        <p className="text-slate-600 dark:text-slate-400">
          Sprint 7 - Fase 2: Testing backend integration
        </p>
      </div>

      {/* Test Message Input */}
      <div className="mb-6 p-4 bg-slate-50 dark:bg-slate-800 rounded-lg">
        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
          Test Message for Chat:
        </label>
        <input
          type="text"
          value={testMessage}
          onChange={e => setTestMessage(e.target.value)}
          className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-md bg-white dark:bg-slate-700 text-slate-800 dark:text-slate-200"
          placeholder="Enter test message..."
        />
      </div>

      {/* Run All Button */}
      <div className="mb-6">
        <button
          onClick={runAllTests}
          disabled={Object.values(loading).some(Boolean)}
          className="px-6 py-3 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 disabled:bg-slate-400 transition-colors"
        >
          {Object.values(loading).some(Boolean) ? '⏳ Running Tests...' : '▶️ Run All Tests'}
        </button>
      </div>

      {/* Individual Tests */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {tests.map(test => (
          <div key={test.name} className="p-4 bg-white dark:bg-slate-800 rounded-lg shadow-sm border border-slate-200 dark:border-slate-700">
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-semibold text-slate-800 dark:text-slate-100">{test.name}</h3>
              <button
                onClick={() => runTest(test.name, test.fn)}
                disabled={loading[test.name]}
                className="px-3 py-1 text-sm bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 rounded hover:bg-slate-200 dark:hover:bg-slate-600 disabled:opacity-50 transition-colors"
              >
                {loading[test.name] ? '⏳' : '▶️'} Test
              </button>
            </div>

            {results[test.name] && (
              <div className="mt-2">
                {results[test.name].success ? (
                  <div>
                    <div className="flex items-center text-green-600 dark:text-green-400 text-sm font-medium mb-2">
                      <span className="mr-2">✅</span>
                      Success
                    </div>
                    <pre className="text-xs bg-slate-50 dark:bg-slate-900 p-2 rounded overflow-auto max-h-40 text-slate-700 dark:text-slate-300">
                      {JSON.stringify(results[test.name].data, null, 2)}
                    </pre>
                  </div>
                ) : (
                  <div>
                    <div className="flex items-center text-red-600 dark:text-red-400 text-sm font-medium mb-2">
                      <span className="mr-2">❌</span>
                      Failed
                    </div>
                    <p className="text-xs text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 p-2 rounded">
                      {results[test.name].error}
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* File Upload Test */}
      <div className="p-4 bg-white dark:bg-slate-800 rounded-lg shadow-sm border border-slate-200 dark:border-slate-700">
        <h3 className="font-semibold text-slate-800 dark:text-slate-100 mb-3">File Upload Test</h3>
        <input
          type="file"
          accept=".pdf,.txt"
          onChange={handleFileUpload}
          disabled={loading['File Upload']}
          className="block w-full text-sm text-slate-500 dark:text-slate-400
            file:mr-4 file:py-2 file:px-4
            file:rounded-md file:border-0
            file:text-sm file:font-semibold
            file:bg-blue-50 file:text-blue-700
            hover:file:bg-blue-100
            dark:file:bg-blue-900/20 dark:file:text-blue-400
            dark:hover:file:bg-blue-900/30"
        />
        {loading['File Upload'] && (
          <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">⏳ Uploading...</p>
        )}
        {results['File Upload'] && (
          <div className="mt-3">
            {results['File Upload'].success ? (
              <div>
                <div className="flex items-center text-green-600 dark:text-green-400 text-sm font-medium mb-2">
                  <span className="mr-2">✅</span>
                  Upload Success
                </div>
                <pre className="text-xs bg-slate-50 dark:bg-slate-900 p-2 rounded overflow-auto max-h-40 text-slate-700 dark:text-slate-300">
                  {JSON.stringify(results['File Upload'].data, null, 2)}
                </pre>
              </div>
            ) : (
              <div>
                <div className="flex items-center text-red-600 dark:text-red-400 text-sm font-medium mb-2">
                  <span className="mr-2">❌</span>
                  Upload Failed
                </div>
                <p className="text-xs text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 p-2 rounded">
                  {results['File Upload'].error}
                </p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Instructions */}
      <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
        <h3 className="font-semibold text-blue-800 dark:text-blue-300 mb-2">📝 Instructions</h3>
        <ul className="text-sm text-blue-700 dark:text-blue-400 space-y-1">
          <li>• Make sure the backend is running on <code className="bg-blue-100 dark:bg-blue-900/40 px-1 rounded">http://localhost:8000</code></li>
          <li>• Check that VITE_BACKEND_URL is set correctly in .env</li>
          <li>• Run individual tests or all tests at once</li>
          <li>• Green ✅ = Success, Red ❌ = Failed</li>
        </ul>
      </div>
    </div>
  );
};

export default BackendTestView;
