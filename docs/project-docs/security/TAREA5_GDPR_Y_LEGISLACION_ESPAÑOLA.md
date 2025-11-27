# 🔐 TAREA 5: GDPR Y LEGISLACIÓN ESPAÑOLA

**Objetivo**: Cumplir con GDPR y legislación española para comercializar OpositAIA

---

## 📚 MARCO LEGAL APLICABLE

### 1. RGPD (Reglamento General de Protección de Datos)

**Reglamento (UE) 2016/679**
- Aplicable desde: 25 mayo 2018
- Ámbito: Toda la UE
- Multas: Hasta €20M o 4% facturación anual

### 2. LOPDGDD (Ley Orgánica de Protección de Datos)

**Ley Orgánica 3/2018**
- Complementa el RGPD en España
- Adaptaciones específicas españolas
- Autoridad: AEPD (Agencia Española de Protección de Datos)

### 3. LSSI (Ley de Servicios de la Sociedad de la Información)

**Ley 34/2002**
- Cookies y consentimiento
- Información legal obligatoria
- Comunicaciones comerciales

---

## 🎯 DATOS QUE PROCESA OPOSITAIA

### Análisis de Datos Personales

```
┌─────────────────────────────────────────────────────────┐
│                  DATOS QUE PROCESAS                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. DATOS DE CUENTA                                      │
│     • Email (identificación)                             │
│     • Contraseña (hasheada)                              │
│     • Nombre (opcional)                                  │
│     • Fecha de registro                                  │
│                                                          │
│  2. DATOS DE USO                                         │
│     • Queries realizadas                                 │
│     • Documentos consultados                             │
│     • Herramientas utilizadas                            │
│     • Tiempo de uso                                      │
│     • Preferencias (provider LLM, etc.)                  │
│                                                          │
│  3. DATOS TÉCNICOS                                       │
│     • IP address                                         │
│     • User agent                                         │
│     • Cookies de sesión                                  │
│     • Logs de acceso                                     │
│                                                          │
│  4. DATOS GENERADOS                                      │
│     • Resúmenes creados                                  │
│     • Flashcards generadas                               │
│     • Mapas mentales                                     │
│     • Planes de estudio                                  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Clasificación Legal

| Dato | Categoría | Base Legal | Retención |
|------|-----------|------------|-----------|
| Email | Identificativo | Contrato | Mientras sea usuario |
| Contraseña | Identificativo | Contrato | Mientras sea usuario |
| Queries | Uso del servicio | Interés legítimo | 12 meses |
| IP | Técnico | Interés legítimo | 12 meses |
| Contenido generado | Servicio | Contrato | Mientras sea usuario |

**Datos Sensibles**: ❌ NO (no procesas datos de salud, religión, etc.)

---

## ✅ REQUISITOS OBLIGATORIOS

### 1. Información al Usuario

#### A. Política de Privacidad (Obligatorio)

**Contenido mínimo**:

```markdown
# POLÍTICA DE PRIVACIDAD - OPOSITAIA

## 1. RESPONSABLE DEL TRATAMIENTO

**Identidad**: [Tu nombre o empresa]
**NIF/CIF**: [Tu NIF]
**Dirección**: [Tu dirección]
**Email**: privacy@opositaia.com
**Teléfono**: [Tu teléfono]

## 2. DATOS QUE RECOPILAMOS

### 2.1 Datos de Cuenta
- Email (obligatorio)
- Contraseña (hasheada con bcrypt)
- Nombre (opcional)

### 2.2 Datos de Uso
- Consultas realizadas
- Documentos consultados
- Herramientas utilizadas
- Preferencias de configuración

### 2.3 Datos Técnicos
- Dirección IP
- Navegador y dispositivo
- Cookies de sesión

## 3. FINALIDAD DEL TRATAMIENTO

Utilizamos tus datos para:
- Proporcionar el servicio de preparación de oposiciones
- Personalizar tu experiencia
- Mejorar nuestros servicios
- Comunicaciones relacionadas con el servicio
- Cumplir obligaciones legales

