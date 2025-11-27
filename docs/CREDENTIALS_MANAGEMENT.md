# Gestión de Credenciales - OpositaIA

## 🔐 Seguridad de Credenciales

### ⚠️ REGLAS IMPORTANTES

1. **NUNCA** commitear credenciales a Git
2. **NUNCA** compartir contraseñas en código
3. **SIEMPRE** usar variables de entorno
4. **SIEMPRE** usar archivos `.local` para credenciales

## 📁 Archivos de Credenciales

### Archivo Local (NO en Git)
**Ubicación**: `.credentials.local`

Este archivo contiene:
- Contraseñas de VPS
- API keys privadas
- Tokens de acceso
- Información sensible

**Estado**: ✅ En `.gitignore` (no se sube a GitHub)

### Cómo Usar

1. **Crear archivo local**:
```bash
cp .credentials.local.example .credentials.local
# Editar con tus credenciales reales
```

2. **Leer credenciales en scripts**:
```bash
# En bash
source .credentials.local
ssh $VPS_USER@$VPS_HOST
```

```python
# En Python
from dotenv import load_dotenv
load_dotenv('.credentials.local')

vps_host = os.getenv('VPS_HOST')
vps_password = os.getenv('VPS_PASSWORD')
```

## 🔑 Credenciales Necesarias

### 1. VPS Hostinger
- **Host**: 147.93.95.67
- **Usuario**: root
- **Password**: [Ver `.credentials.local`]
- **Puerto SSH**: 22

### 2. Google Gemini API
- **API Key**: [Ver `.env`]
- **Obtener en**: https://aistudio.google.com/app/apikey

### 3. BOE API
- **API Key**: No requiere (datos abiertos)
- **Base URL**: https://www.boe.es

### 4. Qdrant
- **URL Local**: http://localhost:6333
- **API Key**: No requiere (local)

### 5. Ollama
- **URL Local**: http://localhost:11434
- **API Key**: No requiere (local)

## 🛡️ Mejores Prácticas

### DO ✅

1. **Usar variables de entorno**:
```bash
# .env
GEMINI_API_KEY=your_key_here
VPS_HOST=147.93.95.67
```

2. **Usar archivos .local**:
```bash
# .credentials.local (en .gitignore)
VPS_PASSWORD=your_password_here
```

3. **Usar gestores de secretos**:
```bash
# Para producción
# - AWS Secrets Manager
# - HashiCorp Vault
# - GitHub Secrets
```

4. **Rotar credenciales regularmente**:
```bash
# Cambiar contraseñas cada 3-6 meses
# Rotar API keys si se comprometen
```

### DON'T ❌

1. **NO hardcodear credenciales**:
```python
# ❌ MAL
password = "Mamkavigadna?1"

# ✅ BIEN
password = os.getenv("VPS_PASSWORD")
```

2. **NO commitear archivos con credenciales**:
```bash
# ❌ MAL
git add .env
git add .credentials.local

# ✅ BIEN
# Estos archivos están en .gitignore
```

3. **NO compartir credenciales en chat/email**:
```
# ❌ MAL
"Mi contraseña es: 12345"

# ✅ BIEN
"He guardado la contraseña en .credentials.local"
```

## 📋 Checklist de Seguridad

Antes de cada commit:

- [ ] Verificar que `.env` está en `.gitignore`
- [ ] Verificar que `.credentials.local` está en `.gitignore`
- [ ] Buscar contraseñas hardcodeadas: `git grep -i password`
- [ ] Buscar API keys hardcodeadas: `git grep -i "api.key"`
- [ ] Revisar archivos staged: `git diff --cached`

## 🔄 Recuperación de Credenciales

Si olvidaste una credencial:

1. **VPS Password**: Revisar `.credentials.local`
2. **Gemini API Key**: Revisar `.env` o regenerar en Google AI Studio
3. **GitHub Token**: Regenerar en GitHub Settings

## 🚨 Si se Compromete una Credencial

1. **Cambiar inmediatamente**:
```bash
# VPS
ssh root@147.93.95.67
passwd  # Cambiar contraseña
```

2. **Rotar API keys**:
```bash
# Gemini: Regenerar en Google AI Studio
# GitHub: Regenerar en Settings > Developer settings
```

3. **Revisar logs**:
```bash
# Verificar accesos no autorizados
ssh root@147.93.95.67
last  # Ver últimos logins
```

4. **Notificar al equipo**:
```
"⚠️ Credencial comprometida: [tipo]
Acción tomada: [cambio/rotación]
Estado: [resuelto/en proceso]"
```

## 📚 Recursos

- [OWASP Secrets Management](https://owasp.org/www-community/vulnerabilities/Use_of_hard-coded_password)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [Git-secrets](https://github.com/awslabs/git-secrets)

---

**Última actualización**: 2025-01-16  
**Versión**: 1.0.0  
**Importancia**: 🔴 CRÍTICO
