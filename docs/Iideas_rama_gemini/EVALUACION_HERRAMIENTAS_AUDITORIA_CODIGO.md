# 🔍 EVALUACIÓN: Herramientas de Auditoría de Código con IA

**Fecha:** 25 Noviembre 2025  
**Objetivo:** Encontrar la mejor herramienta para auditar OpositaIA  
**Criterios:** Seguridad, GDPR, legislación española, eficiencia, bugs, vulnerabilidades

---

## 📊 RESUMEN EJECUTIVO

**Mejor opción GLOBAL:** SonarQube Community (Open Source) + Snyk  
**Mejor opción IA:** Workik AI (gratis con limitaciones)  
**Mejor opción PRIVACIDAD:** GuardRails (local, open source)  
**Mejor opción AGENTES:** agentic-radar (específico para sistemas multi-agente)

**Recomendación para OpositaIA:**
1. **SonarQube Community** (análisis estático completo)
2. **Snyk** (vulnerabilidades y dependencias)
3. **Workik AI** (revisión con IA, contexto del proyecto)
4. **agentic-radar** (específico para tus agentes IA)

---

## 🏆 TOP 3 HERRAMIENTAS RECOMENDADAS

### 1. SonarQube Community Edition ⭐⭐⭐⭐⭐

**Tipo:** Open Source, auto-hospedado  
**Coste:** €0 (Community Edition)  
**Privacidad:** 🟢 Excelente (tu servidor)

#### ✅ Ventajas
- **Análisis completo:** Code smells, bugs, vulnerabilidades, deuda técnica
- **35+ lenguajes:** Python, TypeScript, JavaScript, etc.
- **Reglas GDPR:** Puede configurarse para detectar violaciones
- **Métricas detalladas:** Cobertura, complejidad, duplicación
- **Integración CI/CD:** GitHub Actions, GitLab CI
- **Histórico:** Tracking de calidad en el tiempo
- **Gratis:** Community Edition sin límites

#### ❌ Desventajas
- Requiere servidor (Docker)
- Configuración inicial compleja
- No tiene IA nativa (solo análisis estático)

#### 📊 Qué detecta
```
✅ Bugs y code smells
✅ Vulnerabilidades de seguridad (OWASP Top 10)
✅ Secretos expuestos (API keys, passwords)
✅ Deuda técnica
✅ Complejidad ciclomática
✅ Duplicación de código
✅ Cobertura de tests
⚠️  GDPR (con reglas custom)
❌ Legislación española específica (requiere reglas custom)
```

#### 🚀 Implementación
```bash
# Docker Compose
docker run -d --name sonarqube \
  -p 9000:9000 \
  sonarqube:community

# Escanear proyecto
npm install -g sonarqube-scanner
sonar-scanner \
  -Dsonar.projectKey=opositaia \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000
```

**Tiempo setup:** 2-3 horas  
**Tiempo primer scan:** 10-15 minutos

---

### 2. Snyk ⭐⭐⭐⭐⭐

**Tipo:** SaaS + CLI local  
**Coste:** €0 (Free tier: 200 tests/mes)  
**Privacidad:** 🟡 Media (SaaS pero no almacena código)

#### ✅ Ventajas
- **Vulnerabilidades:** Base de datos actualizada diariamente
- **Dependencias:** Escanea npm, pip, requirements.txt
- **Licencias:** Detecta licencias incompatibles
- **Fix automático:** Sugiere actualizaciones seguras
- **Integración GitHub:** PR checks automáticos
- **CLI local:** Escanea sin subir código
- **Gratis:** 200 tests/mes suficiente para MVP

#### ❌ Desventajas
- Limitado a dependencias (no analiza tu código custom)
- Free tier limitado
- Requiere cuenta

#### 📊 Qué detecta
```
✅ Vulnerabilidades en dependencias (CVE)
✅ Licencias incompatibles
✅ Dependencias obsoletas
✅ Secretos en código
✅ Docker vulnerabilities
✅ IaC security (Terraform, K8s)
❌ Bugs en tu código
❌ GDPR
❌ Legislación española
```

#### 🚀 Implementación
```bash
# Instalar
npm install -g snyk

# Autenticar
snyk auth

# Escanear
snyk test

# Monitorear
snyk monitor

# GitHub Action
# .github/workflows/snyk.yml
```

**Tiempo setup:** 30 minutos  
**Tiempo primer scan:** 2-3 minutos

---

### 3. Workik AI ⭐⭐⭐⭐

**Tipo:** SaaS con IA  
**Coste:** €0 (Free tier con limitaciones)  
**Privacidad:** 🟡 Media (SaaS)