## 4. BASE LEGAL

- **Ejecución del contrato**: Datos necesarios para el servicio
- **Interés legítimo**: Mejora del servicio y seguridad
- **Consentimiento**: Comunicaciones comerciales (opcional)

## 5. DESTINATARIOS DE LOS DATOS

Tus datos pueden ser compartidos con:
- **Cloudflare**: Hosting y CDN (USA - Privacy Shield)
- **Qdrant Cloud**: Base de datos vectorial (EU)
- **Proveedores LLM**: 
  - Groq (USA)
  - DeepSeek (China)
  - Google Gemini (USA)
  - Cohere (Canadá)

Todos con garantías adecuadas (cláusulas contractuales tipo).

## 6. TRANSFERENCIAS INTERNACIONALES

Algunos proveedores están fuera de la UE:
- **USA**: Privacy Shield / Cláusulas contractuales tipo
- **China**: Cláusulas contractuales tipo
- **Canadá**: Decisión de adecuación

## 7. PLAZO DE CONSERVACIÓN

- **Datos de cuenta**: Mientras seas usuario + 1 año
- **Datos de uso**: 12 meses
- **Logs técnicos**: 12 meses
- **Contenido generado**: Mientras seas usuario

## 8. TUS DERECHOS

Tienes derecho a:
- **Acceso**: Obtener copia de tus datos
- **Rectificación**: Corregir datos inexactos
- **Supresión**: Eliminar tus datos ("derecho al olvido")
- **Limitación**: Restringir el tratamiento
- **Portabilidad**: Recibir tus datos en formato estructurado
- **Oposición**: Oponerte al tratamiento
- **No ser objeto de decisiones automatizadas**

Para ejercer tus derechos: privacy@opositaia.com

## 9. RECLAMACIONES

Puedes reclamar ante la AEPD:
- Web: www.aepd.es
- Sede electrónica: sedeagpd.gob.es
- Dirección: C/ Jorge Juan, 6, 28001 Madrid

## 10. SEGURIDAD

Medidas implementadas:
- Cifrado SSL/TLS
- Contraseñas hasheadas (bcrypt)
- Autenticación OAuth 2.0
- Rate limiting
- Logs de auditoría
- Backups cifrados

## 11. COOKIES

Utilizamos cookies para:
- Sesión de usuario (necesarias)
- Preferencias (funcionales)
- Analíticas (con consentimiento)

Más info en nuestra Política de Cookies.

Última actualización: [Fecha]
```

#### B. Aviso Legal (Obligatorio)

```markdown
# AVISO LEGAL - OPOSITAIA

## 1. DATOS IDENTIFICATIVOS

**Titular**: [Tu nombre o empresa]
**NIF/CIF**: [Tu NIF]
**Domicilio**: [Tu dirección]
**Email**: legal@opositaia.com
**Teléfono**: [Tu teléfono]

## 2. OBJETO

OpositAIA es una plataforma de preparación de oposiciones de Seguridad Social mediante IA.

## 3. CONDICIONES DE USO

### 3.1 Acceso
El acceso y uso requiere registro previo.

### 3.2 Obligaciones del Usuario
- Proporcionar información veraz
- Uso responsable del servicio
- No compartir credenciales
- No realizar ingeniería inversa

### 3.3 Propiedad Intelectual
- El contenido generado es propiedad del usuario
- La plataforma y su código son propiedad de OpositAIA
- Las leyes y normativas son de dominio público

### 3.4 Responsabilidad
- OpositAIA no garantiza la exactitud absoluta del contenido
- El usuario es responsable de verificar la información
- No sustituye el estudio de fuentes oficiales

### 3.5 Modificaciones
Nos reservamos el derecho a modificar estos términos.

## 4. LEGISLACIÓN APLICABLE

Legislación española. Jurisdicción de los tribunales de [Tu ciudad].

