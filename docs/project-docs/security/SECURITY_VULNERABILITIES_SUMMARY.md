# Informe de Vulnerabilidades y Mitigaciones (sin cambios de código)

Este documento resume las principales vulnerabilidades detectadas en el repositorio OPOS_GEMINI_1 y propone **medidas de mitigación sin modificar el código fuente actual**. Las medidas se centran en configuración, despliegue, permisos, entorno y procesos.

> Nota: Este informe complementa a `SECURITY_AUDIT_REPORT.md`, que se centra sobre todo en gestión de secretos. Aquí se amplía a aspectos de infraestructura, configuración y buenas prácticas operativas.

---

## 1. CORS excesivamente permisivo en backend

**Ubicación relevante**:
- `backend/main.py`

Fragmento relevante (resumen):
- Uso de `CORSMiddleware` con:
  - `allow_origins=["*"]  # TODO: Restrict in production`
  - `allow_credentials=True`

**Riesgo**:
- En producción, permitir `allow_origins="*"` junto con `allow_credentials=True` expone a:
  - Riesgo de **robo de tokens/cookies** desde orígenes no confiables.
  - Mayor superficie para ataques de **CSRF combinado con XSS** si el frontend tiene alguna vulnerabilidad.

**Mitigación SIN cambiar el código**:
1. **Configurar CORS "por entorno" en el despliegue**:
   - Definir variables de entorno (o ficheros de configuración) que el código ya pueda leer indirectamente (por ejemplo mediante un wrapper de arranque) para limitar orígenes.
   - En el **reverse proxy (Nginx, Caddy, Traefik, etc.)**, aplicar una política CORS restrictiva para peticiones públicas:
     - Permitir únicamente dominios oficiales, p.ej.: `https://app.opositaia.com` y dominios de staging.
     - Bloquear `Origin` no reconocidos.

2. **Separar el endpoint de administración / internos detrás de VPN**:
   - Si el backend se usa también para scripts internos (migraciones, herramientas), exponer esos puertos/paths solo vía:
     - VPN
     - IPs whitelisteadas
     - o una red privada (ej. VPC)

3. **Configurar cookies como `SameSite=Strict` y `Secure` a nivel de infraestructura** (si se usan cookies):
   - Forzar HTTPS en el despliegue.
   - Configurar el servidor/proxy para marcar cookies con `Secure; HttpOnly; SameSite=Strict`.

4. **WAF/Firewall de aplicación**:
   - Colocar un WAF delante del backend que filtre peticiones de orígenes anómalos y patrones maliciosos.

---

## 2. API Key de Qdrant hardcodeada en script de migración

**Ubicaciones relevantes**:
- `backend/migrate_qdrant_simple.py`
  - `API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."`
- `backend/migrate_qdrant_to_cloud.py`
  - `QDRANT_CLOUD_API_KEY = os.getenv('QDRANT_API_KEY', '<api-key-hardcodeada>')`

**Riesgo**:
- Exposición de **API keys sensibles en el repositorio**.
- Cualquiera con acceso al repo (o a un leak futuro) podría:
  - Leer, modificar o borrar colecciones en Qdrant Cloud.
  - Acceder a datos indexados potencialmente sensibles.

**Mitigación SIN cambiar el código**:
1. **Rotar inmediatamente las API keys expuestas** en el panel de Qdrant Cloud.
2. **Restringir permisos de las nuevas keys**:
   - Usar una key con permisos mínimos necesarios (principio de mínimo privilegio).
   - Crear keys distintas para:
     - Producción (sólo desde la infraestructura de producción, restringida por IP).
     - Entorno local / pruebas.
3. **Restringir acceso al repositorio**:
   - Asegurar que solo personal autorizado tenga acceso al código que todavía contiene esas keys históricas.
   - Revisar si el repo es/ha sido público y, de ser así, considerar las keys definitivamente comprometidas.
4. **Aislar datos de prueba vs producción**:
   - Garantizar que las colecciones a las que apunten esas keys expuestas sólo contengan datos de pruebas (si es posible), nunca datos reales de usuarios.
5. **Configurar reglas de red en Qdrant Cloud**:
   - Limitar acceso por IP / VPC a las instancias autorizadas.

> Aunque no modifiquemos el código, **rotar las keys y endurecer permisos** elimina el impacto de que sigan apareciendo en el histórico.

---

## 3. Contraseñas por defecto en conexiones a Postgres