#### ✅ Ventajas
- **IA contextual:** Entiende tu proyecto completo
- **Múltiples modelos:** Gemini, Claude, Llama, Mistral
- **Integración GitHub:** Conecta tu repo
- **Revisión inteligente:** Detecta bugs lógicos
- **Sugerencias:** Mejoras de rendimiento y arquitectura
- **Documentación:** Genera docs automáticamente
- **Gratis:** Plan free disponible

#### ❌ Desventajas
- SaaS (tu código va a sus servidores)
- Free tier limitado
- No específico para GDPR/legislación

#### 📊 Qué detecta
```
✅ Bugs lógicos
✅ Vulnerabilidades de seguridad
✅ Optimizaciones de rendimiento
✅ Mejoras de arquitectura
✅ Code smells
✅ Sugerencias de refactoring
⚠️  GDPR (depende del prompt)
❌ Legislación española específica
```

#### 🚀 Implementación
```
1. Crear cuenta en workik.com
2. Conectar repositorio GitHub
3. Configurar contexto (DB schema, APIs, etc.)
4. Ejecutar análisis con IA
5. Revisar sugerencias
```

**Tiempo setup:** 1 hora  
**Tiempo primer análisis:** 5-10 minutos

---

## 🔧 HERRAMIENTAS COMPLEMENTARIAS

### 4. agentic-radar ⭐⭐⭐⭐

**Tipo:** Open Source, local  
**Coste:** €0  
**Privacidad:** 🟢 Excelente (100% local)

#### ✅ Específico para sistemas multi-agente
- **Arquitectura de agentes:** Visualiza flujos
- **Vulnerabilidades IA:** Prompt injection, jailbreaks
- **Dependencias:** CVEs en librerías de IA
- **Interacciones:** Detecta loops infinitos
- **Seguridad:** Validación de inputs/outputs

#### 📊 Perfecto para OpositaIA
```
✅ Analiza tus agentes (RAG, QA, generadores)
✅ Detecta vulnerabilidades en prompts
✅ Verifica flujos de agentes
✅ CVEs en transformers, qdrant-client, etc.
✅ Visualiza arquitectura
```

#### 🚀 Implementación
```bash
# Instalar
pip install agentic-radar

# Escanear
agentic-radar scan ./backend/agents

# Visualizar
agentic-radar visualize
```

**Tiempo setup:** 30 minutos  
**Uso:** Específico para auditar agentes IA

---

### 5. Qodo (ex Codium) ⭐⭐⭐⭐

**Tipo:** SaaS + GitHub App  
**Coste:** €0 (open source projects)  
**Privacidad:** 🟡 Media (SaaS)

#### ✅ Ventajas
- **PR reviews:** Automáticas con IA
- **Tests:** Genera tests automáticamente
- **Documentación:** Actualiza docs en PRs
- **Políticas:** Detecta violaciones de estándares
- **Gratis:** Para proyectos open source

#### 📊 Qué ofrece
```
✅ Revisión automática de PRs
✅ Generación de tests
✅ Actualización de docs
✅ Detección de breaking changes
✅ Sugerencias de mejora
```

**Uso:** Integrar en GitHub para PRs automáticos

---

### 6. GuardRails ⭐⭐⭐⭐

**Tipo:** CLI local, open source  
**Coste:** €0 (usa tu API key)  
**Privacidad:** 🟢 Excelente (100% local)

#### ✅ Ventajas
- **100% local:** Tu código no sale de tu máquina
- **Tu API key:** OpenAI, Gemini, Claude, etc.
- **Completo:** Vulnerabilidades, secretos, code smells
- **Tests:** Genera tests automáticamente
- **Commits:** Mensajes de commit inteligentes
- **Docs:** Genera documentación

#### 📊 Qué detecta
```
✅ Vulnerabilidades
✅ Secretos expuestos
✅ Code smells
✅ Bugs potenciales
✅ Optimizaciones
```

#### 🚀 Implementación
```bash
# Instalar (buscar en GitHub)
npm install -g guardrails-cli

# Configurar API key
export OPENAI_API_KEY=tu-key

# Escanear
guardrails scan .

# Generar tests
guardrails generate-tests
```

**Tiempo setup:** 30 minutos  
**Coste:** Solo API calls (~$1-5 por scan completo)

---

## 🆕 HERRAMIENTAS ADICIONALES INVESTIGADAS

### 7. Semgrep ⭐⭐⭐⭐⭐

**Tipo:** Open Source + SaaS  
**Coste:** €0 (Community)  
**Privacidad:** 🟢 Excelente (puede ser local)

