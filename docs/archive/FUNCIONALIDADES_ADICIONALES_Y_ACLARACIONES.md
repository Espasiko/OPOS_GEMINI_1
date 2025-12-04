# 🚀 FUNCIONALIDADES ADICIONALES Y ACLARACIONES

**Fecha:** 26 Noviembre 2025  
**Objetivo:** Documentar nuevas funcionalidades y resolver dudas técnicas

---

## 📋 ÍNDICE

1. [Mapas Mentales con Excalidraw](#1-mapas-mentales-con-excalidraw)
2. [Integración con Anki (Tarjetas)](#2-integración-con-anki)
3. [Generador de Memes](#3-generador-de-memes)
4. [Temas del Temario Oficial](#4-temas-del-temario-oficial)
5. [Dashboard de Configuración](#5-dashboard-de-configuración)
6. [Mensajes Motivacionales](#6-mensajes-motivacionales)
7. [Google Drive OAuth2 Simplificado](#7-google-drive-oauth2)
8. [Almacenamiento Alternativo](#8-almacenamiento-alternativo)
9. [Migración Frontend](#9-migración-frontend)
10. [Limpieza de Código](#10-limpieza-de-código)
11. [Herramientas Seguridad - Aclaraciones](#11-herramientas-seguridad)
12. [Resumen Decisiones Finales](#12-resumen-decisiones-finales)

---

## 1. MAPAS MENTALES CON EXCALIDRAW

### 🎨 ¿Qué es Excalidraw?

**Excalidraw** es una librería open source para crear diagramas y dibujos con estilo "dibujado a mano".

**Características:**
- ✅ Open source y gratis
- ✅ Estilo visual atractivo (hand-drawn)
- ✅ Colaboración en tiempo real
- ✅ Export a PNG, SVG, JSON
- ✅ React component disponible

### 🔧 Implementación

#### Instalar librería

```bash
npm install @excalidraw/excalidraw
```

#### Componente MindMapView mejorado

```typescript
// components/MindMapView.tsx
import { Excalidraw } from '@excalidraw/excalidraw';
import { useState } from 'react';

const MindMapView = () => {
  const [excalidrawAPI, setExcalidrawAPI] = useState(null);
  
  const handleSave = async () => {
    if (!excalidrawAPI) return;
    
    // Obtener elementos del canvas
    const elements = excalidrawAPI.getSceneElements();
    const appState = excalidrawAPI.getAppState();
    
    // Guardar en BD
    await fetch('/api/mind-maps', {
      method: 'POST',
      body: JSON.stringify({
        elements,
        appState,
        tema_id: currentTema
      })
    });
  };
  
  const handleLoad = async (mapId: string) => {
    const response = await fetch(`/api/mind-maps/${mapId}`);
    const data = await response.json();
    
    // Cargar en Excalidraw
    excalidrawAPI.updateScene({
      elements: data.elements,
      appState: data.appState
    });
  };
  
  return (
    <div className="mind-map-container">
      <div className="toolbar">
        <button onClick={handleSave}>💾 Guardar</button>
        <button onClick={() => handleLoad(selectedMapId)}>📂 Cargar</button>
        <button onClick={() => excalidrawAPI.resetScene()}>🗑️ Limpiar</button>
      </div>
      
      <Excalidraw
        excalidrawAPI={(api) => setExcalidrawAPI(api)}
        initialData={{
          elements: [],
          appState: { viewBackgroundColor: "#ffffff" }
        }}
        UIOptions={{
          canvasActions: {
            loadScene: false,
            export: { saveFileToDisk: true }
          }
        }}
      />
    </div>
  );
};
```

#### Backend para guardar mapas

```python
# backend/routers/mind_maps.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter(prefix="/mind-maps", tags=["mind-maps"])

class MindMapCreate(BaseModel):
    tema_id: int
    tema_nombre: str
    titulo: str
    elements: List[Dict[str, Any]]  # Elementos de Excalidraw
    appState: Dict[str, Any]  # Estado de Excalidraw

@router.post("/")
async def create_mind_map(user_id: str, mind_map: MindMapCreate):
    """Guardar mapa mental"""
    with db.get_cursor() as cursor:
        cursor.execute("""
            INSERT INTO mind_maps (
                user_id, tema_id, tema_nombre, titulo, contenido
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (
            user_id,
            mind_map.tema_id,
            mind_map.tema_nombre,
            mind_map.titulo,
            json.dumps({
                'elements': mind_map.elements,
                'appState': mind_map.appState
            })
        ))
        
        map_id = cursor.fetchone()[0]
        return {"id": str(map_id), "status": "created"}

@router.get("/{map_id}")
async def get_mind_map(map_id: str):
    """Obtener mapa mental"""
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT contenido, tema_nombre, titulo
            FROM mind_maps
            WHERE id = %s
        """, (map_id,))
        
        result = cursor.fetchone()
        if not result:
            raise HTTPException(404, "Mapa no encontrado")
        
        return {
            "elements": result[0]['elements'],
            "appState": result[0]['appState'],
            "tema_nombre": result[1],
            "titulo": result[2]
        }
```

### ⏱️ Estimación: 4 horas

---

## 2. INTEGRACIÓN CON ANKI

### 📚 ¿Qué es Anki?

**Anki** es el sistema de repetición espaciada más popular. Tiene formato `.apkg` para mazos de tarjetas.

### 🔧 Implementación

#### Opción A: Export a formato Anki (.apkg)

```python
# backend/services/anki_export.py
import genanki
import random

class AnkiExporter:
    def __init__(self):
        # Crear modelo de tarjeta
        self.model = genanki.Model(
            random.randrange(1 << 30, 1 << 31),
            'OpositaIA - Seguridad Social',
            fields=[
                {'name': 'Pregunta'},
                {'name': 'Respuesta'},
                {'name': 'Tema'},
                {'name': 'Referencia'}
            ],
            templates=[{
                'name': 'Tarjeta 1',
                'qfmt': '''
                    <div class="pregunta">{{Pregunta}}</div>
                    <div class="tema">Tema: {{Tema}}</div>
                ''',
                'afmt': '''
                    {{FrontSide}}
                    <hr>
                    <div class="respuesta">{{Respuesta}}</div>
                    <div class="referencia">{{Referencia}}</div>
                '''
            }],
            css='''
                .pregunta { font-size: 20px; font-weight: bold; }
                .respuesta { font-size: 18px; color: #2c3e50; }
                .tema { font-size: 14px; color: #7f8c8d; }
                .referencia { font-size: 12px; color: #95a5a6; margin-top: 10px; }
            '''
        )
    
    def create_deck_from_flashcards(self, flashcards: List[dict], deck_name: str):
        """
        Crear mazo Anki desde flashcards
        """
        # Crear mazo
        deck = genanki.Deck(
            random.randrange(1 << 30, 1 << 31),
            deck_name
        )
        
        # Añadir tarjetas
        for card in flashcards:
            note = genanki.Note(
                model=self.model,
                fields=[
                    card['pregunta'],
                    card['respuesta'],
                    card['tema'],
                    card.get('referencia', '')
                ]
            )
            deck.add_note(note)
        
        # Generar archivo .apkg
        package = genanki.Package(deck)
        output_path = f"/tmp/{deck_name}.apkg"
        package.write_to_file(output_path)
        
        return output_path

# backend/routers/flashcards.py
@router.get("/export/anki")
async def export_to_anki(user_id: str, tema_id: int = None):
    """
    Exportar flashcards a formato Anki
    """
    # Obtener flashcards del usuario
    with db.get_cursor() as cursor:
        query = """
            SELECT pregunta, respuesta, tema_nombre, referencia_boe
            FROM flashcards
            WHERE user_id = %s
        """
        params = [user_id]
        
        if tema_id:
            query += " AND tema_id = %s"
            params.append(tema_id)
        
        cursor.execute(query, params)
        flashcards = cursor.fetchall()
    
    # Convertir a formato dict
    cards = [
        {
            'pregunta': f[0],
            'respuesta': f[1],
            'tema': f[2],
            'referencia': f[3]
        }
        for f in flashcards
    ]
    
    # Crear mazo Anki
    exporter = AnkiExporter()
    deck_name = f"OpositaIA - Tema {tema_id}" if tema_id else "OpositaIA - Todos los temas"
    apkg_path = exporter.create_deck_from_flashcards(cards, deck_name)
    
    # Devolver archivo
    return FileResponse(
        apkg_path,
        media_type='application/octet-stream',
        filename=f"{deck_name}.apkg"
    )
```

#### Frontend: Botón de export

```typescript
// components/FlashcardsView.tsx
const FlashcardsView = () => {
  const handleExportAnki = async () => {
    const response = await fetch(`/api/flashcards/export/anki?user_id=${userId}&tema_id=${temaId}`);
    const blob = await response.blob();
    
    // Descargar archivo
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `OpositaIA-Tema-${temaId}.apkg`;
    a.click();
  };
  
  return (
    <div>
      <button onClick={handleExportAnki}>
        📥 Exportar a Anki
      </button>
      {/* ... resto del componente ... */}
    </div>
  );
};
```

#### Opción B: AnkiConnect (Sincronización directa)

**AnkiConnect** es un plugin de Anki que permite control remoto vía API.

```python
# backend/services/anki_connect.py
import requests

class AnkiConnect:
    def __init__(self, url="http://localhost:8765"):
        self.url = url
    
    def invoke(self, action, **params):
        """Llamar a AnkiConnect API"""
        response = requests.post(self.url, json={
            'action': action,
            'version': 6,
            'params': params
        })
        return response.json()
    
    def add_note(self, deck_name, front, back, tags=[]):
        """Añadir nota a Anki"""
        return self.invoke('addNote', note={
            'deckName': deck_name,
            'modelName': 'Basic',
            'fields': {
                'Front': front,
                'Back': back
            },
            'tags': tags
        })
    
    def sync_flashcards(self, flashcards, deck_name="OpositaIA"):
        """Sincronizar flashcards con Anki"""
        results = []
        for card in flashcards:
            result = self.add_note(
                deck_name=deck_name,
                front=card['pregunta'],
                back=card['respuesta'],
                tags=[card['tema'], 'opositaia']
            )
            results.append(result)
        return results
```

### 🎯 RECOMENDACIÓN

**Para MVP:** Opción A (Export .apkg) - Más simple, no requiere Anki instalado  
**Para Producción:** Opción B (AnkiConnect) - Sincronización automática

### ⏱️ Estimación: 3 horas (Opción A) o 6 horas (Opción B)

---

## 3. GENERADOR DE MEMES

### 😂 ¿Por qué falta?

¡Buena pregunta! Los memes son excelentes para:
- Hacer el estudio más divertido
- Memorizar conceptos complejos
- Compartir en redes sociales (marketing viral)

### 🔧 Implementación

```python
# backend/routers/memes.py
from fastapi import APIRouter
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

router = APIRouter(prefix="/memes", tags=["memes"])

class MemeGenerator:
    def __init__(self):
        # Templates populares
        self.templates = {
            'drake': 'https://i.imgflip.com/30b1gx.jpg',
            'distracted_boyfriend': 'https://i.imgflip.com/1ur9b0.jpg',
            'two_buttons': 'https://i.imgflip.com/1g8my4.jpg',
            'change_my_mind': 'https://i.imgflip.com/24y43o.jpg'
        }
    
    def create_meme(self, template: str, top_text: str, bottom_text: str = ""):
        """
        Crear meme con texto
        """
        # Descargar template
        response = requests.get(self.templates[template])
        img = Image.open(BytesIO(response.content))
        
        # Preparar para dibujar
        draw = ImageDraw.Draw(img)
        
        # Font (necesitas tener Impact.ttf)
        try:
            font = ImageFont.truetype("Impact.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        # Calcular posición del texto
        width, height = img.size
        
        # Texto superior
        bbox = draw.textbbox((0, 0), top_text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) / 2
        y = 10
        
        # Dibujar con borde negro
        for adj in range(-2, 3):
            for adj2 in range(-2, 3):
                draw.text((x+adj, y+adj2), top_text, font=font, fill="black")
        draw.text((x, y), top_text, font=font, fill="white")
        
        # Texto inferior (si existe)
        if bottom_text:
            bbox = draw.textbbox((0, 0), bottom_text, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) / 2
            y = height - 60
            
            for adj in range(-2, 3):
                for adj2 in range(-2, 3):
                    draw.text((x+adj, y+adj2), bottom_text, font=font, fill="black")
            draw.text((x, y), bottom_text, font=font, fill="white")
        
        # Guardar
        output = BytesIO()
        img.save(output, format='JPEG')
        output.seek(0)
        
        return output

@router.post("/generate")
async def generate_meme(
    template: str,
    concepto: str,
    user_id: str
):
    """
    Generar meme educativo con IA
    """
    # Usar IA para generar texto del meme
    prompt = f"""
    Crea un meme educativo sobre: {concepto}
    
    Template: {template}
    
    Genera:
    - Texto superior (máximo 50 caracteres)
    - Texto inferior (máximo 50 caracteres)
    
    El meme debe ser gracioso pero educativo, relacionado con oposiciones de Seguridad Social.
    
    Formato JSON:
    {{
        "top_text": "...",
        "bottom_text": "..."
    }}
    """
    
    # Llamar a Gemini
    response = await gemini_api.generate(prompt)
    meme_data = json.loads(response)
    
    # Generar meme
    generator = MemeGenerator()
    meme_image = generator.create_meme(
        template=template,
        top_text=meme_data['top_text'],
        bottom_text=meme_data['bottom_text']
    )
    
    # Guardar en BD (opcional)
    # ...
    
    return StreamingResponse(meme_image, media_type="image/jpeg")
```

#### Frontend

```typescript
// components/MemeGeneratorView.tsx
const MemeGeneratorView = () => {
  const [template, setTemplate] = useState('drake');
  const [concepto, setConcepto] = useState('');
  const [memeUrl, setMemeUrl] = useState('');
  
  const handleGenerate = async () => {
    const response = await fetch('/api/memes/generate', {
      method: 'POST',
      body: JSON.stringify({ template, concepto, user_id: userId })
    });
    
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    setMemeUrl(url);
  };
  
  return (
    <div className="meme-generator">
      <h2>🎭 Generador de Memes Educativos</h2>
      
      <select value={template} onChange={(e) => setTemplate(e.target.value)}>
        <option value="drake">Drake</option>
        <option value="distracted_boyfriend">Novio Distraído</option>
        <option value="two_buttons">Dos Botones</option>
        <option value="change_my_mind">Change My Mind</option>
      </select>
      
      <input
        type="text"
        placeholder="Concepto (ej: Incapacidad Temporal)"
        value={concepto}
        onChange={(e) => setConcepto(e.target.value)}
      />
      
      <button onClick={handleGenerate}>🎨 Generar Meme</button>
      
      {memeUrl && (
        <div className="meme-result">
          <img src={memeUrl} alt="Meme generado" />
          <button onClick={() => {
            const a = document.createElement('a');
            a.href = memeUrl;
            a.download = `meme-${concepto}.jpg`;
            a.click();
          }}>
            📥 Descargar
          </button>
          <button onClick={() => {
            // Compartir en redes sociales
            navigator.share({
              title: `Meme: ${concepto}`,
              text: 'Estudiando oposiciones con OpositaIA',
              url: memeUrl
            });
          }}>
            📤 Compartir
          </button>
        </div>
      )}
    </div>
  );
};
```

### ⏱️ Estimación: 4 horas

---

## 4. TEMAS DEL TEMARIO OFICIAL

### 📚 Problema Actual

Los tests tienen temas limitados. Necesitamos:
1. Todos los temas del temario oficial
2. Opción de añadir temas de academias

### 🔧 Solución

#### Base de datos de temas

```sql
-- backend/database/schema.sql

CREATE TABLE IF NOT EXISTS temarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(255) NOT NULL,  -- "Administrativo C1", "Gestión A2", etc.
    tipo VARCHAR(50) NOT NULL,  -- "oficial", "academia"
    academia VARCHAR(255),  -- Nombre de la academia (si aplica)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS temas (
    id SERIAL PRIMARY KEY,
    temario_id UUID REFERENCES temarios(id),
    numero INTEGER NOT NULL,  -- Número del tema (1, 2, 3...)
    titulo TEXT NOT NULL,
    descripcion TEXT,
    bloques TEXT[],  -- Subapartados del tema
    es_oficial BOOLEAN DEFAULT TRUE,
    created_by UUID REFERENCES user_progress(user_id),  -- Usuario que lo creó
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_temas_temario_id ON temas(temario_id);
CREATE INDEX idx_temas_numero ON temas(numero);
CREATE INDEX idx_temas_es_oficial ON temas(es_oficial);
```

#### Seed data: Temario oficial

```python
# backend/database/seed_temarios.py

TEMARIOS_OFICIALES = {
    'administrativo_c1': {
        'nombre': 'Cuerpo Administrativo (C1)',
        'temas': [
            {
                'numero': 1,
                'titulo': 'La Constitución Española de 1978',
                'bloques': [
                    'Estructura',
                    'Principios generales',
                    'Derechos y deberes fundamentales'
                ]
            },
            {
                'numero': 2,
                'titulo': 'La organización territorial del Estado',
                'bloques': [
                    'Comunidades Autónomas',
                    'Provincias',
                    'Municipios'
                ]
            },
            # ... hasta tema 36
        ]
    },
    'gestion_a2': {
        'nombre': 'Cuerpo de Gestión (A2)',
        'temas': [
            # ... 79 temas
        ]
    }
}

def seed_temarios():
    """Insertar temarios oficiales en BD"""
    for key, data in TEMARIOS_OFICIALES.items():
        # Crear temario
        temario_id = db.execute("""
            INSERT INTO temarios (nombre, tipo)
            VALUES (%s, 'oficial')
            RETURNING id
        """, (data['nombre'],))
        
        # Insertar temas
        for tema in data['temas']:
            db.execute("""
                INSERT INTO temas (
                    temario_id, numero, titulo, bloques, es_oficial
                )
                VALUES (%s, %s, %s, %s, TRUE)
            """, (
                temario_id,
                tema['numero'],
                tema['titulo'],
                tema['bloques']
            ))
```

#### API para gestionar temas

```python
# backend/routers/temarios.py

@router.get("/temarios")
async def list_temarios():
    """Listar todos los temarios disponibles"""
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT id, nombre, tipo, academia
            FROM temarios
            ORDER BY tipo DESC, nombre
        """)
        return cursor.fetchall()

@router.get("/temarios/{temario_id}/temas")
async def list_temas(temario_id: str):
    """Listar temas de un temario"""
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT numero, titulo, descripcion, bloques
            FROM temas
            WHERE temario_id = %s
            ORDER BY numero
        """, (temario_id,))
        return cursor.fetchall()

@router.post("/temarios/custom")
async def create_custom_temario(
    user_id: str,
    nombre: str,
    academia: str,
    temas: List[dict]
):
    """
    Crear temario personalizado (de academia)
    """
    with db.get_cursor() as cursor:
        # Crear temario
        cursor.execute("""
            INSERT INTO temarios (nombre, tipo, academia)
            VALUES (%s, 'academia', %s)
            RETURNING id
        """, (nombre, academia))
        
        temario_id = cursor.fetchone()[0]
        
        # Insertar temas
        for tema in temas:
            cursor.execute("""
                INSERT INTO temas (
                    temario_id, numero, titulo, descripcion,
                    bloques, es_oficial, created_by
                )
                VALUES (%s, %s, %s, %s, %s, FALSE, %s)
            """, (
                temario_id,
                tema['numero'],
                tema['titulo'],
                tema.get('descripcion', ''),
                tema.get('bloques', []),
                user_id
            ))
        
        return {"temario_id": str(temario_id), "status": "created"}
```

#### Frontend: Selector de temario

```typescript
// components/TemarioSelector.tsx
const TemarioSelector = () => {
  const [temarios, setTemarios] = useState([]);
  const [selectedTemario, setSelectedTemario] = useState(null);
  const [temas, setTemas] = useState([]);
  
  useEffect(() => {
    // Cargar temarios
    fetch('/api/temarios')
      .then(r => r.json())
      .then(setTemarios);
  }, []);
  
  useEffect(() => {
    if (selectedTemario) {
      // Cargar temas del temario seleccionado
      fetch(`/api/temarios/${selectedTemario}/temas`)
        .then(r => r.json())
        .then(setTemas);
    }
  }, [selectedTemario]);
  
  return (
    <div className="temario-selector">
      <h3>Selecciona tu temario</h3>
      
      <select onChange={(e) => setSelectedTemario(e.target.value)}>
        <option value="">-- Selecciona --</option>
        {temarios.map(t => (
          <option key={t.id} value={t.id}>
            {t.nombre} {t.tipo === 'academia' && `(${t.academia})`}
          </option>
        ))}
      </select>
      
      {temas.length > 0 && (
        <div className="temas-list">
          <h4>Temas disponibles ({temas.length})</h4>
          <ul>
            {temas.map(tema => (
              <li key={tema.numero}>
                <strong>Tema {tema.numero}:</strong> {tema.titulo}
                {tema.bloques && (
                  <ul className="bloques">
                    {tema.bloques.map((bloque, i) => (
                      <li key={i}>{bloque}</li>
                    ))}
                  </ul>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
      
      <button onClick={() => {
        // Abrir modal para añadir temario personalizado
        setShowCustomModal(true);
      }}>
        ➕ Añadir temario de mi academia
      </button>
    </div>
  );
};
```

### ⏱️ Estimación: 6 horas

---


## 5. DASHBOARD DE CONFIGURACIÓN

### 🎛️ Problema Actual

La página de configuración está vacía. Necesitamos un dashboard completo donde el usuario pueda:
1. Ajustar nivel de dificultad
2. Configurar fecha límite de leyes
3. Seleccionar modalidad y convocatoria
4. Ver diagrama de progreso
5. Configurar preferencias

### 🔧 Implementación

```typescript
// components/SettingsView.tsx
import { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';

const SettingsView = () => {
  const [settings, setSettings] = useState({
    nivel: 'intermedio',
    fecha_limite_leyes: '2024-12-31',
    modalidad: 'administrativo_c1',
    convocatoria: '2025',
    modo_adaptativo: true,
    notificaciones: true
  });
  
  const [progreso, setProgreso] = useState(null);
  
  useEffect(() => {
    // Cargar configuración actual
    fetch(`/api/user/${userId}/settings`)
      .then(r => r.json())
      .then(setSettings);
    
    // Cargar progreso
    fetch(`/api/user/${userId}/progress`)
      .then(r => r.json())
      .then(setProgreso);
  }, []);
  
  const handleSave = async () => {
    await fetch(`/api/user/${userId}/settings`, {
      method: 'PUT',
      body: JSON.stringify(settings)
    });
    
    toast.success('Configuración guardada');
  };
  
  return (
    <div className="settings-dashboard">
      <h1>⚙️ Configuración</h1>
      
      {/* Sección 1: Perfil de Estudio */}
      <section className="settings-section">
        <h2>👤 Perfil de Estudio</h2>
        
        <div className="form-group">
          <label>Modalidad de Oposición</label>
          <select 
            value={settings.modalidad}
            onChange={(e) => setSettings({...settings, modalidad: e.target.value})}
          >
            <option value="administrativo_c1">Administrativo (C1)</option>
            <option value="gestion_a2_libre">Gestión (A2) - Acceso Libre</option>
            <option value="gestion_a2_interna">Gestión (A2) - Promoción Interna</option>
            <option value="letrados_a1">Letrados (A1)</option>
          </select>
        </div>
        
        <div className="form-group">
          <label>Convocatoria</label>
          <input 
            type="text"
            value={settings.convocatoria}
            onChange={(e) => setSettings({...settings, convocatoria: e.target.value})}
            placeholder="2025"
          />
        </div>
        
        <div className="form-group">
          <label>Fecha límite de legislación</label>
          <input 
            type="date"
            value={settings.fecha_limite_leyes}
            onChange={(e) => setSettings({...settings, fecha_limite_leyes: e.target.value})}
          />
          <p className="help-text">
            ℹ️ Solo se considerarán leyes y cambios hasta esta fecha en exámenes y búsquedas
          </p>
        </div>
      </section>
      
      {/* Sección 2: Nivel y Dificultad */}
      <section className="settings-section">
        <h2>📊 Nivel y Dificultad</h2>
        
        <div className="form-group">
          <label>Nivel actual</label>
          <div className="nivel-selector">
            <button 
              className={settings.nivel === 'inicial' ? 'active' : ''}
              onClick={() => setSettings({...settings, nivel: 'inicial'})}
            >
              🌱 Inicial
            </button>
            <button 
              className={settings.nivel === 'intermedio' ? 'active' : ''}
              onClick={() => setSettings({...settings, nivel: 'intermedio'})}
            >
              🌿 Intermedio
            </button>
            <button 
              className={settings.nivel === 'avanzado' ? 'active' : ''}
              onClick={() => setSettings({...settings, nivel: 'avanzado'})}
            >
              🌳 Avanzado
            </button>
          </div>
        </div>
        
        <div className="form-group">
          <label>
            <input 
              type="checkbox"
              checked={settings.modo_adaptativo}
              onChange={(e) => setSettings({...settings, modo_adaptativo: e.target.checked})}
            />
            Modo adaptativo (ajusta dificultad según tu progreso)
          </label>
          <p className="help-text">
            💡 Recomendado: El sistema ajustará automáticamente la dificultad basándose en tus últimos 3-4 simulacros
          </p>
        </div>
      </section>
      
      {/* Sección 3: Progreso */}
      <section className="settings-section">
        <h2>📈 Tu Progreso</h2>
        
        {progreso && (
          <div className="progreso-dashboard">
            <div className="stats-grid">
              <div className="stat-card">
                <h3>Preguntas Respondidas</h3>
                <p className="stat-value">{progreso.total_preguntas}</p>
              </div>
              
              <div className="stat-card">
                <h3>Precisión Global</h3>
                <p className="stat-value">{progreso.precision_global}%</p>
              </div>
              
              <div className="stat-card">
                <h3>Simulacros Completados</h3>
                <p className="stat-value">{progreso.simulacros_completed}</p>
              </div>
              
              <div className="stat-card">
                <h3>Probabilidad de Aprobar</h3>
                <p className="stat-value probability">
                  {progreso.probability_pass ? `${progreso.probability_pass}%` : 'N/A'}
                </p>
                {progreso.probability_pass && (
                  <p className="stat-subtitle">
                    {progreso.probability_pass > 70 ? '🎉 ¡Excelente!' :
                     progreso.probability_pass > 40 ? '💪 Vas bien' :
                     '📚 Sigue estudiando'}
                  </p>
                )}
              </div>
            </div>
            
            {/* Gráfico de evolución */}
            <div className="chart-container">
              <h3>Evolución de Precisión</h3>
              <Line 
                data={{
                  labels: progreso.evolution.map(e => e.date),
                  datasets: [{
                    label: 'Precisión (%)',
                    data: progreso.evolution.map(e => e.accuracy),
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    tension: 0.4
                  }]
                }}
                options={{
                  responsive: true,
                  scales: {
                    y: {
                      beginAtZero: true,
                      max: 100
                    }
                  }
                }}
              />
            </div>
            
            {/* Temas débiles */}
            {progreso.temas_debiles && progreso.temas_debiles.length > 0 && (
              <div className="temas-debiles">
                <h3>⚠️ Temas que necesitan refuerzo</h3>
                <ul>
                  {progreso.temas_debiles.map(tema => (
                    <li key={tema.id}>
                      <span className="tema-nombre">{tema.nombre}</span>
                      <span className="tema-precision">{tema.precision}%</span>
                      <button onClick={() => navigate(`/practice?tema=${tema.id}`)}>
                        Practicar
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </section>
      
      {/* Sección 4: Notificaciones */}
      <section className="settings-section">
        <h2>🔔 Notificaciones</h2>
        
        <div className="form-group">
          <label>
            <input 
              type="checkbox"
              checked={settings.notificaciones}
              onChange={(e) => setSettings({...settings, notificaciones: e.target.checked})}
            />
            Recibir recordatorios de estudio
          </label>
        </div>
      </section>
      
      {/* Botón guardar */}
      <div className="settings-actions">
        <button className="btn-primary" onClick={handleSave}>
          💾 Guardar Configuración
        </button>
      </div>
    </div>
  );
};
```

#### Backend

```python
# backend/routers/user.py

@router.get("/{user_id}/settings")
async def get_user_settings(user_id: str):
    """Obtener configuración del usuario"""
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT settings
            FROM user_progress
            WHERE user_id = %s
        """, (user_id,))
        
        result = cursor.fetchone()
        if not result or not result[0]:
            # Configuración por defecto
            return {
                'nivel': 'intermedio',
                'fecha_limite_leyes': '2024-12-31',
                'modalidad': 'administrativo_c1',
                'convocatoria': '2025',
                'modo_adaptativo': True,
                'notificaciones': True
            }
        
        return result[0]

@router.put("/{user_id}/settings")
async def update_user_settings(user_id: str, settings: dict):
    """Actualizar configuración del usuario"""
    with db.get_cursor() as cursor:
        cursor.execute("""
            UPDATE user_progress
            SET settings = %s::jsonb,
                updated_at = NOW()
            WHERE user_id = %s
        """, (json.dumps(settings), user_id))
        
        return {"status": "updated"}

@router.get("/{user_id}/progress/evolution")
async def get_progress_evolution(user_id: str, days: int = 30):
    """Obtener evolución del progreso"""
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT 
                DATE(created_at) as date,
                AVG(CASE WHEN es_correcta THEN 100 ELSE 0 END) as accuracy
            FROM answer_history
            WHERE user_id = %s
              AND created_at >= NOW() - INTERVAL '%s days'
            GROUP BY DATE(created_at)
            ORDER BY date
        """, (user_id, days))
        
        results = cursor.fetchall()
        return [
            {'date': r[0].isoformat(), 'accuracy': round(r[1], 2)}
            for r in results
        ]
```

### ⏱️ Estimación: 8 horas

---

## 6. MENSAJES MOTIVACIONALES

### 💪 Implementación

```python
# backend/services/motivational_messages.py

class MotivationalMessages:
    MESSAGES = {
        'high_difficulty_warning': {
            'title': '⚠️ Nivel de Dificultad Alto',
            'message': '''
            Has seleccionado un simulacro de nivel difícil.
            
            💡 **Consejo:** Tirarse a lo más difícil muchas veces solo lleva a frustración.
            
            🛁 **Recomendación:** Date un "baño de éxito" de vez en cuando:
            - Baja el nivel de dificultad temporalmente
            - Completa algunos tests más fáciles
            - Recupera confianza y ánimo
            - Luego vuelve al nivel difícil
            
            ¿Quieres continuar con nivel difícil o prefieres ajustar?
            ''',
            'actions': [
                {'label': 'Continuar (Difícil)', 'value': 'continue'},
                {'label': 'Cambiar a Medio', 'value': 'medium'},
                {'label': 'Cambiar a Fácil', 'value': 'easy'}
            ]
        },
        'insufficient_data': {
            'title': '📊 Necesitas Más Datos',
            'message': '''
            Para calcular tu probabilidad de aprobar necesitamos al menos 3 simulacros completos.
            
            **Actualmente tienes:** {simulacros_count} simulacros
            **Te faltan:** {simulacros_needed} simulacros
            
            💪 ¡Ánimo! Cada simulacro te acerca más a tu objetivo.
            ''',
            'actions': [
                {'label': 'Hacer Simulacro Ahora', 'value': 'start_simulacro'}
            ]
        },
        'low_accuracy': {
            'title': '📚 Refuerza tus Conocimientos',
            'message': '''
            Tu precisión actual es {accuracy}%, por debajo del 60%.
            
            **No te desanimes, esto es normal al principio.**
            
            🎯 **Plan de acción:**
            1. Estudia los temas básicos (Constitución, LGSS Título I)
            2. Practica tests cortos (10-20 preguntas)
            3. Revisa tus errores frecuentes
            4. Cuando llegues a 60%, intenta simulacros
            
            💡 **Recuerda:** Todos los opositores empiezan aquí. ¡Tú puedes!
            ''',
            'actions': [
                {'label': 'Ver Temas Básicos', 'value': 'basic_topics'},
                {'label': 'Test Corto (10 preguntas)', 'value': 'short_test'}
            ]
        },
        'good_progress': {
            'title': '🎉 ¡Vas por Buen Camino!',
            'message': '''
            Tu precisión es {accuracy}%, estás en el rango intermedio (60-85%).
            
            **Probabilidad de aprobar:** {probability}%
            
            💪 **Sigue así:**
            - Enfócate en tus temas débiles
            - Realiza casos prácticos
            - Mantén la constancia
            
            ¡Estás cada vez más cerca de tu objetivo!
            ''',
            'actions': [
                {'label': 'Ver Temas Débiles', 'value': 'weak_topics'},
                {'label': 'Caso Práctico', 'value': 'practical_case'}
            ]
        },
        'excellent': {
            'title': '🏆 ¡Excelente Nivel!',
            'message': '''
            Tu precisión es {accuracy}%, ¡estás en nivel avanzado!
            
            **Probabilidad de aprobar:** {probability}% 🎯
            
            🌟 **Estás listo para:**
            - Simular condiciones de examen real
            - Practicar gestión del tiempo
            - Repasar jurisprudencia reciente
            
            ¡El examen oficial está a tu alcance!
            ''',
            'actions': [
                {'label': 'Simulacro Oficial', 'value': 'official_exam'},
                {'label': 'Jurisprudencia', 'value': 'jurisprudence'}
            ]
        }
    }
    
    @staticmethod
    def get_message(message_type: str, **kwargs):
        """Obtener mensaje motivacional con variables"""
        template = MotivationalMessages.MESSAGES.get(message_type)
        if not template:
            return None
        
        message = template['message'].format(**kwargs)
        
        return {
            'title': template['title'],
            'message': message,
            'actions': template['actions']
        }

# backend/routers/ai_functions.py

@router.post("/generate-mock-exam")
async def generate_mock_exam(
    user_id: str,
    difficulty: str = "media"
):
    """Generar simulacro con advertencia si es difícil"""
    
    # Obtener progreso del usuario
    progress = await get_user_progress(user_id)
    
    # Si intenta nivel difícil sin suficiente historial
    if difficulty == "difícil" and progress['simulacros_completed'] < 3:
        motivational = MotivationalMessages.get_message(
            'high_difficulty_warning'
        )
        return {
            'warning': True,
            'motivational': motivational,
            'can_continue': True
        }
    
    # Si tiene baja precisión
    if progress['accuracy'] < 60:
        motivational = MotivationalMessages.get_message(
            'low_accuracy',
            accuracy=progress['accuracy']
        )
        return {
            'warning': True,
            'motivational': motivational,
            'recommendation': 'Practica tests cortos antes de simulacros'
        }
    
    # Generar simulacro normalmente
    # ...
```

#### Frontend: Modal motivacional

```typescript
// components/MotivationalModal.tsx
const MotivationalModal = ({ message, onAction, onClose }) => {
  return (
    <div className="modal-overlay">
      <div className="motivational-modal">
        <h2>{message.title}</h2>
        <div className="message-content">
          {message.message.split('\n').map((line, i) => (
            <p key={i}>{line}</p>
          ))}
        </div>
        <div className="modal-actions">
          {message.actions.map(action => (
            <button 
              key={action.value}
              onClick={() => onAction(action.value)}
              className={action.value === 'continue' ? 'btn-warning' : 'btn-primary'}
            >
              {action.label}
            </button>
          ))}
          <button onClick={onClose} className="btn-secondary">
            Cancelar
          </button>
        </div>
      </div>
    </div>
  );
};
```

### ⏱️ Estimación: 2 horas

---

## 7. GOOGLE DRIVE OAUTH2 SIMPLIFICADO

### 🔐 ¿Es Complejo OAuth2?

**Respuesta:** NO, si usas librerías modernas. El flujo es:

1. Usuario hace clic "Conectar Google Drive"
2. Redirige a Google (página de Google, no tuya)
3. Usuario hace clic "Permitir"
4. Google redirige de vuelta con token
5. Guardas token encriptado
6. ¡Listo!

### 🔧 Implementación Simplificada

```python
# backend/routers/auth_google.py
from fastapi import APIRouter, HTTPException
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
import os

router = APIRouter(prefix="/auth/google", tags=["auth"])

# Configuración OAuth2
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
CLIENT_CONFIG = {
    "web": {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uris": [os.getenv("GOOGLE_REDIRECT_URI")],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token"
    }
}

@router.get("/authorize")
async def authorize_google_drive(user_id: str):
    """
    Paso 1: Redirigir a Google para autorización
    """
    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=CLIENT_CONFIG['web']['redirect_uris'][0]
    )
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        state=user_id  # Pasar user_id en state
    )
    
    return {"authorization_url": authorization_url}

@router.get("/callback")
async def google_drive_callback(code: str, state: str):
    """
    Paso 2: Google redirige aquí con el código
    """
    user_id = state  # Recuperar user_id
    
    # Intercambiar código por token
    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=CLIENT_CONFIG['web']['redirect_uris'][0]
    )
    
    flow.fetch_token(code=code)
    credentials = flow.credentials
    
    # Guardar token encriptado en BD
    from cryptography.fernet import Fernet
    cipher = Fernet(os.getenv("ENCRYPTION_KEY").encode())
    
    encrypted_token = cipher.encrypt(
        json.dumps({
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }).encode()
    )
    
    # Guardar en BD
    with db.get_cursor() as cursor:
        cursor.execute("""
            UPDATE user_progress
            SET google_drive_token = %s,
                updated_at = NOW()
            WHERE user_id = %s
        """, (encrypted_token.decode(), user_id))
    
    # Redirigir al frontend
    return RedirectResponse(url=f"{os.getenv('FRONTEND_URL')}/settings?google_drive=connected")
```

#### Frontend: Un solo botón

```typescript
// components/GoogleDriveConnect.tsx
const GoogleDriveConnect = () => {
  const [isConnected, setIsConnected] = useState(false);
  
  const handleConnect = async () => {
    // Obtener URL de autorización
    const response = await fetch(`/api/auth/google/authorize?user_id=${userId}`);
    const { authorization_url } = await response.json();
    
    // Redirigir a Google (el usuario solo hace clic "Permitir")
    window.location.href = authorization_url;
  };
  
  return (
    <div className="google-drive-connect">
      {!isConnected ? (
        <button onClick={handleConnect} className="btn-google">
          <img src="/google-drive-icon.svg" alt="Google Drive" />
          Conectar Google Drive
        </button>
      ) : (
        <div className="connected">
          ✅ Google Drive conectado
          <button onClick={handleDisconnect}>Desconectar</button>
        </div>
      )}
      
      <p className="help-text">
        ℹ️ Solo necesitas hacer clic en "Permitir" en la página de Google.
        Tus documentos NO se almacenan en nuestros servidores.
      </p>
    </div>
  );
};
```

### 📊 Límites API

**10,000 requests/día = 100 usuarios × 100 requests/día**

Esto es MÁS que suficiente porque:
- Listar documentos: 1 request
- Leer documento: 1 request por documento
- Usuario promedio: 5-10 requests/día

### ⏱️ Estimación: 4 horas (no 6, es más simple de lo que parece)

---

## 8. ALMACENAMIENTO ALTERNATIVO

### 🔍 Alternativas a Google Drive

#### Opción 1: Dropbox

**API:** Dropbox API  
**Free tier:** 2GB storage  
**OAuth2:** Similar a Google (simple)  
**Ventajas:** Muy usado, API simple  
**Desventajas:** Free tier pequeño

#### Opción 2: OneDrive (Microsoft)

**API:** Microsoft Graph API  
**Free tier:** 5GB storage  
**OAuth2:** Similar a Google  
**Ventajas:** Integrado con Office  
**Desventajas:** API más compleja

#### Opción 3: pCloud

**API:** pCloud API  
**Free tier:** 10GB storage  
**OAuth2:** Sí  
**Ventajas:** Más espacio gratis, enfocado en privacidad  
**Desventajas:** Menos conocido

### 🎯 RECOMENDACIÓN

**Para MVP:** Documentos temporales (Redis) + Opción "Pronto: Google Drive"  
**Para Producción:** Google Drive (más usado) + Dropbox (alternativa)

### 💾 Redis: ¿Necesitas Cuenta?

**NO necesitas cuenta.** Redis es un servidor que instalas en tu VPS:

```bash
# Instalar Redis en VPS
sudo apt-get install redis-server

# O con Docker
docker run -d -p 6379:6379 redis:7-alpine
```

Ya está en tu `docker-compose.yml` propuesto, así que lo tendrás automáticamente.

---


## 9. MIGRACIÓN FRONTEND

### 📁 Problema Actual

El frontend está en la raíz del proyecto. Mejor estructura:

```
opositaia/
├── frontend/          # Todo el código React
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
├── backend/           # Todo el código Python
│   ├── routers/
│   ├── agents/
│   └── main.py
└── docker-compose.yml
```

### 🔧 Migración

```bash
# 1. Crear carpeta frontend
mkdir frontend

# 2. Mover archivos React
mv src frontend/
mv public frontend/
mv index.html frontend/
mv package.json frontend/
mv package-lock.json frontend/
mv vite.config.ts frontend/
mv tsconfig.json frontend/
mv tsconfig.node.json frontend/
mv .eslintrc.cjs frontend/

# 3. Mover archivos de configuración específicos de frontend
mv tailwind.config.js frontend/
mv postcss.config.js frontend/

# 4. Actualizar .gitignore
echo "frontend/node_modules/" >> .gitignore
echo "frontend/dist/" >> .gitignore

# 5. Actualizar rutas en vite.config.ts
# (Ya no necesitas cambiar nada, Vite detecta automáticamente)

# 6. Borrar geminiService.tsx si existe
rm frontend/src/services/geminiService.tsx

# 7. Verificar que funciona
cd frontend
npm install
npm run dev
```

### 📝 Actualizar docker-compose.yml

```yaml
services:
  frontend:
    build: ./frontend  # Cambiar de . a ./frontend
    # ...resto igual
```

### ⏱️ Estimación: 1 hora

---

## 10. LIMPIEZA DE CÓDIGO

### 🗑️ Archivos a Revisar

```bash
# 1. Buscar archivos duplicados
find . -name "*.tsx" -o -name "*.ts" | sort | uniq -d

# 2. Buscar archivos no usados
# Instalar depcheck
npm install -g depcheck

cd frontend
depcheck

# 3. Buscar imports no usados
# Instalar eslint-plugin-unused-imports
npm install --save-dev eslint-plugin-unused-imports

# 4. Buscar código comentado
grep -r "// TODO" frontend/src
grep -r "// FIXME" frontend/src
grep -r "console.log" frontend/src

# 5. Buscar archivos de test sin implementar
find . -name "*.test.ts" -o -name "*.test.tsx" | xargs grep -l "test.todo"
```

### 📋 Checklist de Limpieza

```markdown
- [ ] Borrar geminiService.tsx (ya no se usa)
- [ ] Borrar archivos en carpeta `basura/` (son históricos)
- [ ] Revisar imports no usados en cada archivo
- [ ] Eliminar console.log() de producción
- [ ] Eliminar código comentado viejo
- [ ] Actualizar dependencias obsoletas
- [ ] Eliminar archivos de test vacíos
- [ ] Consolidar utilidades duplicadas
```

### 🔧 Script Automático

```bash
# cleanup.sh
#!/bin/bash

echo "🧹 Limpiando código..."

# 1. Eliminar node_modules y reinstalar
cd frontend
rm -rf node_modules
npm install

# 2. Ejecutar linter
npm run lint --fix

# 3. Formatear código
npm run format

# 4. Eliminar archivos temporales
find . -name "*.log" -delete
find . -name ".DS_Store" -delete
find . -name "Thumbs.db" -delete

# 5. Eliminar console.log (cuidado, revisar antes)
# find src -name "*.ts" -o -name "*.tsx" | xargs sed -i '/console\.log/d'

echo "✅ Limpieza completada"
```

### ⏱️ Estimación: 2 horas

---

## 11. HERRAMIENTAS SEGURIDAD - ACLARACIONES

### 🤔 Dudas Resueltas

#### ¿Qué es un PR (Pull Request)?

**PR = Pull Request** (en GitHub) o **Merge Request** (en GitLab)

**Flujo:**
1. Creas una rama: `git checkout -b feature/nueva-funcionalidad`
2. Haces cambios y commit: `git commit -m "Añadir nueva funcionalidad"`
3. Subes la rama: `git push origin feature/nueva-funcionalidad`
4. Abres un PR en GitHub: "Quiero mergear esta rama a main"
5. **Qodo revisa automáticamente** el código del PR
6. Apruebas y mergeas

**Ventaja de Qodo:** Revisa cada PR antes de mergear, detecta bugs temprano.

---

#### ¿Por qué "Vendor Lock-in" con Aikido?

**Vendor Lock-in** = Dependes de un proveedor y es difícil cambiar.

**Con Aikido:**
- Si dejas de pagar, pierdes acceso a la plataforma
- Tus configuraciones están en Aikido (no en tu repo)
- Difícil migrar a otra herramienta

**Con Semgrep (open source):**
- Reglas en tu repo (`.semgrep/`)
- Puedes cambiar a otra herramienta fácilmente
- No dependes de nadie

---

#### Semgrep: ¿Es Suficiente?

**Semgrep solo hace SAST** (análisis estático de código)

**NO hace:**
- SCA (análisis de dependencias) → Usa Snyk para esto
- DAST (análisis dinámico) → No necesario para MVP
- Secrets detection → Semgrep tiene reglas para esto

**Conclusión:** Semgrep + Snyk = Suficiente para MVP

---

#### SonarQube: ¿Vale la Pena?

**Para MVP:** NO, es overkill  
**Para Producción:** SÍ, cuando tengas equipo

**Razones:**
- Setup complejo (2-3 horas)
- Genera mucho ruido al principio
- Necesitas tiempo para configurar reglas
- Mejor cuando tienes varios desarrolladores

**Recomendación:** Empieza con Semgrep, añade SonarQube cuando tengas >5 desarrolladores

---

#### Qodo: ¿Para Qué Sirve?

**Qodo es útil para:**
1. **Revisión automática de PRs** (detecta bugs antes de mergear)
2. **Generación de tests** (crea tests automáticamente)
3. **Sugerencias de mejora** (refactoring, optimizaciones)

**¿Lo necesitas ahora?**
- Si trabajas solo: NO (yo te reviso el código)
- Si tienes equipo: SÍ (automatiza revisiones)

**Decisión:** Desinstala Qodo por ahora, reinstala cuando tengas equipo.

---

### 🎯 STACK FINAL DE SEGURIDAD (MVP)

```
1. Semgrep (SAST + Secrets)
   └── Reglas: GDPR + LOPDGDD custom

2. Snyk (SCA - Dependencias)
   └── Escanea npm + pip

3. GitHub Actions (CI/CD)
   └── Ejecuta Semgrep + Snyk en cada PR

4. Yo (Kiro) 😊
   └── Revisión de código + Fixes
```

**Coste:** €0  
**Tiempo setup:** 2 horas  
**Suficiente para:** MVP + Primeros 100 usuarios

---

## 12. RESUMEN DECISIONES FINALES

### ✅ FUNCIONALIDADES APROBADAS

| # | Funcionalidad | Prioridad | Estimación | Cuándo |
|---|---------------|-----------|------------|--------|
| 1 | **Mapas Mentales con Excalidraw** | 🔴 Alta | 4h | Sprint 1 |
| 2 | **Export a Anki (.apkg)** | 🟠 Media | 3h | Sprint 2 |
| 3 | **Generador de Memes** | 🟡 Baja | 4h | Sprint 3 |
| 4 | **Temas Oficiales Completos** | 🔴 Alta | 6h | Sprint 1 |
| 5 | **Dashboard de Configuración** | 🔴 Alta | 8h | Sprint 1 |
| 6 | **Mensajes Motivacionales** | 🟠 Media | 2h | Sprint 2 |
| 7 | **Google Drive OAuth2** | 🟠 Media | 4h | Sprint 3 |
| 8 | **Migración Frontend** | 🔴 Alta | 1h | Ahora |
| 9 | **Limpieza de Código** | 🔴 Alta | 2h | Ahora |

**Total nuevo:** 34 horas adicionales

---

### 📊 TIEMPO TOTAL ACTUALIZADO

| Epic | Original | Nuevas Funcionalidades | Total |
|------|----------|------------------------|-------|
| Epic 1: UX | 20h | +12h (Excalidraw, Dashboard) | 32h |
| Epic 2: Personalización | 16h | +2h (Mensajes) | 18h |
| Epic 3: Transparencia | 9h | - | 9h |
| Epic 4: Contexto | 19h | +7h (Google Drive, Anki) | 26h |
| Epic 5: Seguridad | 14h | - | 14h |
| Epic 6: Extras | - | +10h (Memes, Temas, Limpieza) | 10h |
| **TOTAL** | **78h** | **+31h** | **109h** |

**Nuevo timeline:** 11 semanas (2.5 meses)

---

### 🎯 PRIORIZACIÓN PARA MVP

#### MUST HAVE (Crítico para MVP)
1. ✅ Migración Frontend (1h)
2. ✅ Limpieza de Código (2h)
3. ✅ Dashboard de Configuración (8h)
4. ✅ Temas Oficiales Completos (6h)
5. ✅ Mapas Mentales con Excalidraw (4h)
6. ✅ Mensajes Motivacionales (2h)

**Subtotal MVP:** 23 horas

#### SHOULD HAVE (Importante pero no crítico)
7. ✅ Export a Anki (3h)
8. ✅ Google Drive OAuth2 (4h)

**Subtotal:** 7 horas

#### NICE TO HAVE (Puede esperar)
9. ⏸️ Generador de Memes (4h) - Posponer a post-MVP

---

### 📅 PLAN DE IMPLEMENTACIÓN ACTUALIZADO

#### Semana 1: Preparación y Limpieza
- [ ] Migración Frontend (1h)
- [ ] Limpieza de Código (2h)
- [ ] Dockerización (6h)
- [ ] Deploy VPS (2h)

**Total:** 11 horas

#### Semana 2-3: Funcionalidades Críticas
- [ ] Dashboard de Configuración (8h)
- [ ] Temas Oficiales Completos (6h)
- [ ] Mapas Mentales con Excalidraw (4h)
- [ ] Mensajes Motivacionales (2h)

**Total:** 20 horas

#### Semana 4-5: Stories del Plan Original
- [ ] Story 2.2: Algoritmo Adaptativo (8h)
- [ ] Story 4.1: RAG Adaptativo (10h)
- [ ] Story 4.2: Documentos Temporales (3h)
- [ ] Story 4.3: Búsqueda Web (6h)

**Total:** 27 horas

#### Semana 6-7: Integraciones
- [ ] Export a Anki (3h)
- [ ] Google Drive OAuth2 (4h)
- [ ] Story 5.1: Semgrep + Snyk (2h)

**Total:** 9 horas

#### Semana 8-9: Testing y Deploy
- [ ] Testing E2E (4h)
- [ ] Fixes de bugs (8h)
- [ ] Documentación (4h)
- [ ] Deploy producción (2h)

**Total:** 18 horas

**GRAN TOTAL:** 85 horas (~10 semanas)

---

### 💰 COSTES ACTUALIZADOS

| Servicio | MVP | Producción |
|----------|-----|------------|
| VPS Hostinger (8GB) | €10/mes | €10/mes |
| Vercel (Frontend) | €0 | €0 |
| Cloudflare Tunnel | €0 | €0 |
| Qdrant Cloud | €0 (1GB) | €25/mes (5GB) |
| Gemini API | €0 (1M tokens/día) | €25/mes |
| Google Custom Search | €0 (100/día) | €15/mes |
| Google Drive API | €0 | €0 |
| **TOTAL** | **€10/mes** | **€75/mes** |

---

### ✅ CHECKLIST FINAL ANTES DE EMPEZAR

#### Preparación
- [ ] Aprobar este documento completo
- [ ] Backup VPS actual
- [ ] Borrar Mistral del VPS
- [ ] Verificar 5GB libres

#### Cuentas y API Keys
- [ ] Cuenta Vercel
- [ ] Cuenta Cloudflare
- [ ] Gemini API key
- [ ] Google Custom Search API key
- [ ] Google OAuth2 credentials (client_id, client_secret)
- [ ] Qdrant Cloud API key

#### Configuración
- [ ] Dominio registrado (opositaia.com)
- [ ] DNS configurado
- [ ] .env con todas las keys
- [ ] Docker instalado en VPS

#### Código
- [ ] Migrar frontend a carpeta frontend/
- [ ] Borrar geminiService.tsx
- [ ] Limpiar código basura
- [ ] Actualizar .gitignore

---

### 🎯 PRÓXIMA ACCIÓN

**¿Qué hacemos primero?**

**Opción A: Preparación (Recomendado)**
1. Migración Frontend (1h)
2. Limpieza de Código (2h)
3. Dockerización (6h)

**Opción B: Funcionalidades Nuevas**
1. Dashboard de Configuración (8h)
2. Temas Oficiales (6h)

**Opción C: Plan Original**
1. Modificar Story 2.2 (8h)
2. Modificar Story 4.1 (10h)

**Mi recomendación:** Opción A (Preparación) - Mejor base para todo lo demás.

---

### 📞 PREGUNTAS FINALES

1. **¿Apruebas todas las nuevas funcionalidades?**
2. **¿Priorizamos como sugiero (MUST HAVE primero)?**
3. **¿Empezamos por Opción A (Preparación)?**
4. **¿Tienes dominio registrado o necesitas comprar?**
5. **¿Alguna funcionalidad adicional que se me haya olvidado?**

---

**Documento creado:** 26 Noviembre 2025  
**Próxima acción:** Esperar tu aprobación y empezar con la migración

