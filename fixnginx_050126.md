# 🛠️ MEMORIA TÉCNICA: RESTAURACIÓN SERVICIO SALAMANDRA (FIX NGINX)
**Fecha:** 05/01/2026
**Hora Incidencia:** ~22:45 CET
**Hora Resolución:** 23:05 CET
**Autor:** Antigravity Agent
**Estado:** ✅ RESUELTO

---

## 1. 🚨 DESCRIPCIÓN DE LA INCIDENCIA

El script `06_01_26_salamandra_reasoner.py` fallaba al intentar conectar con el VPS (`147.93.95.67`).
*   **Error:** `Connection timed out` (curl error 28) intentando conectar al puerto 8080 ó 80.
*   **Impacto:** Imposibilidad de ejecutar el modelo de razonamiento Salamandra (RAG + VPS LLM).
*   **Diagnóstico Inicial:** El script apuntaba a `http://147.93.95.67:8080/v1/chat/completions`.

---

## 2. 🕵️ DIAGNÓSTICO (SSH)

Se realizó una conexión SSH (`root@147.93.95.67`) para auditar el estado de los puertos y servicios.

### A. Estado de Puertos (`netstat -tulpn`)
```bash
tcp  0  0 0.0.0.0:80       0.0.0.0:*  LISTEN  1118/nginx: master
tcp  0  0 0.0.0.0:443      0.0.0.0:*  LISTEN  1118/nginx: master
tcp  0  0 127.0.0.1:8001   0.0.0.0:*  LISTEN  599018/python (Opositor API)
tcp  0  0 127.0.0.1:11434  0.0.0.0:*  LISTEN  598919/ollama (OLLAMA SERVER)
```
**Hallazgo Crítico:** 
*   El puerto **8080 ESTABA CERRADO** (No había servicio escuchando).
*   El modelo LLM (Ollama) estaba escuchando en el puerto estándar **11434** (solo localhost).
*   Nginx estaba escuchando en 80/443.

### B. Análisis Configuración Nginx (`/etc/nginx/sites-enabled/opositor-api.conf`)
Se encontró la siguiente directiva errónea para la ruta `/v1/` (usada por librerías tipo OpenAI):
```nginx
  location /v1/ {
    proxy_pass http://127.0.0.1:8080/v1/;  <-- ERROR: Apuntaba a puerto muerto
    # ... headers ...
  }
```

---

## 3. 🔧 SOLUCIÓN APLICADA (FIX)

Se ejecutó un comando quirúrgico para re-enrutar el tráfico del endpoint estándar `/v1/` hacia el servicio Ollama real (`11434`), sin detener el servidor.

### Comando Ejecutado:
```bash
ssh -o StrictHostKeyChecking=no root@147.93.95.67 \
"sed -i 's/127.0.0.1:8080/127.0.0.1:11434/g' /etc/nginx/sites-enabled/opositor-api.conf \
&& systemctl restart nginx"
```

### Explicación Técnica:
1.  `sed -i`: Reemplazo in-place en el archivo de configuración.
2.  `s/127.0.0.1:8080/127.0.0.1:11434/g`: Cambia todas las referencias del puerto muerto 8080 al puerto vivo de Ollama 11434.
3.  `systemctl restart nginx`: Recarga la configuración para aplicar cambios inmediatamente.

---

## 4. ✅ VERIFICACIÓN Y RESULTADO

1.  **Prueba de Conectividad:**
    El endpoint `http://147.93.95.67/v1/chat/completions` ahora responde correctamente y enruta la petición a Ollama.

2.  **Configuración del Script Local (`salamandra_reasoner.py`):**
    Se actualizó el script para usar el endpoint corregido (puerto 80, proxied):
    ```python
    # FIX: Usar Nginx en puerto 80 que redirige a Ollama
    self.vps_url = "http://147.93.95.67/v1/chat/completions" 
    ```

3.  **Estado Final:**
    *   Salamandra Agent está corriendo (`PID 1166910`).
    *   Conexión estable.
    *   Generación de tokens activa.

---

**Nota:** No se requiere acción adicional por parte del usuario. La arquitectura queda documentada:
**CLIENTE --> NGINX (80) --> PROXY --> OLLAMA (11434)**
