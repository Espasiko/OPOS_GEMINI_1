"""
Tests for Chat Router
Sprint 7 - Fase 1
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import httpx
import sys
from pathlib import Path

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

    def test_chat_message_mistral_unavailable(self):
        """Should return 503 when Mistral server is unreachable"""
        async def mocked_post(*args, **kwargs):
            request = httpx.Request("POST", "http://dummy")
            raise httpx.ConnectError("Connection failed", request=request)
        with patch("backend.routers.chat.httpx.AsyncClient.post", side_effect=mocked_post):
            resp = client.post("/chat/message", json={
                "message": "hola",
                "conversation_id": "c1",
                "use_rag": False
            })
            assert resp.status_code == 503
            assert "Cannot connect to Mistral server" in resp.text

    def test_chat_message_mistral_error_status(self):
        """Should return 500 when Mistral returns non-200 status"""
        class MockResponse:
            def __init__(self, status_code=500, text="error"):
                self.status_code = status_code
                self.text = text
            def json(self):
                return {"error": self.text}
        class MockClient:
            async def __aenter__(self):
                return self
            async def __aexit__(self, exc_type, exc, tb):
                return False
            async def post(self, *args, **kwargs):
                return MockResponse(500, "internal")
        with patch("backend.routers.chat.httpx.AsyncClient", return_value=MockClient()):
            resp = client.post("/chat/message", json={
                "message": "hola",
                "conversation_id": "c2",
                "use_rag": False
            })
            assert resp.status_code == 500
            assert "Mistral API error" in resp.text

    def test_chat_message_includes_sources_with_rag(self):
        """Should include sources when RAG returns results"""
        async def mocked_search_documents(self, query, top_k, min_score, layer_filter=None):
            return [
                {
                    "content": "Texto legal relevante...",
                    "score": 0.9,
                    "metadata": {"norma_completa": "TRLGSS", "articulo": "195", "capa": 1}
                }
            ]
        class MockResponseOK:
            def __init__(self):
                self.status_code = 200
            def json(self):
                return {
                    "choices": [{"message": {"content": "respuesta"}}]
                }
        class MockClientOK:
            async def __aenter__(self):
                return self
            async def __aexit__(self, exc_type, exc, tb):
                return False
            async def post(self, *args, **kwargs):
                return MockResponseOK()
        with patch("backend.routers.chat.RAGAgentV2.search_documents", new=mocked_search_documents):
            with patch("backend.routers.chat.httpx.AsyncClient", return_value=MockClientOK()):
                resp = client.post("/chat/message", json={
                    "message": "¿Qué dice la ley?",
                    "conversation_id": "c3",
                    "use_rag": True
                })
                assert resp.status_code == 200
                data = resp.json()
                assert "sources" in data
                assert len(data["sources"]) == 1
                assert data["sources"][0]["norma"] == "TRLGSS"
                assert data["response"] == "respuesta"

    def test_chat_stream_rag_failure_emits_error_and_done(self):
        """Stream should handle RAG failure gracefully and finish with [DONE]"""
        def raise_get_rag_agent():
            raise Exception("RAG down")
        class DummyProvider:
            def get_info(self):
                return "dummy"
            async def generate_stream(self, messages, temperature=0.7, max_tokens=2000):
                for part in ["Hola ", "mundo"]:
                    yield part
        with patch("backend.routers.chat.get_rag_agent", side_effect=raise_get_rag_agent):
            with patch("backend.routers.chat.get_provider", return_value=DummyProvider()):
                resp = client.post("/chat/stream", json={
                    "message": "ping",
                    "conversation_id": "c4",
                    "use_rag": True,
                    "provider": "dummy"
                })
                assert resp.status_code == 200
                body = resp.text
                assert "data: {\"error\":" in body
                assert "data: [DONE]" in body
                # Also ensure provider chunks were streamed
                assert "Hola " in body or "mundo" in body

    def test_chat_providers_endpoint(self):
        """Providers list is exposed"""
        with patch("backend.routers.chat.list_providers", return_value=["p1", "p2"]):
            resp = client.get("/chat/providers")
            assert resp.status_code == 200
            data = resp.json()
            assert data["providers"] == ["p1", "p2"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
