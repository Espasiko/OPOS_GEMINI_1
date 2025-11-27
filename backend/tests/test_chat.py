"""
Tests for Chat Router
Sprint 7 - Fase 1
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
import sys
from pathlib import Path
import json

sys.path.append(str(Path(__file__).parent.parent))
from main import app

client = TestClient(app)


class TestChatRouter:
    """Test suite for chat router"""
    
    def test_chat_health(self):
        """Test chat health endpoint"""
        response = client.get("/chat/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "mistral" in data
        assert "rag" in data
    
    def test_chat_message_structure(self):
        """Test chat message endpoint structure (without external dependencies)"""
        # This test will fail if Mistral is down, but validates the endpoint exists
        response = client.post("/chat/message", json={
            "message": "test",
            "conversation_id": "test-123",
            "use_rag": False  # Don't use RAG to avoid dependencies
        })
        
        # Should not be 404 (endpoint exists)
        assert response.status_code != 404
        
        # If it's 503, Mistral is down (expected in test environment)
        # If it's 200, great!
        # If it's 422, validation error
        assert response.status_code in [200, 422, 500, 503]
    
    def test_chat_message_validation(self):
        """Test request validation"""
        # Missing required fields
        response = client.post("/chat/message", json={})
        assert response.status_code == 422

    # ========== NEW TESTS ==========
    
    @patch('routers.chat.get_provider')
    @patch('routers.chat.get_rag_agent')
    def test_stream_sse_chunks_with_done(self, mock_rag_agent, mock_get_provider):
        """Should stream SSE chunks and end with [DONE] when provider streams successfully"""
        # Mock RAG to return no results (simplify test)
        mock_rag_instance = AsyncMock()
        mock_rag_instance.search_documents = AsyncMock(return_value=[])
        mock_rag_agent.return_value = mock_rag_instance
        
        # Mock provider to stream content
        mock_provider = MagicMock()
        mock_provider.get_info.return_value = {"name": "Test Provider"}
        
        async def mock_stream(messages, temperature, max_tokens):
            """Simulate streaming chunks"""
            for chunk in ["Hello", " ", "world", "!"]:
                yield chunk
        
        mock_provider.generate_stream = mock_stream
        mock_get_provider.return_value = mock_provider
        
        # Make request
        response = client.post("/chat/stream", json={
            "message": "test",
            "conversation_id": "test-123",
            "use_rag": False,
            "provider": "test-provider"
        })
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
        
        # Parse SSE stream
        lines = response.text.strip().split('\n')
        data_lines = [line for line in lines if line.startswith('data: ')]
        
        # Should have content chunks + [DONE]
        assert len(data_lines) > 0
        
        # Last line should be [DONE]
        assert data_lines[-1] == 'data: [DONE]'
        
        # Other lines should be valid JSON
        for line in data_lines[:-1]:
            data = json.loads(line[6:])  # Remove 'data: ' prefix
            # Should have choices or error
            assert 'choices' in data or 'error' in data
    
    @patch('routers.chat.get_provider')
    @patch('routers.chat.get_rag_agent')
    def test_stream_includes_sources_with_rag(self, mock_rag_agent, mock_get_provider):
        """Should include sources in the stream when RAG returns results and use top_k trimming"""
        # Mock RAG to return 9 results (3x top_k)
        mock_rag_instance = AsyncMock()
        mock_results = [
            {
                'content': f'Content {i}',
                'score': 0.9 - (i * 0.05),
                'metadata': {
                    'norma_completa': f'Ley {i}',
                    'articulo': f'{i}',
                    'capa': 1 if i < 3 else 2  # First 3 are capa 1
                }
            }
            for i in range(9)
        ]
        mock_rag_instance.search_documents = AsyncMock(return_value=mock_results)
        mock_rag_agent.return_value = mock_rag_instance
        
        # Mock provider
        mock_provider = MagicMock()
        mock_provider.get_info.return_value = {"name": "Test Provider"}
        
        async def mock_stream(messages, temperature, max_tokens):
            yield "Response"
        
        mock_provider.generate_stream = mock_stream
        mock_get_provider.return_value = mock_provider
        
        # Make request with top_k=3
        response = client.post("/chat/stream", json={
            "message": "test",
            "conversation_id": "test-123",
            "use_rag": True,
            "provider": "test-provider",
            "top_k": 3
        })
        
        assert response.status_code == 200
        
        # Parse SSE stream
        lines = response.text.strip().split('\n')
        data_lines = [line for line in lines if line.startswith('data: ')]
        
        # Find sources line
        sources_line = None
        for line in data_lines:
            if line != 'data: [DONE]':
                data = json.loads(line[6:])
                if 'sources' in data:
                    sources_line = data
                    break
        
        # Should have sources
        assert sources_line is not None
        assert 'sources' in sources_line
        
        # Should have exactly top_k sources (3)
        assert len(sources_line['sources']) == 3
        
        # Sources should have required fields
        for source in sources_line['sources']:
            assert 'norma' in source
            assert 'score' in source
            assert 'content_preview' in source
    
    @patch('routers.chat.get_provider')
    @patch('routers.chat.get_rag_agent')
    def test_stream_continues_when_rag_fails(self, mock_rag_agent, mock_get_provider):
        """Should emit an SSE error and continue when RAG lookup fails, still ending with [DONE]"""
        # Mock RAG to raise exception
        mock_rag_instance = AsyncMock()
        mock_rag_instance.search_documents = AsyncMock(side_effect=Exception("RAG connection failed"))
        mock_rag_agent.return_value = mock_rag_instance
        
        # Mock provider
        mock_provider = MagicMock()
        mock_provider.get_info.return_value = {"name": "Test Provider"}
        
        async def mock_stream(messages, temperature, max_tokens):
            yield "Response without RAG"
        
        mock_provider.generate_stream = mock_stream
        mock_get_provider.return_value = mock_provider
        
        # Make request
        response = client.post("/chat/stream", json={
            "message": "test",
            "conversation_id": "test-123",
            "use_rag": True,
            "provider": "test-provider"
        })
        
        assert response.status_code == 200
        
        # Parse SSE stream
        lines = response.text.strip().split('\n')
        data_lines = [line for line in lines if line.startswith('data: ')]
        
        # Should have error message about RAG
        error_found = False
        for line in data_lines:
            if line != 'data: [DONE]':
                data = json.loads(line[6:])
                if 'error' in data and 'RAG' in data['error']:
                    error_found = True
                    break
        
        assert error_found, "Should emit error message when RAG fails"
        
        # Should still end with [DONE]
        assert data_lines[-1] == 'data: [DONE]'
    
    @patch('httpx.AsyncClient.post')
    @patch('routers.chat.RAGAgentV2')
    def test_message_returns_503_when_mistral_unreachable(self, mock_rag_class, mock_httpx_post):
        """Should return 503 when Mistral is unreachable in non-streaming /message"""
        # Mock RAG to return no results
        mock_rag_instance = AsyncMock()
        mock_rag_instance.search_documents = AsyncMock(return_value=[])
        mock_rag_class.return_value = mock_rag_instance
        
        # Mock httpx to raise ConnectError
        import httpx
        mock_httpx_post.side_effect = httpx.ConnectError("Connection refused")
        
        # Make request
        response = client.post("/chat/message", json={
            "message": "test",
            "conversation_id": "test-123",
            "use_rag": False
        })
        
        # Should return 503
        assert response.status_code == 503
        assert "Cannot connect to Mistral server" in response.json()["detail"]
    
    @patch('routers.chat.list_providers')
    def test_list_providers_structure(self, mock_list_providers):
        """Should list providers via /chat/providers with expected structure"""
        # Mock list_providers to return expected structure
        mock_list_providers.return_value = [
            {
                "id": "groq-8b",
                "name": "Groq Llama 3.3 70B",
                "model": "llama-3.3-70b-versatile"
            },
            {
                "id": "deepseek-chat",
                "name": "DeepSeek Chat",
                "model": "deepseek-chat"
            }
        ]
        
        # Make request
        response = client.get("/chat/providers")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should have providers key
        assert "providers" in data
        assert isinstance(data["providers"], list)
        
        # Should have at least one provider
        assert len(data["providers"]) > 0
        
        # Each provider should have required fields
        for provider in data["providers"]:
            assert "id" in provider
            assert "name" in provider
            assert "model" in provider


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

