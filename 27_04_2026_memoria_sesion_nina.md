# Memoria de sesión — Compilación Agente Escritor para Nina
**Fecha:** 27 de abril de 2026
**Hora:** 02:35 → 03:35 UTC+02:00
**Duración:** ~1 h
**Operador:** Spas (WSL2 Ubuntu 24.04 sobre Windows)
**Destinataria final:** Nina (Windows 10, sin Python ni WSL, máquina lenta)

---

## 1. Objetivo de la sesión

Cerrar el ciclo del **Agente Escritor**: convertirlo de un script Python que solo
funciona en mi WSL a un **ejecutable Windows independiente** (`AgenteEscritor.exe`)
que Nina pueda usar en su máquina lenta sin instalar nada y resistente a reinicios
y a tocar configuraciones por error.

Tareas heredadas del checkpoint anterior:

1. Quitar la inyección forzada de fecha del system prompt (ya hecha en sesión 26/04).
2. Cambiar `MISTRAL_AGENT_MODEL` a `mistral-medium-latest` (ya hecho).
3. Añadir `TAVILY_API_KEY` al `.env.backend` (ya hecho).
4. Reiniciar proxy y verificar `/health` (ya hecho).
5. **Compilar el proxy a `AgenteEscritor.exe` con PyInstaller (Windows x64).** ← foco de hoy
6. **Preparar paquete distribuible para Nina.** ← foco de hoy

---

## 2. Estrategia de compilación elegida

**Problema:** estoy en WSL Linux y necesito producir un `.exe` para Windows nativo.
Tres caminos posibles:

| Opción | Ventajas | Desventajas |
|---|---|---|
| Instalar Wine + Python Windows en WSL | Control total | 2-3 GB de instalación, configuración manual |
| Compilar en la propia máquina de Nina | Nativo | Nina no tiene Python ni sabe usar terminal |
| **Cross-compile vía Docker (Wine + Python + PyInstaller en imagen)** | Reproducible, aislado, sin tocar mi sistema | Bajar ~1.5 GB de imagen una vez |

**Elegida: Docker.** Ya tenía Docker 27.5.1 instalado (`/usr/bin/docker`).

### Imagen Docker usada

```
batonogov/pyinstaller-windows:latest
sha256:d718ceb48e5d49a83ae17ab0cc60d617b01fab72efd6fc61d02486a748e04b5a
```

Contiene:

- Wine (para correr binarios Windows en Linux)
- Python 3.13 Windows
- PyInstaller
- Entrypoint `bash` que ejecuta `pip install -r requirements.txt` antes del build,
  y luego pasa los argumentos como `sh -c "$@"`.

**Repositorio fuente:** https://github.com/batonogov/docker-pyinstaller

---

## 3. Proceso paso a paso

### 3.1. Preparar directorio de build aislado

```bash
mkdir -p /home/spas/build_agente
cp /home/spas/OPOS_GEMINI_1/backend/proxy_agente_escritor.py /home/spas/build_agente/
```

### 3.2. Crear `requirements.txt` minimalista

Solo las 7 dependencias del proxy (no las 80+ del backend completo):

```
fastapi==0.115.0
uvicorn[standard]==0.32.0
requests==2.32.5
beautifulsoup4==4.12.0
python-dotenv==1.2.1
mistralai==1.10.0
pydantic==2.12.5
```

Archivo: `/home/spas/build_agente/requirements.txt` (139 bytes).

### 3.3. Adaptar el código para Windows nativo

Tres ediciones críticas en `proxy_agente_escritor.py` (copia en build dir, NO en el original del repo):

**a) `import sys` movido al top de imports.**

**b) `detectar_ip_windows()` renombrada a `detectar_ip_host_desde_wsl()` y `get_obsidian_base_url()` ahora detecta el OS:**

```python
def get_obsidian_base_url() -> str:
    if OBSIDIAN_REST_URL_ENV:
        return OBSIDIAN_REST_URL_ENV
    # Windows nativo: el .exe corre en la misma máquina que Obsidian
    if sys.platform.startswith("win"):
        return f"http://127.0.0.1:{OBSIDIAN_PORT}"
    # Linux/WSL: hay que cruzar a Windows host
    ip = detectar_ip_host_desde_wsl()
    if ip:
        return f"http://{ip}:{OBSIDIAN_PORT}"
    return f"http://127.0.0.1:{OBSIDIAN_PORT}"
```