Última actualización: [Fecha]
```

#### C. Política de Cookies (Obligatorio)

```markdown
# POLÍTICA DE COOKIES - OPOSITAIA

## 1. ¿QUÉ SON LAS COOKIES?

Pequeños archivos de texto que se almacenan en tu dispositivo.

## 2. COOKIES QUE UTILIZAMOS

### 2.1 Cookies Necesarias (No requieren consentimiento)
| Cookie | Finalidad | Duración |
|--------|-----------|----------|
| session_id | Mantener sesión | Sesión |
| csrf_token | Seguridad | Sesión |

### 2.2 Cookies Funcionales (Requieren consentimiento)
| Cookie | Finalidad | Duración |
|--------|-----------|----------|
| user_prefs | Preferencias | 1 año |
| theme | Tema visual | 1 año |

### 2.3 Cookies Analíticas (Requieren consentimiento)
| Cookie | Finalidad | Duración | Proveedor |
|--------|-----------|----------|-----------|
| _ga | Google Analytics | 2 años | Google |
| _gid | Google Analytics | 24 horas | Google |

## 3. GESTIÓN DE COOKIES

Puedes gestionar las cookies en:
- Configuración de tu navegador
- Panel de preferencias de OpositAIA

## 4. MÁS INFORMACIÓN

- Chrome: chrome://settings/cookies
- Firefox: about:preferences#privacy
- Safari: Preferencias > Privacidad

Última actualización: [Fecha]
```

### 2. Consentimiento del Usuario

#### Banner de Cookies (Obligatorio)

```html
<!-- components/CookieBanner.tsx -->
<div class="cookie-banner">
  <h3>🍪 Usamos cookies</h3>
  <p>
    Utilizamos cookies necesarias para el funcionamiento del sitio y 
    cookies opcionales para mejorar tu experiencia.
  </p>
  
  <div class="cookie-options">
    <label>
      <input type="checkbox" checked disabled> 
      Necesarias (obligatorias)
    </label>
    <label>
      <input type="checkbox" id="functional"> 
      Funcionales
    </label>
    <label>
      <input type="checkbox" id="analytics"> 
      Analíticas
    </label>
  </div>
  
  <div class="cookie-actions">
    <button onclick="acceptAll()">Aceptar todas</button>
    <button onclick="acceptSelected()">Aceptar seleccionadas</button>
    <button onclick="rejectOptional()">Solo necesarias</button>
  </div>
  
  <a href="/politica-cookies">Más información</a>
</div>
```

#### Consentimiento para Tratamiento de Datos

```html
<!-- En el registro -->
<form>
  <input type="email" name="email" required>
  <input type="password" name="password" required>
  
  <label>
    <input type="checkbox" name="privacy_accepted" required>
    He leído y acepto la 
    <a href="/politica-privacidad">Política de Privacidad</a>
  </label>
  
  <label>
    <input type="checkbox" name="terms_accepted" required>
    Acepto los 
    <a href="/terminos-condiciones">Términos y Condiciones</a>
  </label>
  
  <label>
    <input type="checkbox" name="marketing_accepted">
    Acepto recibir comunicaciones comerciales (opcional)
  </label>
  
  <button type="submit">Registrarse</button>
</form>
```

### 3. Derechos del Usuario

#### Portal de Privacidad

```typescript
// components/PrivacyPortal.tsx
export function PrivacyPortal() {
  return (
    <div className="privacy-portal">
      <h2>Tus Derechos de Privacidad</h2>
      
      <div className="rights-grid">
        <div className="right-card">
          <h3>📥 Acceso</h3>
          <p>Descarga todos tus datos</p>
          <button onClick={downloadData}>Descargar mis datos</button>
        </div>
        
        <div className="right-card">
          <h3>✏️ Rectificación</h3>
          <p>Corrige tus datos</p>
          <button onClick={editProfile}>Editar perfil</button>
        </div>
        
        <div className="right-card">
          <h3>🗑️ Supresión</h3>
          <p>Elimina tu cuenta y datos</p>
          <button onClick={deleteAccount}>Eliminar cuenta</button>
        </div>
        
        <div className="right-card">
          <h3>📤 Portabilidad</h3>
          <p>Exporta tus datos</p>
          <button onClick={exportData}>Exportar datos</button>
        </div>
        
        <div className="right-card">
          <h3>🚫 Oposición</h3>
          <p>Oponte al tratamiento</p>
          <button onClick={objectProcessing}>Ejercer oposición</button>
        </div>
        
        <div className="right-card">
          <h3>⚠️ Reclamar</h3>
          <p>Contacta con nosotros o la AEPD</p>
          <a href="mailto:privacy@opositaia.com">Contactar</a>
        </div>
      </div>
    </div>
  );
}
```

#### Implementación Backend

```python
# backend/routers/privacy.py
from fastapi import APIRouter, Depends
from typing import Dict
import json

