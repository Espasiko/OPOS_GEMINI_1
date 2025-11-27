"""
Upload Router - File and URL processing
Sprint 7 - Fase 1
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional
import pypdf
import io
import httpx
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/upload", tags=["upload"])


class UploadResponse(BaseModel):
    document_id: str
    filename: str
    text_length: int
    pages: Optional[int] = None
    indexed: bool = False
    text_preview: str


class UrlUploadRequest(BaseModel):
    url: HttpUrl


class UrlUploadResponse(BaseModel):
    document_id: str
    url: str
    text_length: int
    indexed: bool = False
    text_preview: str


# Caché temporal de documentos (en producción usar Redis)
document_cache = {}


@router.post("/file", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    Sube un archivo y extrae su texto
    
    Soporta:
    - PDF
    - TXT
    
    Returns:
    - document_id: ID único para referenciar el documento
    - text_length: Longitud del texto extraído
    - text_preview: Primeros 500 caracteres
    """
    logger.info(f"Uploading file: {file.filename}")
    
    # Validar tipo de archivo
    allowed_types = ["application/pdf", "text/plain"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Allowed: PDF, TXT"
        )
    
    # Validar tamaño (max 10MB)
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum size: 10MB"
        )
    
    # Extraer texto según tipo
    try:
        if file.content_type == "application/pdf":
            pdf = pypdf.PdfReader(io.BytesIO(content))
            pages = len(pdf.pages)
            
            text_parts = []
            for page_num, page in enumerate(pdf.pages):
                try:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
                except Exception as e:
                    logger.warning(f"Error extracting page {page_num}: {e}")
            
            text = "\n".join(text_parts)
            
            if not text.strip():
                raise HTTPException(
                    status_code=400,
                    detail="PDF contains no extractable text"
                )
            
        else:  # text/plain
            text = content.decode('utf-8')
            pages = None
        
        # Generar ID único
        doc_id = str(uuid.uuid4())
        
        # Guardar en caché temporal
        document_cache[doc_id] = {
            "text": text,
            "filename": file.filename,
            "content_type": file.content_type,
            "pages": pages
        }
        
        logger.info(f"File processed: {file.filename} ({len(text)} chars)")
        
        return UploadResponse(
            document_id=doc_id,
            filename=file.filename,
            text_length=len(text),
            pages=pages,
            indexed=False,
            text_preview=text[:500]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )


@router.post("/url", response_model=UrlUploadResponse)
async def upload_url(request: UrlUploadRequest):
    """
    Descarga contenido de una URL y extrae texto
    
    Soporta:
    - Páginas HTML
    - PDFs remotos
    - Archivos de texto
    """
    url = str(request.url)
    logger.info(f"Fetching URL: {url}")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            
            content_type = response.headers.get('content-type', '').lower()
            
            # Procesar según content-type
            if 'pdf' in content_type:
                # PDF remoto
                pdf = pypdf.PdfReader(io.BytesIO(response.content))
                text_parts = []
                for page in pdf.pages:
                    try:
                        text = page.extract_text()
                        if text:
                            text_parts.append(text)
                    except:
                        pass
                text = "\n".join(text_parts)
                
            elif 'html' in content_type or 'text' in content_type:
                # HTML o texto
                text = response.text
                
                # Limpieza básica de HTML
                if 'html' in content_type:
                    import re
                    # Remover tags HTML básicos
                    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
                    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
                    text = re.sub(r'<[^>]+>', '', text)
                    text = re.sub(r'\s+', ' ', text)
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported content type: {content_type}"
                )
            
            if not text.strip():
                raise HTTPException(
                    status_code=400,
                    detail="URL contains no extractable text"
                )
            
            # Generar ID
            doc_id = str(uuid.uuid4())
            
            # Guardar en caché
            document_cache[doc_id] = {
                "text": text,
                "url": url,
                "content_type": content_type
            }
            
            logger.info(f"URL processed: {url} ({len(text)} chars)")
            
            return UrlUploadResponse(
                document_id=doc_id,
                url=url,
                text_length=len(text),
                indexed=False,
                text_preview=text[:500]
            )
            
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Failed to fetch URL: {e.response.status_code}"
        )
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to URL"
        )
    except Exception as e:
        logger.error(f"Error fetching URL: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing URL: {str(e)}"
        )


@router.get("/document/{document_id}")
async def get_document(document_id: str):
    """
    Obtiene un documento del caché por su ID
    """
    if document_id not in document_cache:
        raise HTTPException(
            status_code=404,
            detail="Document not found in cache"
        )
    
    doc = document_cache[document_id]
    
    return {
        "document_id": document_id,
        "text": doc["text"],
        "metadata": {
            k: v for k, v in doc.items() if k != "text"
        }
    }


@router.delete("/document/{document_id}")
async def delete_document(document_id: str):
    """
    Elimina un documento del caché
    """
    if document_id in document_cache:
        del document_cache[document_id]
        return {"status": "deleted", "document_id": document_id}
    
    raise HTTPException(
        status_code=404,
        detail="Document not found"
    )


@router.get("/health")
async def upload_health():
    """
    Health check del servicio de upload
    """
    return {
        "status": "healthy",
        "cached_documents": len(document_cache),
        "supported_types": ["PDF", "TXT", "HTML"]
    }
