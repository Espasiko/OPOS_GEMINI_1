# Scripts Archivados (Sesión 20/12/2025)

Estos scripts fueron creados durante la sesión de depuración e integración del Agente Mistral con RAG. Se archivan para limpiar la raíz del proyecto, ya que han sido reemplazados por una versión final estable o eran pruebas temporales.

## Scripts Archivados

| Script | Descripción | Razón de Archivo |
|--------|-------------|------------------|
| `debug_rag_scores.py` | Script de diagnóstico para verificar scores raw de Qdrant. | Cumplió su función de diagnóstico. No se necesita en producción. |
| `test_rag_mistral.py` | Test inicial de conexión RAG. | Supersedido por `generate_qa_mistral_real.py`. |
| `test_mistral_agent_simple.py` | Test simple de conectividad con Mistral Agent. | Pruebas iniciales completadas. |
| `generate_qa_mistral_hf.py` | Intentos con HuggingFace Inference API. | Se optó por usar Mistral Agent Studio oficial. |
| `generate_qa_mistral_agent.py` | Primera versión del generador con agente. | Tenía problemas con tool_calls y conexión falsa. |
| `generate_10_qa_mistral_v2.py` | Versión mejorada con loop de tool_calls. | Evolucionó a la versión "real" conectada al backend. |
| `generate_10_qa_mistral_studio.py` | Script intermedio para Mistral Studio. | Reemplazado por `generate_qa_mistral_real.py`. |
| `call_mistral_agent.py` | Llamada simple al agente. | Demasiado básico. |

## Script PRINCIPAL (Mantener en raíz)

*   **`generate_qa_mistral_real.py`**: Este es el **script definitivo**. Conecta correctamente con el backend FastAPI, maneja timeouts, parsea correctamente la respuesta `documents` y genera los JSONL finales.