#### ✅ Ventajas
- **Reglas custom:** Puedes crear reglas para GDPR/LOPDGDD
- **Rápido:** Análisis en segundos
- **30+ lenguajes:** Python, TypeScript, etc.
- **SAST:** Static Application Security Testing
- **Gratis:** Community edition completa

#### 📊 Específico para legislación
```
✅ Reglas custom para GDPR
✅ Reglas custom para LOPDGDD
✅ Detecta PII (datos personales)
✅ Verifica consentimiento
✅ Audita logs de acceso
```

#### 🚀 Implementación
```bash
# Instalar
pip install semgrep

# Escanear con reglas GDPR
semgrep --config=p/gdpr .

# Crear reglas custom para LOPDGDD
# rules/lopdgdd.yml
```

**Tiempo setup:** 1 hora  
**Ventaja:** Puedes crear reglas específicas para legislación española

---

### 8. CodeQL (GitHub) ⭐⭐⭐⭐

**Tipo:** Open Source (GitHub)  
**Coste:** €0 (repos públicos)  
**Privacidad:** 🟡 Media (GitHub)

#### ✅ Ventajas
- **Queries SQL-like:** Busca patrones complejos
- **Seguridad:** Detecta vulnerabilidades avanzadas
- **Integración GitHub:** Automático en repos públicos
- **Base de datos:** Convierte código en BD queryable

#### 📊 Qué detecta
```
✅ Vulnerabilidades complejas
✅ Injection attacks (SQL, XSS, etc.)
✅ Path traversal
✅ Insecure deserialization
✅ Patrones custom
```

**Uso:** Activar en GitHub Security → Code scanning

---

### 9. Trivy ⭐⭐⭐⭐

**Tipo:** Open Source, CLI  
**Coste:** €0  
**Privacidad:** 🟢 Excelente (local)

#### ✅ Ventajas
- **Contenedores:** Escanea Docker images
- **IaC:** Terraform, K8s, Docker Compose
- **Dependencias:** npm, pip, etc.
- **Secretos:** API keys, passwords
- **Rápido:** Scan en segundos

#### 📊 Perfecto para tu stack
```
✅ Docker images (PostgreSQL, Qdrant)
✅ docker-compose.yml
✅ requirements.txt (Python)
✅ package.json (Node)
✅ Secretos en .env
```

#### 🚀 Implementación
```bash
# Instalar
brew install trivy

# Escanear imagen
trivy image postgres:latest

# Escanear proyecto
trivy fs .

# Escanear docker-compose
trivy config docker-compose.yml
```

**Tiempo setup:** 15 minutos

---

## 📋 COMPARATIVA COMPLETA

| Herramienta | Tipo | Coste | Privacidad | Bugs | Security | GDPR | Legislación ES | IA | Agentes |
|-------------|------|-------|------------|------|----------|------|----------------|----|---------| 
| **SonarQube** | OSS | €0 | 🟢 | ✅ | ✅ | ⚠️ | ⚠️ | ❌ | ❌ |
| **Snyk** | SaaS | €0* | 🟡 | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Workik AI** | SaaS | €0* | 🟡 | ✅ | ✅ | ⚠️ | ❌ | ✅ | ❌ |
| **agentic-radar** | OSS | €0 | 🟢 | ⚠️ | ✅ | ❌ | ❌ | ✅ | ✅ |
| **Qodo** | SaaS | €0* | 🟡 | ✅ | ⚠️ | ❌ | ❌ | ✅ | ❌ |
| **GuardRails** | CLI | API | 🟢 | ✅ | ✅ | ⚠️ | ❌ | ✅ | ❌ |
| **Semgrep** | OSS | €0 | 🟢 | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **CodeQL** | OSS | €0* | 🟡 | ✅ | ✅ | ⚠️ | ⚠️ | ❌ | ❌ |
| **Trivy** | OSS | €0 | 🟢 | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |

**Leyenda:**
- €0 = Gratis
- €0* = Gratis con limitaciones
- API = Coste de API calls
- 🟢 = Excelente (local)
- 🟡 = Media (SaaS)
- 🔴 = Baja (almacena código)

---

## 🎯 RECOMENDACIÓN FINAL PARA OPOSITAIA

### Stack Completo de Auditoría

#### 1. **SonarQube Community** (Base)
**Propósito:** Análisis estático completo  
**Coste:** €0  
**Setup:** 2-3 horas  
**Uso:** Scan semanal + CI/CD

**Qué audita:**
- Bugs y code smells
- Vulnerabilidades OWASP
- Deuda técnica
- Complejidad
- Duplicación

