"""
User Router - Sprint 11
Endpoints para gestión de usuarios y progreso
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
import logging
from database.db import db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/user", tags=["user"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class UserRegister(BaseModel):
    username: str
    email: EmailStr

class UserProgress(BaseModel):
    user_id: str
    username: str
    email: str
    total_preguntas: int
    total_correctas: int
    precision_global: float
    dias_estudiados: int
    racha_actual: int
    racha_maxima: int
    ultima_sesion: Optional[datetime]
    temas_completados: List[int]
    temas_debiles: List[int]

class SessionUpdate(BaseModel):
    duracion: int  # segundos
    preguntas_respondidas: int
    preguntas_correctas: int
    temas_estudiados: List[int]

class UserStats(BaseModel):
    user_id: str
    total_preguntas: int
    precision_global: float
    tiempo_total_horas: float
    simulacros_realizados: int
    casos_creados: int
    mapas_creados: int
    mejor_tema: Optional[str]
    peor_tema: Optional[str]


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/register", response_model=dict)
async def register_user(user: UserRegister):
    """
    Registrar nuevo usuario
    """
    try:
        with db.get_cursor() as cursor:
            # Check if user exists
            cursor.execute(
                "SELECT user_id FROM user_progress WHERE email = %s",
                (user.email,)
            )
            existing = cursor.fetchone()
            
            if existing:
                raise HTTPException(
                    status_code=400,
                    detail="User with this email already exists"
                )
            
            # Insert new user
            cursor.execute("""
                INSERT INTO user_progress (username, email)
                VALUES (%s, %s)
                RETURNING user_id, username, email, created_at
            """, (user.username, user.email))
            
            result = cursor.fetchone()
            
            logger.info(f"✅ User registered: {user.email}")
            
            return {
                "user_id": str(result[0]),
                "username": result[1],
                "email": result[2],
                "created_at": result[3].isoformat()
            }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}/progress", response_model=UserProgress)
async def get_user_progress(user_id: str):
    """
    Obtener progreso del usuario
    """
    try:
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT 
                    user_id, username, email,
                    total_preguntas, total_correctas, precision_global,
                    dias_estudiados, racha_actual, racha_maxima,
                    ultima_sesion, temas_completados, temas_debiles
                FROM user_progress
                WHERE user_id = %s
            """, (user_id,))
            
            result = cursor.fetchone()
            
            if not result:
                raise HTTPException(status_code=404, detail="User not found")
            
            return UserProgress(
                user_id=str(result[0]),
                username=result[1],
                email=result[2],
                total_preguntas=result[3],
                total_correctas=result[4],
                precision_global=result[5],
                dias_estudiados=result[6],
                racha_actual=result[7],
                racha_maxima=result[8],
                ultima_sesion=result[9],
                temas_completados=result[10] or [],
                temas_debiles=result[11] or []
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user progress: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{user_id}/session")
async def update_session(user_id: str, session: SessionUpdate):
    """
    Actualizar sesión de estudio
    """
    try:
        with db.get_cursor() as cursor:
            # Insert study session
            cursor.execute("""
                INSERT INTO study_sessions (
                    user_id, duracion, preguntas_respondidas,
                    preguntas_correctas, temas_estudiados,
                    started_at, ended_at
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    NOW() - INTERVAL '%s seconds',
                    NOW()
                )
                RETURNING id
            """, (
                user_id,
                session.duracion,
                session.preguntas_respondidas,
                session.preguntas_correctas,
                session.temas_estudiados,
                session.duracion
            ))
            
            session_id = cursor.fetchone()[0]
            
            # Update user progress
            cursor.execute("""
                UPDATE user_progress
                SET 
                    dias_estudiados = dias_estudiados + 1,
                    ultima_sesion = NOW(),
                    updated_at = NOW()
                WHERE user_id = %s
            """, (user_id,))
            
            logger.info(f"✅ Session updated for user: {user_id}")
            
            return {
                "session_id": str(session_id),
                "status": "updated"
            }
            
    except Exception as e:
        logger.error(f"Error updating session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}/stats", response_model=UserStats)
async def get_user_stats(user_id: str):
    """
    Obtener estadísticas detalladas del usuario
    """
    try:
        with db.get_cursor() as cursor:
            # Get basic stats
            cursor.execute("""
                SELECT 
                    total_preguntas, precision_global
                FROM user_progress
                WHERE user_id = %s
            """, (user_id,))
            
            basic = cursor.fetchone()
            if not basic:
                raise HTTPException(status_code=404, detail="User not found")
            
            # Get study time
            cursor.execute("""
                SELECT COALESCE(SUM(duracion), 0) / 3600.0
                FROM study_sessions
                WHERE user_id = %s
            """, (user_id,))
            tiempo_total = cursor.fetchone()[0]
            
            # Get simulacros count
            cursor.execute("""
                SELECT COUNT(*)
                FROM simulacros
                WHERE user_id = %s
            """, (user_id,))
            simulacros = cursor.fetchone()[0]
            
            # Get casos count
            cursor.execute("""
                SELECT COUNT(*)
                FROM user_cases
                WHERE user_id = %s
            """, (user_id,))
            casos = cursor.fetchone()[0]
            
            # Get mapas count
            cursor.execute("""
                SELECT COUNT(*)
                FROM mind_maps
                WHERE user_id = %s
            """, (user_id,))
            mapas = cursor.fetchone()[0]
            
            # Get best/worst topics
            cursor.execute("""
                SELECT 
                    tema_nombre,
                    ROUND(
                        (SUM(CASE WHEN es_correcta THEN 1 ELSE 0 END)::FLOAT / 
                         COUNT(*)::FLOAT) * 100, 
                        2
                    ) as precision
                FROM answer_history
                WHERE user_id = %s
                GROUP BY tema_nombre
                ORDER BY precision DESC
                LIMIT 1
            """, (user_id,))
            mejor = cursor.fetchone()
            
            cursor.execute("""
                SELECT 
                    tema_nombre,
                    ROUND(
                        (SUM(CASE WHEN es_correcta THEN 1 ELSE 0 END)::FLOAT / 
                         COUNT(*)::FLOAT) * 100, 
                        2
                    ) as precision
                FROM answer_history
                WHERE user_id = %s
                GROUP BY tema_nombre
                ORDER BY precision ASC
                LIMIT 1
            """, (user_id,))
            peor = cursor.fetchone()
            
            return UserStats(
                user_id=user_id,
                total_preguntas=basic[0],
                precision_global=basic[1],
                tiempo_total_horas=float(tiempo_total),
                simulacros_realizados=simulacros,
                casos_creados=casos,
                mapas_creados=mapas,
                mejor_tema=mejor[0] if mejor else None,
                peor_tema=peor[0] if peor else None
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check del servicio de usuarios"""
    return {
        "status": "healthy",
        "service": "user-management"
    }
