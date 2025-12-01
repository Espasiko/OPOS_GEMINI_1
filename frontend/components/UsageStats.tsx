import { useEffect, useState } from 'react';

interface SummaryResponse {
  totalRequests: number;
  totalTokens: number;
  totalCost: number;
  byProvider: Record<string, { requests: number; tokens: number; cost: number }>;
}

export const UsageStats: React.FC = () => {
  const BACKEND_URL = (import.meta as any).env?.VITE_BACKEND_URL || 'http://localhost:8000';
  const [summary, setSummary] = useState<SummaryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [filters, setFilters] = useState<{ from?: string; to?: string; user_id?: string; provider?: string }>({});

  useEffect(() => {
    const fetchSummary = async () => {
      setLoading(true);
      setError(null);
      try {
        const params = new URLSearchParams();
        if (filters.from) params.set('from_ts', filters.from);
        if (filters.to) params.set('to_ts', filters.to);
        if (filters.user_id) params.set('user_id', filters.user_id);
        if (filters.provider) params.set('provider', filters.provider);
        const res = await fetch(`${BACKEND_URL}/chat/usage/summary?${params.toString()}`);
        const data = await res.json();
        setSummary(data);
      } catch (e: any) {
        setError(e.message || 'Error al cargar el resumen');
      } finally {
        setLoading(false);
      }
    };
    fetchSummary();
  }, [filters, BACKEND_URL]);

  return (
    <div className="p-4">
      <h2 className="text-lg font-semibold mb-2">Estadísticas de Uso</h2>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-2 mb-4">
        <div>
          <label className="text-xs text-slate-500">Desde</label>
          <input type="datetime-local" className="w-full border rounded px-2 py-1"
            value={filters.from || ''}
            onChange={(e) => setFilters(f => ({ ...f, from: e.target.value }))}
          />
        </div>
        <div>
          <label className="text-xs text-slate-500">Hasta</label>
          <input type="datetime-local" className="w-full border rounded px-2 py-1"
            value={filters.to || ''}
            onChange={(e) => setFilters(f => ({ ...f, to: e.target.value }))}
          />
        </div>
        <div>
          <label className="text-xs text-slate-500">Usuario</label>
          <input type="text" placeholder="user_id" className="w-full border rounded px-2 py-1"
            value={filters.user_id || ''}
            onChange={(e) => setFilters(f => ({ ...f, user_id: e.target.value }))}
          />
        </div>
        <div>
          <label className="text-xs text-slate-500">Proveedor</label>
          <input type="text" placeholder="provider id" className="w-full border rounded px-2 py-1"
            value={filters.provider || ''}
            onChange={(e) => setFilters(f => ({ ...f, provider: e.target.value }))}
          />
        </div>
      </div>

      {loading && <p className="text-sm text-slate-500">Cargando…</p>}
      {error && <p className="text-sm text-red-600">{error}</p>}

      {summary && (
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-3 border rounded">
              <div className="text-xs text-slate-500">Total peticiones</div>
              <div className="text-xl font-bold">{summary.totalRequests.toLocaleString()}</div>
            </div>
            <div className="p-3 border rounded">
              <div className="text-xs text-slate-500">Total tokens</div>
              <div className="text-xl font-bold">{summary.totalTokens.toLocaleString()}</div>
            </div>
            <div className="p-3 border rounded">
              <div className="text-xs text-slate-500">Coste total (€)</div>
              <div className="text-xl font-bold">€{summary.totalCost.toFixed(6)}</div>
            </div>
          </div>

          <div>
            <h3 className="text-md font-semibold mb-2">Por proveedor</h3>
            <table className="w-full text-sm border">
              <thead>
                <tr className="bg-slate-100">
                  <th className="text-left p-2 border">Proveedor</th>
                  <th className="text-right p-2 border">Peticiones</th>
                  <th className="text-right p-2 border">Tokens</th>
                  <th className="text-right p-2 border">Coste (€)</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(summary.byProvider).map(([pid, stats]) => (
                  <tr key={pid}>
                    <td className="p-2 border">{pid || 'unknown'}</td>
                    <td className="p-2 border text-right">{stats.requests.toLocaleString()}</td>
                    <td className="p-2 border text-right">{stats.tokens.toLocaleString()}</td>
                    <td className="p-2 border text-right">€{stats.cost.toFixed(6)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default UsageStats;
