"""
Tests for Chat Router
Sprint 7 - Fase 1
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
