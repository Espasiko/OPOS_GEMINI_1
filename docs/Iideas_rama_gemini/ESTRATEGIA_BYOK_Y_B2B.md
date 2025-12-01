# 🚀 ESTRATEGIA BYOK (Bring Your Own Key) + B2B

**Fecha**: 23 Noviembre 2025  
**Modelo de Negocio**: Híbrido BYOK + Managed + Enterprise  
**Estado**: Estrategia definitiva aprobada

---

## 📋 ÍNDICE

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Modelo de 3 Tiers](#modelo-de-3-tiers)
3. [Implementación Técnica](#implementación-técnica)
4. [Soporte Automatizado con IA](#soporte-automatizado)
5. [Estrategia B2B](#estrategia-b2b)
6. [Análisis Financiero](#análisis-financiero)
7. [Roadmap de Implementación](#roadmap)

---

## 🎯 RESUMEN EJECUTIVO

### La Oportunidad

**Problema**: Competidores cobran por tokens + software → costes altos y opacos  
**Solución**: BYOK (Bring Your Own Key) → usuario controla sus costes, nosotros vendemos software

### Ventajas Clave

✅ **Coste CERO de infraestructura IA** (usuarios traen sus keys)  
✅ **Escalabilidad infinita** (no hay límite de usuarios)  
✅ **Margen 100%** en tier freemium  
✅ **Diferenciador de mercado** (libertad de elegir modelo)  
✅ **Transparencia total** (usuario ve su propio uso)  
✅ **Perfecto para B2B** (academias/preparadores)

### Target Perfecto

- 🎓 **Opositores**: Gen Z, técnicamente capaces
- 📚 **Academias**: Quieren control de costes
- 👨‍🏫 **Preparadores**: Necesitan escalabilidad
- 🏢 **Empresas**: Políticas de seguridad propias

---

## 💎 MODELO DE 3 TIERS

### TIER 1: FREEMIUM (BYOK) 🆓

**Target**: Estudiantes individuales, early adopters

```
┌─────────────────────────────────────────────┐
│  FREEMIUM - Bring Your Own Key             │
├─────────────────────────────────────────────┤
│  ✅ Usuario trae su API key de Groq         │
│  ✅ 14,400 requests/día (free tier Groq)    │
│  ✅ Acceso a TODAS las features             │
│  ✅ Sin límite de tiempo                    │
│  ✅ Sin tarjeta de crédito                  │
│  ✅ Puede cambiar de modelo cuando quiera   │
├─────────────────────────────────────────────┤
│  Coste para ti: €0                          │
│  Precio usuario: €0                         │
│  Margen: N/A (lead generation)              │
└─────────────────────────────────────────────┘
```

**Providers soportados (todos con free tier):**
- Groq: 14,400 req/día
- Google Gemini: 1,500 req/día
- Mistral: 1M tokens/mes
- OpenRouter: Varios modelos gratis

**Gancho de Marketing:**
```
🎯 "Estudia Oposiciones con IA - Gratis Para Siempre"

✅ Trae tu API key de Groq (100% gratis)
✅ 14,400 preguntas al día
✅ Todas las herramientas incluidas
✅ Sin límites de tiempo

[Empezar Gratis en 2 minutos]
```

---

### TIER 2: PREMIUM (Managed) ⚡

**Target**: Usuarios que quieren comodidad, profesionales

```
┌─────────────────────────────────────────────┐
│  PREMIUM - Sin Configuración                │
├─────────────────────────────────────────────┤
│  ✅ Nosotros proveemos las API keys         │
│  ✅ Sin límites (hasta 10K req/mes)         │
│  ✅ Soporte prioritario (24h)               │
│  ✅ Sin configuración técnica               │
│  ✅ Listo en 30 segundos                    │
│  ✅ Actualizaciones automáticas             │
├─────────────────────────────────────────────┤
│  Coste para ti: €6/mes                      │
│  Precio usuario: €29.99/mes                 │
│  Margen: €23.99 (80%)                       │
└─────────────────────────────────────────────┘
```

**Propuesta de Valor:**
- "Olvídate de la configuración, enfócate en estudiar"
- "Soporte experto cuando lo necesites"
- "Garantía de disponibilidad 99.9%"

---

### TIER 3: ENTERPRISE (B2B) 🏢

**Target**: Academias, preparadores, empresas

```
┌─────────────────────────────────────────────┐
│  ENTERPRISE - Para Academias                │
├─────────────────────────────────────────────┤
│  ✅ Multi-usuario (10-200 estudiantes)      │
│  ✅ Dashboard de administración             │
│  ✅ Analytics avanzados                     │
│  ✅ Branding personalizado                  │
│  ✅ Contenido propio                        │
│  ✅ BYOK o Managed (a elegir)               │
│  ✅ Soporte dedicado                        │
│  ✅ SLA garantizado                         │
├─────────────────────────────────────────────┤
│  Coste para ti: €6-€50/mes                  │
│  Precio: €199-€999/mes                      │
│  Margen: 80-95%                             │
└─────────────────────────────────────────────┘
```

**Planes Enterprise:**

| Plan | Estudiantes | BYOK | Managed | Features |
|------|-------------|------|---------|----------|
| **Starter** | 10-25 | €199/mes | €249/mes | Dashboard básico |
| **Professional** | 26-50 | €399/mes | €499/mes | + Analytics + Branding |
| **Enterprise** | 51-200 | €799/mes | €999/mes | + White-label + API |
| **Custom** | 200+ | Negociar | Negociar | Todo personalizado |

---

## 🔧 IMPLEMENTACIÓN TÉCNICA

### Arquitectura del Sistema

```
┌─────────────────────────────────────────────┐
│           FRONTEND (React)                  │
│  - Onboarding BYOK                          │
│  - Configuración de keys                    │
│  - Selector de provider                     │
└────────────────┬────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────┐
│           BACKEND (FastAPI)                 │
│  ┌─────────────────────────────────────┐   │
│  │  API Key Manager                    │   │
│  │  - Encriptación (Fernet)            │   │
│  │  - Validación                       │   │
│  │  - Pool management                  │   │
│  └─────────────────────────────────────┘   │
│  ┌─────────────────────────────────────┐   │
│  │  Provider Router                    │   │
│  │  - Groq                             │   │
│  │  - Gemini                           │   │
│  │  - Mistral                          │   │
│  │  - OpenRouter                       │   │
│  └─────────────────────────────────────┘   │
│  ┌─────────────────────────────────────┐   │
│  │  Token Tracker                      │   │
│  │  - Por usuario                      │   │
│  │  - Por feature                      │   │
│  │  - Por provider                     │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────┐
│        PROVIDERS (External APIs)            │
│  - Groq (BYOK o Pool)                       │
│  - Gemini (BYOK o Pool)                     │
│  - Mistral (BYOK o Pool)                    │
└─────────────────────────────────────────────┘
```

---

### 1. Modelo de Datos

```python
# backend/models/user.py
from enum import Enum
from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel, EmailStr

class UserTier(str, Enum):
    FREEMIUM_BYOK = "freemium_byok"
    PREMIUM_MANAGED = "premium_managed"
    ENTERPRISE_BYOK = "enterprise_byok"
    ENTERPRISE_MANAGED = "enterprise_managed"

class APIKeyConfig(BaseModel):
    """Configuración de API keys del usuario"""
    groq_key: Optional[str] = None  # Encriptado
    gemini_key: Optional[str] = None
    mistral_key: Optional[str] = None
    openrouter_key: Optional[str] = None
    
    # Metadata
    groq_validated_at: Optional[datetime] = None
    gemini_validated_at: Optional[datetime] = None
    
    # Preferencias
    default_provider: str = "groq"
    fallback_provider: Optional[str] = "gemini"

class User(BaseModel):
    id: str
    email: EmailStr
    name: str
    tier: UserTier
    
    # API Keys (solo para BYOK)
    api_keys: Optional[APIKeyConfig] = None
    
    # Subscription
    subscription_id: Optional[str] = None
    subscription_ends_at: Optional[datetime] = None
    
    # Enterprise
    organization_id: Optional[str] = None
    is_admin: bool = False
    
    # Metadata
    created_at: datetime
    last_login_at: Optional[datetime] = None
    onboarding_completed: bool = False

class Organization(BaseModel):
    """Para tier Enterprise"""
    id: str
    name: str
    tier: UserTier
    
    # API Keys (si es BYOK)
    api_keys: Optional[APIKeyConfig] = None
    
    # Configuración
    max_students: int
    branding: Dict = {}  # logo, colors, domain
    custom_content: bool = False
    
    # Billing
    subscription_id: str
    billing_email: EmailStr
    
    # Metadata
    created_at: datetime
    admin_user_ids: list[str] = []
```

---

### 2. API Key Manager

```python
# backend/services/api_key_manager.py
from cryptography.fernet import Fernet
from groq import Groq
import google.generativeai as genai
from mistralai.client import MistralClient
import os
from typing import Optional, Tuple
import asyncio

class APIKeyManager:
    """Gestiona API keys de forma segura"""
    
    def __init__(self):
        # Encriptación
        self.cipher = Fernet(os.getenv("ENCRYPTION_KEY").encode())
        
        # Pool de keys managed (para tier Premium)
        self.managed_keys = {
            "groq": self._load_groq_pool(),
            "gemini": self._load_gemini_pool(),
            "mistral": self._load_mistral_pool()
        }
        
        # Cache de clientes
        self.client_cache = {}
    
    def _load_groq_pool(self) -> list[str]:
        """Carga pool de keys de Groq para usuarios Premium"""
        keys = os.getenv("GROQ_POOL_KEYS", "").split(",")
        return [k.strip() for k in keys if k.strip()]
    
    def _load_gemini_pool(self) -> list[str]:
        """Carga pool de keys de Gemini"""
        keys = os.getenv("GEMINI_POOL_KEYS", "").split(",")
        return [k.strip() for k in keys if k.strip()]
    
    def _load_mistral_pool(self) -> list[str]:
        """Carga pool de keys de Mistral"""
        keys = os.getenv("MISTRAL_POOL_KEYS", "").split(",")
        return [k.strip() for k in keys if k.strip()]
    
    # ===== ENCRIPTACIÓN =====
    
    def encrypt_key(self, api_key: str) -> str:
        """Encripta API key antes de guardar en DB"""
        return self.cipher.encrypt(api_key.encode()).decode()
    
    def decrypt_key(self, encrypted_key: str) -> str:
        """Desencripta API key para usar"""
        return self.cipher.decrypt(encrypted_key.encode()).decode()
    
    # ===== VALIDACIÓN =====
    
    async def validate_groq_key(self, api_key: str) -> Tuple[bool, Optional[str]]:
        """Valida que la API key de Groq funcione"""
        try:
            client = Groq(api_key=api_key)
            response = await asyncio.to_thread(
                client.chat.completions.create,
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            return True, None
        except Exception as e:
            error_msg = str(e)
            if "invalid" in error_msg.lower():
                return False, "API key inválida"
            elif "quota" in error_msg.lower():
                return False, "Límite de cuota alcanzado"
            else:
                return False, f"Error: {error_msg}"
    
    async def validate_gemini_key(self, api_key: str) -> Tuple[bool, Optional[str]]:
        """Valida que la API key de Gemini funcione"""
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            response = await asyncio.to_thread(
                model.generate_content,
                "test"
            )
            return True, None
        except Exception as e:
            return False, str(e)
    
    async def validate_mistral_key(self, api_key: str) -> Tuple[bool, Optional[str]]:
        """Valida que la API key de Mistral funcione"""
        try:
            client = MistralClient(api_key=api_key)
            response = await asyncio.to_thread(
                client.chat,
                model="mistral-tiny",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            return True, None
        except Exception as e:
            return False, str(e)
    
    # ===== OBTENER CLIENTES =====
    
    async def get_client_for_user(
        self,
        user: User,
        provider: str,
        organization: Optional[Organization] = None
    ):
        """Obtiene cliente configurado según tier del usuario"""
        
        # Enterprise: puede tener keys a nivel org
        if user.tier in [UserTier.ENTERPRISE_BYOK, UserTier.ENTERPRISE_MANAGED]:
            if organization and organization.api_keys:
                return await self._get_client_from_keys(
                    provider,
                    organization.api_keys
                )
        
        # BYOK: usar key del usuario
        if user.tier == UserTier.FREEMIUM_BYOK:
            if not user.api_keys:
                raise ValueError(f"No tienes configurada API key de {provider}")
            
            return await self._get_client_from_keys(provider, user.api_keys)
        
        # Managed: usar pool
        elif user.tier in [UserTier.PREMIUM_MANAGED, UserTier.ENTERPRISE_MANAGED]:
            return await self._get_client_from_pool(provider, user.id)
        
        else:
            raise ValueError(f"Tier no soportado: {user.tier}")
    
    async def _get_client_from_keys(self, provider: str, keys: APIKeyConfig):
        """Obtiene cliente desde keys del usuario/org"""
        
        if provider == "groq":
            if not keys.groq_key:
                raise ValueError("No tienes configurada API key de Groq")
            api_key = self.decrypt_key(keys.groq_key)
            return Groq(api_key=api_key)
        
        elif provider == "gemini":
            if not keys.gemini_key:
                raise ValueError("No tienes configurada API key de Gemini")
            api_key = self.decrypt_key(keys.gemini_key)
            genai.configure(api_key=api_key)
            return genai.GenerativeModel('gemini-pro')
        
        elif provider == "mistral":
            if not keys.mistral_key:
                raise ValueError("No tienes configurada API key de Mistral")
            api_key = self.decrypt_key(keys.mistral_key)
            return MistralClient(api_key=api_key)
        
        else:
            raise ValueError(f"Provider no soportado: {provider}")
    
    async def _get_client_from_pool(self, provider: str, user_id: str):
        """Obtiene cliente desde pool (round-robin simple)"""
        
        if provider not in self.managed_keys:
            raise ValueError(f"Provider no disponible en managed: {provider}")
        
        keys = self.managed_keys[provider]
        if not keys:
            raise ValueError(f"No hay keys disponibles para {provider}")
        
        # Round-robin simple (en producción: usar Redis para distribuir)
        key_index = hash(user_id) % len(keys)
        api_key = keys[key_index]
        
        if provider == "groq":
            return Groq(api_key=api_key)
        elif provider == "gemini":
            genai.configure(api_key=api_key)
            return genai.GenerativeModel('gemini-pro')
        elif provider == "mistral":
            return MistralClient(api_key=api_key)

# Instancia global
api_key_manager = APIKeyManager()
```

---