**Ubicaciones relevantes**:
- `backend/database/init_db.py`
  - `password=os.getenv("POSTGRES_PASSWORD", "postgres")`
- `backend/test_database.py`
  - `POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")`

**Riesgo**:
- Si se despliega sin definir correctamente `POSTGRES_PASSWORD` en entorno, el sistema usará la contraseña por defecto `postgres`.
- Esto permite acceso no autorizado a la base de datos si el puerto es accesible desde fuera del entorno de confianza.

**Mitigación SIN cambiar el código**:
1. **Definir siempre `POSTGRES_PASSWORD` en variables de entorno de despliegue**:
   - Usar un gestor de secretos (Vault, AWS Secrets Manager, etc.) o variables seguras del proveedor de hosting.
   - Asegurarse de que en contenedores Docker / orquestador (Docker Compose, Kubernetes) se pase una contraseña robusta.

2. **Cerrar el puerto de Postgres al exterior**:
   - Asegurar que la base de datos sea accesible únicamente desde la red interna / VPC o desde hosts autorizados.
   - Configurar firewall / grupos de seguridad para no exponer el puerto 5432 a Internet.

3. **Revisar y migrar contraseñas ya desplegadas**:
   - Si en algún entorno se usó `postgres` como contraseña, cambiarla inmediatamente.
   - Revocar cualquier acceso que pudiera haberse aprovechado de esa debilidad.

4. **Monitoring y alertas**:
   - Activar logs de conexión a la BD y alertas por intentos fallidos masivos.

---

## 4. Gestión de Qdrant: endpoints y debug logs

**Ubicaciones relevantes**:
- `backend/migrate_qdrant_to_cloud.py`
  - `print(f"🔧 Debug: URL: {QDRANT_CLOUD_URL}")`
  - `print(f"🔧 Debug: API Key cargada: {QDRANT_CLOUD_API_KEY[:20]}..." ...)`
- `backend/test_database.py`
  - `CLOUD_URL = "https://b554ceb5-2169-4064-9ce7-83c8cd44cf84.europe-west3-0.gcp.cloud.qdrant.io"`

**Riesgo**:
- Aunque no se imprime la key completa, se exponen:
  - **URLs de infraestructura en cloud**.
  - Prefijos de API keys que pueden usarse para fingerprinting o ataques dirigidos.

**Mitigación SIN cambiar el código**:
1. **Ejecutar estos scripts solo en entornos de administración controlados**:
   - Máquinas de administración internas, nunca en contenedores de producción expuestos a usuarios.

2. **Redirigir o filtrar logs en producción**:
   - Configurar el entorno/producto para que estos scripts se ejecuten con salida redirigida a ficheros protegidos.
   - Ajustar niveles de logging del sistema, de forma que en entornos sensibles no se muestren logs de debug en consola compartida.

3. **No compartir logs públicamente**:
   - Asegurarse de que logs con estos mensajes no se suban a repositorios públicos, ni se envíen a canales externos sin filtrado.

4. **Segmentar colecciones y accesos**:
   - Colecciones de datos sensibles deben vivir en proyectos/instancias separadas con políticas estrictas, reduciendo el valor de la información de endpoints en estos scripts.

---

## 5. Uso intensivo de proveedores de LLM (GROQ, DeepSeek, Gemini, HF, Cohere)

**Ubicación relevante**:
- `backend/agents/llm_providers.py`

El código:
- Obtiene las API keys mediante `os.getenv()` (**correcto a nivel de secretos**).
- Envía prompts y contexto a proveedores externos.

**Riesgos** (de diseño/proceso, no de código directo):
1. **Filtrado insuficiente de datos personales o sensibles** antes de enviar texto a proveedores externos.
2. **Persistencia de datos**: algunos proveedores pueden loggear consultas según su política.
3. **Cumplimiento legal (GDPR y normativa española)** si se envían datos personales de opositores, usuarios, etc.

**Mitigación SIN cambiar el código**:
1. **Política interna de datos y prompts**:
   - Definir explícitamente qué tipo de datos está permitido enviar a los LLM:
     - Ej: solo textos normativos, resúmenes, material docente, nunca datos personales identificables de usuarios.
   - Documentarlo en manual interno y en la política de privacidad.

2. **Segmentar flujos de información**:
   - Asegurar que la capa que construye prompts (frontend o backend intermedio) **no incluya PII** (nombres reales, emails, DNIs, etc.).
   - En caso de ser inevitable, se recomienda introducir un **proxy de anonimización** que retire datos sensibles antes de llamar a los LLM.

