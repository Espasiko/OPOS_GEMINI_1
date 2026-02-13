# 💾 EXPLICACIÓN: Modelo "EN MEMORIA" - VPS

**Contexto:** Output Ollama VPS mostró:
```
NAME: salamandra-opos:latest
SIZE: 4.8 GB
PROCESSOR: 100% CPU
CONTEXT: 4096
UNTIL: 4 minutes from now
```

---

## ¿QUÉ SIGNIFICA "EN MEMORIA"?

### Memoria = RAM del VPS

**VPS Hostinger:**
```
RAM Total: 7.8 GB
RAM Usada: ~5.5 GB  
RAM Libre: ~2.3 GB

Desglose:
- Modelo Salamandra: 4.8 GB  ← "EN MEMORIA"
- Sistema operativo (Ubuntu): ~0.6 GB
- Serv icios (Nginx, Ollama daemon): ~0.1 GB
- Cache/buffers: ~1.9 GB
```

**"EN MEMORIA" significa:**  
El modelo GGUF (4.8GB) está **cargado en RAM** del VPS, NO en disco.

---

## Jerarquía de Memoria

```
┌─────────────────────────────────────┐
│  CPU (AMD EPYC 2 cores)             │
│  Cache L1/L2/L3 (muy rápido)        │
└────────────┬────────────────────────┘
             │
    ┌────────▼────────┐
    │   RAM: 7.8 GB   │ ← Modelo Salamandra AQUÍ (4.8 GB)
    │   Velocidad:    │   
    │   ~10 GB/s      │   RÁPIDO ✅
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │  Swap: 2 GB     │ ← 1GB USADO (MALO ⚠️)
    │  (archivo disco)│
    │  Velocidad:     │
    │  ~500 MB/s      │   LENTO ❌ (20x más lento)
    └─────────────────┘
```

### Por qué Swap es Malo

```bash
# Si modelo en SWAP:
Lectura 1 token: 20ms (en RAM) → 400ms (en SWAP)
Generación 100 tokens: 2s → 40s ⚠️
```

**Buena noticia:** Modelo Salamandra SÍ cabe en RAM (4.8GB de 7.8GB total)

---

## ¿Qué Significa "100% CPU"?

**NO significa "sobrecargado".**  

Significa: Ollama usa **ambos cores** del CPU para inferencia:

```
Core 0: ████████████ 100% (procesando matriz A)
Core 1: ████████████ 100% (procesando matriz B)
```

**Es NORMAL y DESEABLE** durante generación de tokens.

**Problema:** Con 2 cores, generación es lenta (3-5min/pregunta).  
**Solución:** Más cores = más rápido (pero cuesta €€€).

---

## "UNTIL: 4 minutes from now"

**Qué significa:**  
Ollama **descargará** el modelo de RAM tras 4 minutos de inactividad.

**Consecuencia:**
```
Request 1 (modelo en RAM): Fast (ya cargado)
  ↓ 5 min sin uso
Modelo DESCARGADO de RAM ❌
  ↓ 
Request 2 (modelo NO en RAM): Slow (recarga 20-30s + inferencia)
```

### Solución: OLLAMA_KEEP_ALIVE

```bash
# VPS - systemd override
echo "[Service]" | sudo tee -a /etc/systemd/system/ollama.service.d/override.conf
echo "Environment=\"OLLAMA_KEEP_ALIVE=-1\"" | sudo tee -a /etc/systemd/system/ollama.service.d/override.conf

# Restart
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

**Resultado:**  
```
UNTIL: Never ✅ (modelo SIEMPRE en RAM)
```

---

## Diagrama Flujo Request

### ACTUAL (sin KEEP_ALIVE)

```
┌───────────────┐
│ Request llega │
└───────┬───────┘
        │
    ┌───▼────────┐
    │ ¿Modelo    │ NO → Cargar modelo (20-30s) → Inferencia (180s)
    │ en RAM?    │
    └───┬────────┘
        │ SÍ
        │
    ┌───▼─────────┐
    │ Inferencia  │ (180s)
    └───────┬─────┘
            │
    ┌───────▼────────┐
    │ Timer 4 min     │
    │ Sin requests?   │ NO → Mantener
    └───────┬─────────┘
            │ SÍ
            ▼
       DESCARGAR ❌
```

### OPTIMIZADO (con KEEP_ALIVE=-1)

```
┌──────────────┐
│ Boot VPS     │
└──────┬───────┘
       │
   ┌───▼────────┐
   │ Cargar     │ (1 vez, 20s)
   │ Salamandra │
   └───┬────────┘
       │
 ┌─────▼─────────┐
 │ Modelo SIEMPRE│
 │ EN RAM ✅      │
 └─────┬─────────┘
       │
       └──► Requests instantá neos (NO reload)
```

---

## Estado Optimizaciones VPS

| Optimización | Estado | Impacto |
|:---|:---:|:---|
| num_ctx 4096→2048 | ⏸️ PAUSADO | Usuario decidió mantener 4096 |
| OLLAMA_KEEP_ALIVE | ❌ PENDIENTE | +50% velocidad requests subsiguientes |
| Eliminar FastAPI wrapper | ⏸️ FUTURO | +10-15% velocidad |
| Upgrade VPS RAM | ❌ RECHAZADO | No hay presupuesto |

---

## Conclusión

**"EN MEMORIA" = Modelo Salamandra cargado en VPS RAM (4.8GB de 7.8GB)**

**Bueno:**  
✅ Modelo SÍ cabe en RAM  
✅ NO usa swap (principalmente)  
✅ Inferencia funcional

**Mejorable:**  
⚠️ OLLAMA_KEEP_ALIVE NO configurado → recarga tras 4min  
⚠️ Solo 2 cores CPU → inferencia lenta (3-5min)  
⚠️ 1GB swap usado → indica pressure RAM ocasional  

**NEXT:** Configurar OLLAMA_KEEP_ALIVE para mantener modelo permanente en RAM.

**FIN EXPLICACIÓN**
