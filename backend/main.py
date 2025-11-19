"""
OpositAIA Backend - FastAPI Application
Multi-Agent Architecture with RAG
"""

import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import routers
from routers import rag, rag_v2

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events
    """
    # Startup
    logger.info("🚀 OpositAIA Backend starting...")
    logger.info(f"Embedding Model: {os.getenv('EMBEDDING_MODEL', 'bge-m3')}")
    logger.info(f"Qdrant URL: {os.getenv('QDRANT_URL', 'http://localhost:6333')}")
    logger.info(f"Ollama URL: {os.getenv('OLLAMA_URL', 'http://localhost:11434')}")
    
    yield
    
    # Shutdown
    logger.info("👋 OpositAIA Backend shutting down...")


# Create FastAPI app
app = FastAPI(
    title="OpositAIA API",
    description="Multi-Agent AI System for Spanish Social Security Exam Preparation",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(rag.router)  # V1 (legacy)
app.include_router(rag_v2.router)  # V2 (RoBERTalex + 2 capas)

# Root endpoint
@app.get("/")
async def root():
    """
    API Root - Health check
    """
    return {
        "name": "OpositAIA API",
        "version": "1.0.0",
        "status": "healthy",
        "agents": ["RAG", "Analysis", "Quiz", "Recommendations"],
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "embedding_model": os.getenv("EMBEDDING_MODEL", "bge-m3"),
        "qdrant_url": os.getenv("QDRANT_URL", "http://localhost:6333"),
        "ollama_url": os.getenv("OLLAMA_URL", "http://localhost:11434")
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