3. **Acordar y revisar DPAs / contratos con los proveedores**:
   - Verificar que el uso de datos cumple con GDPR y legislación española.
   - Activar opciones de **"no training"** sobre datos del cliente cuando el proveedor lo ofrezca.

4. **Clasificación de datos**:
   - Establecer niveles (p.ej. Público / Interno / Confidencial / Datos personales) y permitir que solo el nivel Público/Interno viaje a los LLM externos.

5. **Logging prudente**:
   - Configurar el entorno para que logs de peticiones/respuestas de LLM **no guarden datos sensibles**:
     - Si existen adaptadores de logging en el despliegue (ej. reverse proxy, observabilidad), filtrar contenido de prompts y respuestas.

---

## 6. Scripts de migración y herramientas de administración en el mismo repositorio

**Ubicaciones relevantes (ejemplos)**:
- `backend/migrate_qdrant_simple.py`
- `backend/migrate_qdrant_to_cloud.py`
- `backend/scripts/2_create_cloud_collection.py`
- `backend/scripts/3_import_to_cloud.py`
- `backend/agents/*` usados para indexación masiva.

**Riesgo**:
- Estos scripts suelen ejecutarse con **altos privilegios** (lectura/escritura masiva en Qdrant, Postgres, etc.).
- Si un atacante obtiene acceso a cualquier entorno donde estén presentes los scripts y credenciales, puede:
  - Reindexar colecciones.
  - Borrar o corromper datos.

**Mitigación SIN cambiar el código**:
1. **Separar entornos de ejecución**:
   - Ejecutar estos scripts solo en:
     - Máquinas de administración con acceso restringido.
     - Pipelines de CI/CD con permisos mínimos.

2. **Gestión de permisos por rol**:
   - Asignar credenciales específicas para tareas de migración, con duración limitada y scopes reducidos.

3. **Control de acceso al repositorio**:
   - Limitar quién puede clonar/leer este repositorio (si es privado).

4. **Revisión y firma de cambios**:
   - Requerir pull requests y revisiones para cualquier modificación en scripts de administración.

---

## 7. Variables de entorno sensibles en máquinas de desarrollo

**Contexto**:
- El proyecto usa `.env.backend`, `.env`, `.env.local` y otros ficheros de entorno (bien gestionados a nivel de Git según `SECURITY_AUDIT_REPORT.md`).

**Riesgo**:
- Aunque no se suban a Git, en **máquinas de desarrollo** estos ficheros pueden quedar expuestos si:
  - Se hacen backups sin cifrar.
  - Se sincronizan carpetas con servicios en la nube poco seguros.
  - Se comparte la máquina con otras personas.

**Mitigación SIN cambiar el código**:
1. **Cifrado de discos y backups** en equipos de desarrollo.
2. **Uso de gestores de secretos locales** (por ejemplo, `pass`, 1Password, Bitwarden, etc.) en lugar de `.env` planos cuando sea posible.
3. **Política de rotación periódica de claves** aunque no se haya producido incidente.
4. **Formación al equipo** en manejo seguro de variables de entorno y de ficheros `.env`.

---

## 8. Ausencia de pre-commit hooks / escaneos obligatorios en todos los entornos

**Contexto**:
- `SECURITY_AUDIT_REPORT.md` recomienda instalar `git-secrets` y configurar Gitleaks en CI, pero puede que no esté **forzado** en todas las máquinas.

**Riesgo**:
- Un desarrollador que no tenga los hooks instalados puede cometer accidentalmente secretos en nuevas ramas o repos.

**Mitigación SIN cambiar el código**:
1. **Hacer obligatoria la instalación de hooks en el flujo de trabajo**:
   - Documentarlo en `SETUP.md` y políticas internas de desarrollo.
   - Añadir una comprobación en CI que falle si no se ha ejecutado el escaneo (por ejemplo, verificar salida de Gitleaks).

2. **Pipeline de CI centralizado**:
   - Asegurar que toda rama que llegue a `main` pase por un workflow con escaneo de secretos.

3. **Formación y checklist de incorporación**:
   - Incluir la instalación de hooks de seguridad como paso obligatorio de onboarding de nuevos desarrolladores.

---

## 9. Exposición de documentación técnica sensible

**Contexto**:
- El repositorio contiene numerosos documentos internos (`docs/`, `docs_bmad/`, `basura/`, etc.) con información de:
  - Arquitectura.
  - Infraestructura VPS.
  - Planes de migración, costes, etc.