Esto es **clave**: en Windows nativo Obsidian REST está en `127.0.0.1`, no hay
que `ip route` (comando que no existe en Windows) ni cruzar a host.

**c) Carga del `.env` portable para PyInstaller `--onefile`:**

```python
# Compatible con script normal (.py) y con bundle PyInstaller (.exe).
# Para PyInstaller --onefile, sys.executable apunta al .exe en disco;
# __file__ apuntaría al dir temporal _MEIxxx (no útil para el usuario).
if getattr(sys, "frozen", False):
    APP_DIR = Path(sys.executable).resolve().parent
else:
    APP_DIR = Path(__file__).resolve().parent

for _candidate in (".env", ".env.backend"):
    _env_path = APP_DIR / _candidate
    if _env_path.exists():
        load_dotenv(_env_path)
        break
```

Sin esto, el `.exe` empaquetado buscaría el `.env` en un directorio temporal
(`C:\Users\…\AppData\Local\Temp\_MEIxxx\`) que se borra al cerrarse, y nunca
encontraría el `.env` que Nina pone al lado del `.exe`.

**d) Eliminada llamada duplicada `uvicorn.run(...)` al final del fichero.**

### 3.4. Pull de la imagen Docker

```bash
docker pull batonogov/pyinstaller-windows:latest
# ~1.5 GB descargados, varias capas
```

### 3.5. Build (intentos)

**Intento 1** (falló): pasé los flags de PyInstaller como argumentos sueltos.
El entrypoint hace `sh -c "$@"` y los `--onefile --name …` se interpretaron como
opciones de `sh` → `sh: 0: Illegal option --`.

**Intento 2** (falló): pasé un solo string sin `pyinstaller` al inicio. Mismo error.

**Intento 3** (OK): el comando entero, incluyendo `pyinstaller`, en una sola string:

```bash
docker run --rm -v /home/spas/build_agente:/src \
  batonogov/pyinstaller-windows:latest \
  "pyinstaller --onefile --name AgenteEscritor --collect-submodules uvicorn proxy_agente_escritor.py"
```

Tiempo total: ~3 min (instala deps + analiza imports + empaqueta + bootloader).

**Resultado:**

```
/home/spas/build_agente/dist/AgenteEscritor.exe
PE32+ executable (console) x86-64, for MS Windows
18 MB
```

### 3.6. Test del .exe en Wine (sanity check)

Lanzado el .exe dentro del propio container Docker, con el `.env` al lado:

```
2026-04-27 01:28:22 [INFO] 🔗 Obsidian URL: http://127.0.0.1:27123  ✅ detecta Windows
2026-04-27 01:28:22 [INFO] 🤖 Mistral model: mistral-medium-latest o mistral latest   ✅ lee .env
INFO:     Started server process [224]
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 ✅ servidor levantado
```

Sin warnings de keys faltantes → el `.env` se carga bien por la lógica `frozen`.

Los errores de Wine sobre Vulkan/EGL/winebth son esperables en container sin
display y NO ocurrirán en Windows real.

---

## 4. Paquete distribuible final

### 4.1. Carpeta `D:\AgenteEscritor_Para_Nina\`

| Archivo | Tamaño | Descripción |
|---|---|---|
| `AgenteEscritor.exe` | 18 MB | Proxy compilado, Windows x64 |
| `.env` | 1.7 KB | Config real con `MISTRAL_API_KEY`, `MISTRAL_AGENT_MODEL=mistral-medium-latest`, `TAVILY_API_KEY`, `OBSIDIAN_REST_API_KEY`, `PROXY_PORT=8000` |
| `1_arrancar.bat` | 1.6 KB | Doble clic → arranca el .exe, comprueba existencia de `.env` y `.exe` antes |
| `2_parar.bat` | 0.5 KB | Doble clic → `taskkill /F /IM AgenteEscritor.exe` |
| `3_verificar.bat` | 1.2 KB | Doble clic → comprueba proceso vivo, salud `/health`, Obsidian REST en 27123 |
| `LEEME.txt` | 3.4 KB | Manual en castellano simple para Nina (qué hace, cómo usar, problemas frecuentes, seguridad, contacto) |

### 4.2. ZIP empaquetado

```
D:\AgenteEscritor_Para_Nina.zip   (17.6 MB)
```

Generado con `zipfile.ZIP_DEFLATED` (compresslevel=6) directamente desde Python
porque WSL no tenía `zip` instalado (sí tenía `unzip`). Estructura:

```
AgenteEscritor_Para_Nina/
├── .env
├── 1_arrancar.bat
├── 2_parar.bat
├── 3_verificar.bat
├── AgenteEscritor.exe
└── LEEME.txt
```

---

## 5. Decisiones de diseño relevantes

### 5.1. Por qué un `.env` simple en vez de `.env.backend`

Para Nina, "configuración" debe ser obvia. `.env` es el nombre estándar que
cualquier guía de internet menciona. `.env.backend` se mantiene como nombre
**alternativo** en el código (compatibilidad con el repo de desarrollo) gracias
al loop `for _candidate in (".env", ".env.backend")`.

### 5.2. Por qué `mistral-medium-latest` y no `large`

- Cuota mejor en el plan gratuito (1 req/seg contra 1/2 seg del large).
- Suficientemente bueno para tareas literarias y administrativas.
- Más rápido en máquinas lentas porque el bottleneck es la latencia de red,
  no el modelo, pero Mistral medium es noticeably más rápido en TTFT.

### 5.3. Por qué Tavily como motor de búsqueda principal

- API estable y filtrable por fecha (anti-alucinaciones temporales).
- Plan gratuito 1.000 búsquedas/mes (más que de sobra para Nina).
- DuckDuckGo HTML scraping queda como fallback si Tavily falla.

### 5.4. Por qué scripts `.bat` numerados

UX para quien no es técnico:

- `1_arrancar.bat` → empezar
- `2_parar.bat` → parar
- `3_verificar.bat` → arreglar / diagnosticar

Orden numérico → orden de uso normal.

### 5.5. Por qué NO un servicio Windows / autoarranque

Discutido para próxima sesión:

- Servicio Windows requiere `nssm` o similar → instalación adicional.
- Tarea programada al login funciona pero esconde la ventana de logs y Nina no
  vería errores en pantalla.
- **Decisión actual:** Nina abre `1_arrancar.bat` cuando vaya a usar el agente.
  Es 1 doble clic más al día, pero la ventana visible le da feedback claro.

---

## 6. Verificaciones realizadas

| Check | Resultado |
|---|---|
| Sintaxis Python del proxy adaptado | OK (`ast.parse`) |
| Build PyInstaller termina sin errores | OK (mensaje "Build complete!") |
| Tipo de binario | PE32+ x86-64 console MS Windows |
| Tamaño binario | 18 MB |
| Arranque en Wine sin `.env` | Logs warning correctos, server arranca igualmente |
| Arranque en Wine con `.env` al lado | Lee model `mistral-medium-latest`, sin warnings, server arranca |
| Detección Windows nativo | `Obsidian URL: http://127.0.0.1:27123` correcto |
| ZIP descomprime con `unzip -l` | Lista los 6 ficheros con sizes correctos |

---

## 7. Pendientes / próxima sesión

### 7.1. Inmediato (cuando Nina pruebe)

- [ ] Confirmar que su antivirus no marca el .exe como falso positivo (PyInstaller).
- [ ] Verificar que `1_arrancar.bat` arranca limpio y muestra "Application startup complete".
- [ ] Verificar que Copilot/BMO en Obsidian responde con el modelo `agente-escritor`.
- [ ] Confirmar que `search_internet` devuelve resultados con fecha 2026 correcta.

### 7.2. Mejoras futuras (siguiente iteración)

- [ ] **Auto-update del .exe**: que `1_arrancar.bat` chequee versión y avise si hay
      una nueva en un endpoint público.
- [ ] **Logs persistentes**: redirigir stdout/stderr a `logs/agente_YYYY-MM-DD.log`.
- [ ] **Cifrado del .env**: que las keys no estén en texto plano (al menos
      ofuscación con DPAPI Windows).
- [ ] **Modo "watchdog"**: si el proceso muere, relanzarlo. Quizá vía `nssm` o
      script PS que reinicie cada N segundos.
- [ ] **Tray icon**: que aparezca en la bandeja del sistema con menú "Parar /
      Reiniciar / Logs". Esto requiere `pystray` + ícono.
- [ ] **Cloud proxy alternativo**: opción para Nina de NO levantar nada local
      y conectar a un proxy mío en Render/Fly que ella ataque por túnel HTTPS.

### 7.3. Las 6 entidades del Plan Serie Turca (21/04/2026) — registradas hoy ✅

El usuario me recordó que las 6 entidades pendientes correspondían al **Plan
Serie Turca** del 21/04/2026 (`@/home/spas/OPOS_GEMINI_1/21_04_2026_PLAN_SERIE_TURCA.md`),
que se quedó solo en disco — nunca se reflejó en el grafo MCP. Deuda saldada
hoy 27/04/2026 (6 días después). Las 6 entidades creadas:

| # | Entidad MCP | Tipo | Resumen |
|---|---|---|---|
| 1 | `Plan_Serie_Turca_21_04_2026` | MasterPlan | Plan maestro 466 líneas. Cuerpo Adm SS C1 (BOE-A-2025-27158). Método NEXO. Diferenciación de DM con rigor legal + memorabilidad narrativa. |
| 2 | `Personajes_Ciclo_Vital_OPOS` | PedagogicalCharacters | 6 protagonistas: **Amparo Rodríguez (23)**, **Darío Méndez (35)**, **Pilar Sáez (42)**, **Bartolomé Cañete (51)**, **Carmen Ibáñez (58)**, **Estanislao Vela (72)** + relaciones familiares cruzadas (Amparo↔Carmen, Darío↔Bartolomé, Estanislao↔Bartolomé, Carmen↔Darío). |
| 3 | `Arquitectura_3_Capas_Wiki` | Architecture | **Capa 1 Técnica** (13 fichas BOE) + **Capa 2 Narrativa** (capítulos serie turca) + **Capa 3 Práctica** (trampas YAML + calculadoras + simulacros), todas interconectadas por wikilinks Obsidian. |
| 4 | `Modo_Minimal_Regenerador` | ProposedFeature | Flag `--minimal` para `regenerar_vault_trampas.py`. Doble salida: `wiki/` (interno, todo) + `wiki_publico_minimal/` (publicable, allowlist de 5 campos). 2h código estimadas. |
| 5 | `Ideas_Creativas_Wiki_12` | FeatureBacklog | 12 mejoras opcionales: **A** árbol leyes con backlinks, **B** matriz 13×13, **C** Error Museum, **D** timeline legal, **E** calculadoras embebidas, **F** flowcharts Mermaid, **G** falsos amigos, **H** mapa maestro, **I** glosario siglas, **J** wiki tropos, **L** formularios oficiales, **M** export Anki. **K** (TTS) descartada. |
| 6 | `Estrategia_Diferenciacion_Legal_DM` | LegalStrategy | Qué SÍ es libre (BOE, datos, jurisprudencia) vs qué NO se puede copiar de DM (redacción, ejemplos, esquemas, tono). Estrategia limpia: BOE como fuente primaria + ejemplos propios con los 6 personajes. |

**Relaciones MCP creadas (18):** Las 6 entidades quedan vinculadas a
`Plan_Wiki_NEXO_v5_1`, `Trampas_Verificadas_184_19_04_26`, `Catalogo_Trampas_100`,
`Script_regenerar_vault_trampas_v2`, `Patron_LLM_Wiki_Karpathy`,
`Patron_WikiForge_Chavi`, `Skill_WikiForge_OPOS`, `OpositAIA` y
`Sesion_20_04_26_Limpieza_Vault_Total`.

**Decisiones del Plan Serie Turca aún pendientes** (sección 10 del plan original):

1. Confirmar nombres/edades definitivos de los 6 personajes.
2. Orden de arranque: **FASE 2** (modo minimal regenerador, 2h) **vs FASE 1** (fichas personajes). El plan recomienda FASE 2 primero.
3. Rol de Pilar: abogada-autónoma (vehículo pedagógico) vs autónoma pura.
4. Publicación de `wiki_publico_minimal/`: GitHub / GitLab / Obsidian Publish / privado.
5. Tratamiento de marca **MC MUTUAL**: genérico, dejarla, o ficticia tipo "Mutua Horizonte".

---

## 8. Comandos clave (para repetir el proceso si se rompe el .exe)

```bash
# 1. Pull imagen (solo la 1ª vez)
docker pull batonogov/pyinstaller-windows:latest

# 2. Sincronizar fuente
cp /home/spas/OPOS_GEMINI_1/backend/proxy_agente_escritor.py /home/spas/build_agente/
# (si has tocado el proxy original, hay que reaplicar las 4 ediciones de §3.3)

# 3. Compilar
docker run --rm -v /home/spas/build_agente:/src \
  batonogov/pyinstaller-windows:latest \
  "pyinstaller --onefile --name AgenteEscritor --collect-submodules uvicorn proxy_agente_escritor.py"

# 4. Copiar al paquete y zipear
cp /home/spas/build_agente/dist/AgenteEscritor.exe /mnt/d/AgenteEscritor_Para_Nina/
python3 -c "
import zipfile; from pathlib import Path
src = Path('/mnt/d/AgenteEscritor_Para_Nina')
with zipfile.ZipFile('/mnt/d/AgenteEscritor_Para_Nina.zip','w',zipfile.ZIP_DEFLATED,6) as zf:
    for f in src.iterdir():
        zf.write(f, f'AgenteEscritor_Para_Nina/{f.name}')
"
```

---

## 9. Archivos relevantes (rutas absolutas)

**Build artefacts (Linux WSL):**
- `/home/spas/build_agente/proxy_agente_escritor.py` — fuente adaptada Win
- `/home/spas/build_agente/requirements.txt` — deps minimal
- `/home/spas/build_agente/.env` — copia del .env final
- `/home/spas/build_agente/dist/AgenteEscritor.exe` — el binario

**Distribución (D: drive Windows):**
- `/mnt/d/AgenteEscritor_Para_Nina/` — carpeta lista
- `/mnt/d/AgenteEscritor_Para_Nina.zip` — para enviar a Nina

**Repo OPOS (sin tocar en esta sesión, sigue funcional):**
- `/home/spas/OPOS_GEMINI_1/backend/proxy_agente_escritor.py` — versión original WSL
- `/home/spas/OPOS_GEMINI_1/backend/.env.backend` — config dev

**Docs:**
- `/home/spas/OPOS_GEMINI_1/25_04_26_plan_agente_escritor.md` — plan v2.0 (anterior)
- `/home/spas/OPOS_GEMINI_1/24_04_2026_MEMORIA_OBSIDIAN_API_agentes.md` — memoria base
- `/home/spas/OPOS_GEMINI_1/27_04_2026_memoria_sesion_nina.md` — **este archivo**
- `/mnt/d/AgenteEscritor_Para_Nina/LEEME.txt` — manual usuaria final

---

## 10. Resumen ejecutivo (TL;DR)

> Hoy se compiló el proxy `proxy_agente_escritor.py` a un ejecutable Windows
> standalone de **18 MB** (`AgenteEscritor.exe`) usando la imagen Docker
> `batonogov/pyinstaller-windows:latest`. Se adaptó el código para detectar
> Windows nativo (Obsidian en `127.0.0.1`) y para cargar el `.env` desde el
> directorio del `.exe` cuando está empaquetado con PyInstaller `--onefile`.
> Se preparó la carpeta `D:\AgenteEscritor_Para_Nina\` con .exe + .env (con
> claves reales de Mistral medium y Tavily) + 3 scripts .bat numerados +
> LEEME.txt. Todo empaquetado en `D:\AgenteEscritor_Para_Nina.zip` (17.6 MB)
> listo para enviar a Nina. **Nina solo tendrá que descomprimir y doble clic
> en `1_arrancar.bat`.** Verificado en Wine: arranca, lee `.env`, detecta
> Windows, levanta Uvicorn en :8000, sin warnings.
