"""
Tests for Upload Router
Sprint 7 - Fase 1
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
import io
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from main import app

client = TestClient(app)


class TestUploadRouter:
    """Test suite for upload router"""
    
    def test_upload_health(self):
        """Test upload health endpoint"""
        response = client.get("/upload/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "cached_documents" in data
        assert "supported_types" in data
    
    def test_upload_text_file(self):
        """Test uploading a text file"""
        content = "Este es un texto de prueba para oposiciones de Seguridad Social."
        response = client.post(
            "/upload/file",
            files={"file": ("test.txt", io.BytesIO(content.encode()), "text/plain")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "document_id" in data
        assert data["filename"] == "test.txt"
        assert data["text_length"] == len(content)
        assert data["pages"] is None
        assert not data["indexed"]
        assert content in data["text_preview"]
    
    def test_upload_unsupported_file_type(self):
        """Test uploading unsupported file type"""
        response = client.post(
            "/upload/file",
            files={"file": ("test.jpg", io.BytesIO(b"fake image"), "image/jpeg")}
        )
        
        assert response.status_code == 400
        assert "Unsupported file type" in response.json()["detail"]
    
    def test_get_document_not_found(self):
        """Test retrieving non-existent document"""
        response = client.get("/upload/document/non-existent-id")
        assert response.status_code == 404
        assert "Document not found" in response.json()["detail"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
