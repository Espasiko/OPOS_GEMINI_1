import React, { useState, useEffect } from 'react';
import * as vpsService from '../services/vpsService';

export const VPSTestView: React.FC = () => {
  const [health, setHealth] = useState<{ status: string; service: string } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [query, setQuery] = useState('');
  const [searchResult, setSearchResult] = useState<any>(null);

  // Check health on mount
  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      const result = await vpsService.healthCheck();
      setHealth(result);
    } catch (err) {
      console.error('Health check failed:', err);
      setHealth({ status: 'error', service: 'unavailable' });
    }
  };

  const handleSearch = async () => {
    if (!query.trim()) {
      setError('Por favor ingresa una consulta');
      return;
    }

    setLoading(true);
    setError('');
    setSearchResult(null);

    try {
      const result = await vpsService.ragSearch({
        query: query.trim(),
        top_k: 5
      });
      setSearchResult(result);
    } catch (err) {
      setError('Error al buscar: ' + (err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-4">
      <div className="row">
        <div className="col-12">
          <h1>🔌 Prueba de API VPS</h1>
          <p className="text-muted">
            Conectando con: <code>https://electroyhogarpelotazo.tienda</code>
          </p>

          {/* Health Status */}
          <div className="card mb-4">
            <div className="card-body">
              <h5 className="card-title">Estado del Servicio</h5>
              {health ? (
                <div className={`alert ${health.status === 'ok' ? 'alert-success' : 'alert-danger'}`}>
                  <strong>Estado:</strong> {health.status} <br />
                  <strong>Servicio:</strong> {health.service}
                </div>
              ) : (
                <div className="spinner-border" role="status">
                  <span className="visually-hidden">Verificando...</span>
                </div>
              )}
              <button className="btn btn-sm btn-outline-primary" onClick={checkHealth}>
                🔄 Verificar Estado
              </button>
            </div>
          </div>

          {/* RAG Search Test */}
          <div className="card mb-4">
            <div className="card-body">
              <h5 className="card-title">Búsqueda RAG</h5>
              <div className="mb-3">
                <label className="form-label">Consulta:</label>
                <input
                  type="text"
                  className="form-control"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Ej: ¿Qué es la incapacidad temporal?"
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                />
              </div>
              <button
                className="btn btn-primary"
                onClick={handleSearch}
                disabled={loading || !query.trim()}
              >
                {loading ? (
                  <>
                    <span className="spinner-border spinner-border-sm me-2"></span>
                    Buscando...
                  </>
                ) : (
                  '🔍 Buscar'
                )}
              </button>

              {error && (
                <div className="alert alert-danger mt-3">
                  {error}
                </div>
              )}

              {searchResult && (
                <div className="mt-4">
                  <h6>Respuesta:</h6>
                  <div className="alert alert-info">
                    {searchResult.answer}
                  </div>

                  {searchResult.sources && searchResult.sources.length > 0 && (
                    <>
                      <h6>Fuentes ({searchResult.sources.length}):</h6>
                      <div className="list-group">
                        {searchResult.sources.map((source: any, idx: number) => (
                          <div key={idx} className="list-group-item">
                            <div className="d-flex w-100 justify-content-between">
                              <h6 className="mb-1">Fuente {idx + 1}</h6>
                              <small>Score: {source.score?.toFixed(3)}</small>
                            </div>
                            <p className="mb-1">{source.content}</p>
                            {source.metadata && (
                              <small className="text-muted">
                                {JSON.stringify(source.metadata)}
                              </small>
                            )}
                          </div>
                        ))}
                      </div>
                    </>
                  )}

                  <div className="mt-2">
                    <small className="text-muted">
                      Modelo usado: {searchResult.model_used}
                    </small>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* API Documentation Links */}
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Documentación</h5>
              <div className="d-flex gap-2">
                <a
                  href={vpsService.getDocsUrl()}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-outline-primary btn-sm"
                >
                  📖 Swagger UI
                </a>
                <a
                  href={vpsService.getOpenAPIUrl()}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-outline-secondary btn-sm"
                >
                  📄 OpenAPI Spec
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