---

#### 2. **Semgrep** (GDPR + LOPDGDD)
**Propósito:** Reglas custom para legislación  
**Coste:** €0  
**Setup:** 1 hora  
**Uso:** Scan diario + pre-commit

**Qué audita:**
- GDPR compliance
- LOPDGDD (reglas custom)
- PII (datos personales)
- Consentimiento
- Logs de acceso

**Reglas custom a crear:**
```yaml
# rules/lopdgdd.yml
rules:
  - id: lopdgdd-pii-without-consent
    pattern: |
      user.email
      user.dni
      user.phone
    message: "Datos personales sin verificar consentimiento"
    
  - id: lopdgdd-data-retention
    pattern: |
      DELETE FROM users WHERE ...
    message: "Verificar período de retención LOPDGDD"
```

---

#### 3. **Snyk** (Dependencias)
**Propósito:** Vulnerabilidades en librerías  
**Coste:** €0 (200 tests/mes)  
**Setup:** 30 minutos  
**Uso:** Scan en cada PR

**Qué audita:**
- CVEs en dependencias
- Licencias incompatibles
- Actualizaciones de seguridad

---

#### 4. **agentic-radar** (Agentes IA)
**Propósito:** Seguridad de agentes  
**Coste:** €0  
**Setup:** 30 minutos  
**Uso:** Scan mensual

**Qué audita:**
- Prompt injection
- Flujos de agentes
- Vulnerabilidades IA
- CVEs en librerías IA

---

#### 5. **Trivy** (Contenedores)
**Propósito:** Docker y IaC  
**Coste:** €0  
**Setup:** 15 minutos  
**Uso:** Scan en cada build

**Qué audita:**
- Docker images
- docker-compose.yml
- Secretos en archivos

---

#### 6. **Workik AI** (Opcional - Revisión IA)
**Propósito:** Revisión inteligente  
**Coste:** €0 (limitado)  
**Setup:** 1 hora  
**Uso:** Scan mensual o antes de releases

**Qué audita:**
- Bugs lógicos
- Optimizaciones
- Arquitectura

---

## 🚀 PLAN DE IMPLEMENTACIÓN

### Fase 1: Setup Básico (1 día)
```bash
# 1. SonarQube (2h)
docker-compose up -d sonarqube
sonar-scanner

# 2. Snyk (30min)
npm install -g snyk
snyk auth
snyk test

# 3. Trivy (15min)
brew install trivy
trivy fs .
```

### Fase 2: Legislación (2 horas)
```bash
# 4. Semgrep + reglas GDPR/LOPDGDD
pip install semgrep
semgrep --config=p/gdpr .

# Crear reglas custom
# rules/lopdgdd.yml
```

### Fase 3: Agentes IA (1 hora)
```bash
# 5. agentic-radar
pip install agentic-radar
agentic-radar scan ./backend/agents
```

### Fase 4: CI/CD (2 horas)
```yaml
# .github/workflows/security.yml
name: Security Audit
on: [push, pull_request]
jobs:
  sonarqube:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: SonarQube Scan
        run: sonar-scanner
  
  snyk:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Snyk Test
        run: snyk test
  
  semgrep:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Semgrep GDPR
        run: semgrep --config=p/gdpr .
```

---

## 💰 COSTE TOTAL

**Setup:** 0€  
**Mensual:** 0€ (todo gratis)  
**Tiempo setup:** 1 día  
**Tiempo mantenimiento:** 2 horas/semana

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

- [ ] Instalar SonarQube (Docker)
- [ ] Configurar Snyk
- [ ] Instalar Semgrep
- [ ] Crear reglas LOPDGDD custom
- [ ] Instalar agentic-radar
- [ ] Instalar Trivy
- [ ] Configurar GitHub Actions
- [ ] Primer scan completo
- [ ] Revisar y priorizar issues
- [ ] Documentar proceso

---

## 📊 RESULTADO ESPERADO

Después de implementar este stack tendrás:

✅ **Seguridad:** Vulnerabilidades detectadas y priorizadas  
✅ **GDPR:** Compliance verificado automáticamente  
✅ **LOPDGDD:** Reglas custom para legislación española  
✅ **Calidad:** Code smells y deuda técnica medida  
✅ **Agentes:** Seguridad de sistema multi-agente  
✅ **Dependencias:** CVEs detectados y actualizados  
✅ **Contenedores:** Docker images seguras  
✅ **CI/CD:** Auditoría automática en cada PR  

---

**Documento creado:** 25 Noviembre 2025  
**Próxima acción:** Implementar Fase 1 (Setup Básico)
