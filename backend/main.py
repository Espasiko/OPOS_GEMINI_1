"""
OpositAIA Backend - FastAPI Application
Multi-Agent Architecture with RAG
"""

import os
import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env.backend
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env.backend'
    load_dotenv(dotenv_path=env_path)
    logger.info(f"✅ Loaded environment from: {env_path}")
except ImportError:
    logger.warning("⚠️  python-dotenv not installed, using system env vars")
except Exception as e:
    logger.error(f"❌ Error loading .env.backend: {e}")

# Import routers
from routers import rag, rag_v2, chat, upload, ai_functions, user, boe
from database.db import db


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events
    """
    # Startup
    logger.info("🚀 OpositAIA Backend starting...")
    logger.info(f"Embedding Model: {os.getenv('EMBEDDING_MODEL', 'PlanTL-GOB-ES/RoBERTalex')}")
    logger.info(f"Qdrant URL: {os.getenv('QDRANT_URL', 'http://localhost:6333')}")
    logger.info(f"Ollama URL: {os.getenv('OLLAMA_URL', 'http://localhost:11434')}")
    
    # Initialize DB
    try:
        db.initialize()
        logger.info("✅ Database connection initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")

    yield
    
    # Shutdown
    logger.info("👋 OpositAIA Backend shutting down...")
    db.close()


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
app.include_router(chat.router)  # Sprint 7: Chat with Mistral + RAG
app.include_router(upload.router)  # Sprint 7: File/URL upload
app.include_router(ai_functions.router)  # Sprint 8: AI functions multi-provider
app.include_router(user.router)  # Sprint 11: User management
app.include_router(boe.router)  # API oficial datos abiertos BOE

# Root endpoint
@app.get("/")
async def root():
    """
    API Root - Health check
    """
    return {
        "name": "OpositAIA API",
        "version": "2.0.0",
        "status": "healthy",
        "features": [
            "RAG search (v1 & v2)",
            "Chat with Mistral + RAG",
            "File upload and processing",
            "URL content extraction"
        ],
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "embedding_model": os.getenv("EMBEDDING_MODEL", "PlanTL-GOB-ES/RoBERTalex"),
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