**Riesgo**:
- Si el repositorio se hace público o se filtra, un atacante obtendría un **mapa detallado de la infraestructura**, facilitando ataques dirigidos.

**Mitigación SIN cambiar el código**:
1. **Mantener el repositorio como privado** en la plataforma de control de versiones.
2. **Segmentar repositorios**:
   - Separar código de aplicación del detalle de infraestructura más sensible y de credenciales operativas.

3. **Clasificar documentos** y aplicar etiquetas de sensibilidad:
   - Marcar documentos críticos como "Interno" o "Confidencial" y limitar quién puede acceder.

4. **Controlar exportaciones**:
   - Evitar compartir estos documentos por canales no seguros.

---

## 10. Gestión de errores y mensajes al usuario

**Contexto**:
- El código backend (por ejemplo `backend/routers/chat.py`, `backend/routers/ai_functions.py`) captura errores y construye respuestas para el usuario.
- No se observa, a simple vista, un desbordamiento de información en trazas, pero es un punto típico de riesgo.

**Riesgo**:
- Mensajes de error demasiado detallados podrían exponer:
  - Información interna sobre la infraestructura.
  - Stack traces con rutas locales.
  - Detalles de configuración.

**Mitigación SIN cambiar el código**:
1. **Configurar el entorno de producción en modo "no debug"**:
   - Asegurar que no se ejecuta el framework en modo debug.

2. **Configurar el servidor/reverse proxy** para servir al usuario final solo mensajes genéricos de error (5xx) y dejar detalles en logs internos.

3. **Revisar manualmente mensajes de error** en logs y UI antes de salir a producción.

---

## 11. Seguridad en despliegues Docker / Vercel / VPS

**Contexto**:
- El proyecto incluye `docker-compose.yml`, `backend/Dockerfile`, `vercel.json`, `VPS_*` docs.

**Riesgo**:
- Si las imágenes se construyen con prácticas poco seguras (usuarios root, puertos abiertos, etc.) o si en Vercel/VPS se exponen variables o endpoints innecesarios, se amplía la superficie de ataque.

**Mitigación SIN cambiar el código**:
1. **Reforzar imágenes y contenedores en la capa de infraestructura**:
   - Ejecutar contenedores como usuario no root mediante configuración de runtime (aunque el Dockerfile no cambie).
   - Limitar puertos publicados en `docker-compose.yml` y en el proveedor cloud.

2. **Aplicar hardening en el VPS**:
   - Firewall (ufw/iptables) con puertos mínimos expuestos.
   - SSH con claves, sin contraseña.
   - Actualizaciones automáticas de seguridad.

3. **Seguridad específica de Vercel**:
   - Usar solo variables de entorno necesarias.
   - No exponer páginas de debug o endpoints internos.

---

## 12. Recomendaciones organizativas generales

Más allá del código, estas prácticas reducen el riesgo global sin necesidad de modificar el repositorio:

1. **Política de seguridad escrita** adaptada a OPOSITAIA, que incluya:
   - Gestión de secretos.
   - Gestión de accesos al código y a la infraestructura.
   - Uso aceptable de datos y LLMs.

2. **Formación periódica al equipo** en:
   - Phishing, ingeniería social.
   - Buenas prácticas de desarrollo seguro.

3. **Revisión de seguridad previa a cada despliegue importante**:
   - Checklist basada en este documento y en `SECURITY_AUDIT_REPORT.md`.

4. **Plan de respuesta a incidentes**:
   - Procedimiento claro para revocar keys, aislar sistemas y notificar a usuarios si se produjera una brecha.

---

## Conclusión

- El proyecto tiene una **buena base de gestión de secretos** (según `SECURITY_AUDIT_REPORT.md`).
- Las vulnerabilidades más relevantes encontradas se concentran en:
  - Scripts con API keys hardcodeadas.
  - Configuraciones por defecto (CORS abierto, contraseñas de BD por defecto).
  - Riesgos de diseño/operativos en el uso de LLMs y en documentación de infraestructura.
- Todas las mitigaciones propuestas aquí **pueden aplicarse sin modificar el código fuente**, actuando sobre:
  - Rotación de claves y configuración de permisos.
  - Endurecimiento de infraestructura (firewalls, CORS en proxy, acceso a BD/Qdrant).
  - Procesos internos de desarrollo, despliegue y formación.