router = APIRouter(prefix="/privacy", tags=["privacy"])

@router.get("/download-data")
async def download_user_data(user_id: str = Depends(get_current_user)):
    """
    Derecho de acceso (Art. 15 RGPD)
    Proporciona todos los datos del usuario
    """
    # Recopilar todos los datos
    user_data = {
        "account": get_account_data(user_id),
        "queries": get_user_queries(user_id),
        "generated_content": get_generated_content(user_id),
        "preferences": get_user_preferences(user_id),
        "logs": get_user_logs(user_id, last_12_months=True)
    }
    
    # Generar archivo JSON
    filename = f"opositaia_data_{user_id}_{datetime.now().isoformat()}.json"
    
    return {
        "filename": filename,
        "data": user_data,
        "generated_at": datetime.now().isoformat()
    }

@router.delete("/delete-account")
async def delete_user_account(
    user_id: str = Depends(get_current_user),
    confirmation: str = None
):
    """
    Derecho de supresión (Art. 17 RGPD)
    Elimina todos los datos del usuario
    """
    if confirmation != "DELETE_MY_ACCOUNT":
        raise ValueError("Confirmation required")
    
    # Eliminar datos
    delete_account_data(user_id)
    delete_user_queries(user_id)
    delete_generated_content(user_id)
    delete_user_preferences(user_id)
    anonymize_logs(user_id)  # Anonimizar logs (no eliminar por seguridad)
    
    # Log de auditoría
    log_account_deletion(user_id)
    
    return {
        "message": "Account deleted successfully",
        "deleted_at": datetime.now().isoformat()
    }

@router.post("/export-data")
async def export_user_data(
    user_id: str = Depends(get_current_user),
    format: str = "json"
):
    """
    Derecho de portabilidad (Art. 20 RGPD)
    Exporta datos en formato estructurado
    """
    data = get_all_user_data(user_id)
    
    if format == "json":
        return JSONResponse(content=data)
    elif format == "csv":
        return generate_csv(data)
    else:
        raise ValueError("Unsupported format")
```

---

## 🔒 MEDIDAS DE SEGURIDAD TÉCNICAS

### 1. Cifrado

```python
# backend/security/encryption.py
from cryptography.fernet import Fernet
import bcrypt
import os

# Cifrado de datos sensibles
class DataEncryption:
    def __init__(self):
        self.key = os.getenv("ENCRYPTION_KEY").encode()
        self.cipher = Fernet(self.key)
    
    def encrypt(self, data: str) -> str:
        """Cifra datos sensibles"""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Descifra datos"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()

# Hash de contraseñas
def hash_password(password: str) -> str:
    """Hash seguro de contraseña con bcrypt"""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, hashed: str) -> bool:
    """Verifica contraseña"""
    return bcrypt.checkpw(password.encode(), hashed.encode())
```

### 2. Anonimización de Logs

```python
# backend/security/anonymization.py
import hashlib

def anonymize_ip(ip: str) -> str:
    """
    Anonimiza IP para cumplir RGPD
    Mantiene los primeros 3 octetos, anonimiza el último
    """
    parts = ip.split('.')
    if len(parts) == 4:
        return f"{parts[0]}.{parts[1]}.{parts[2]}.0"
    return "0.0.0.0"

def pseudonymize_user_id(user_id: str) -> str:
    """
    Pseudonimiza user_id para logs
    """
    return hashlib.sha256(user_id.encode()).hexdigest()[:16]
```

### 3. Auditoría

```python
# backend/security/audit.py
import logging
from datetime import datetime

audit_logger = logging.getLogger("audit")

def log_data_access(user_id: str, action: str, data_type: str):
    """
    Registra accesos a datos personales
    """
    audit_logger.info({
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": pseudonymize_user_id(user_id),
        "action": action,
        "data_type": data_type
    })

def log_consent_change(user_id: str, consent_type: str, granted: bool):
    """
    Registra cambios en consentimientos
    """
    audit_logger.info({
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": pseudonymize_user_id(user_id),
        "consent_type": consent_type,
        "granted": granted
    })
```

---

## 📋 CHECKLIST DE CUMPLIMIENTO

### Antes del Lanzamiento

- [ ] **Documentos Legales**
  - [ ] Política de Privacidad publicada
  - [ ] Aviso Legal publicado
  - [ ] Política de Cookies publicada
  - [ ] Términos y Condiciones publicados

- [ ] **Consentimientos**
  - [ ] Banner de cookies implementado
  - [ ] Checkboxes de consentimiento en registro
  - [ ] Registro de consentimientos en BD

- [ ] **Derechos del Usuario**
  - [ ] Portal de privacidad implementado
  - [ ] Descarga de datos funcional
  - [ ] Eliminación de cuenta funcional
  - [ ] Exportación de datos funcional

- [ ] **Seguridad Técnica**
  - [ ] SSL/TLS configurado
  - [ ] Contraseñas hasheadas (bcrypt)
  - [ ] Datos sensibles cifrados
  - [ ] Logs anonimizados
  - [ ] Backups cifrados

- [ ] **Contratos con Terceros**
  - [ ] DPA con Cloudflare
  - [ ] DPA con Qdrant
  - [ ] DPA con proveedores LLM

- [ ] **Registro AEPD**
  - [ ] Evaluar si necesitas registro
  - [ ] Registrar actividades de tratamiento

---

## 💰 COSTES

**Asesoría Legal**: €500-1,500 (una vez)  
**Plantillas Legales**: €200-500 (una vez)  
**Herramientas Compliance**: €0-50/mes  
**DPO Externo**: €100-300/mes (si necesario)

**Estimación para OpositAIA**:
- Plantillas legales: €300
- Revisión legal: €500
- **TOTAL INICIAL**: €800
- **MENSUAL**: €0 (no necesitas DPO aún)

---

## 🎯 RECOMENDACIÓN FINAL

**Plan de Acción**:

```
Fase 1: Documentación Legal (1 semana)
- Contratar plantillas legales adaptadas
- Revisar con abogado especializado
- Publicar en web

Fase 2: Implementación Técnica (1 semana)
- Banner de cookies
- Portal de privacidad
- Sistemas de consentimiento

Fase 3: Seguridad (1 semana)
- Cifrado de datos
- Anonimización de logs
- Auditoría

Fase 4: Contratos (1 semana)
- DPAs con proveedores
- Cláusulas contractuales tipo

TOTAL: 4 semanas
COSTE: €800 inicial
```

**Recursos Recomendados**:
- **AEPD**: www.aepd.es (guías gratuitas)
- **Plantillas**: iubenda.com, termsfeed.com
- **Asesoría**: Abogado especializado en protección de datos

---

## ⚠️ IMPORTANTE

**NO LANZAR SIN**:
1. ✅ Política de Privacidad
2. ✅ Aviso Legal
3. ✅ Banner de Cookies
4. ✅ Sistema de consentimientos
5. ✅ Portal de derechos del usuario

**Multas RGPD**: Hasta €20M o 4% facturación  
**Mejor prevenir que curar** 🛡️
