#!/usr/bin/env python3
"""
FASE 2: ENRIQUECIMIENTO DEL DATASET - VERSIÓN CORREGIDA
========================================================
Flujo correcto:
1. Buscar en Qdrant (búsqueda semántica)
2. Extraer BOE ID del payload
3. Consultar tabla leyes_catalogo con BOE ID
4. Enriquecer con URL, fecha vigor, metadata completa
"""

import json
import requests
import re
import psycopg2
from pathlib import Path
import time

DATASET = Path("golden_dataset/consolidated/golden_dataset_cleaned.jsonl")
OUTPUT = Path("golden_dataset/consolidated/golden_dataset_enriched.jsonl")
BACKEND = "http://127.0.0.1:8000"

# PostgreSQL
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'opositaia'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'

def get_law_metadata_from_catalog(boe_id):
    """Consulta tabla leyes_catalogo para obtener metadata completa"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                boe_id,
                nombre_corto,
                titulo,
                url_boe,
                url_eli,
                fecha_entrada_vigor,
                departamento_nombre,
                tipo_norma
            FROM leyes_catalogo
            WHERE boe_id = %s;
        """, (boe_id,))
        
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if row:
            return {
                'boe_id': row[0],
                'nombre_corto': row[1],
                'titulo': row[2],
                'url_boe': row[3],
                'url_eli': row[4],
                'fecha_vigor': str(row[5]) if row[5] else None,
                'departamento': row[6],
                'tipo_norma': row[7]
            }
        return None
        
    except Exception as e:
        print(f"  ❌ Error consultando catálogo: {e}", flush=True)
        return None

def extract_articulos(texto):
    """Extraer menciones de artículos del texto"""
    if not texto:
        return []
    
    patrones = [
        r'Art\.\s*(\d+)',
        r'Artículo\s*(\d+)',
        r'art\s+(\d+)',
    ]
    
    articulos = []
    for patron in patrones:
        matches = re.findall(patron, texto, re.IGNORECASE)
        articulos.extend(matches)
    
    return list(set(articulos))

def buscar_citas_rag(pregunta, explicacion, max_retries=3):
    """Buscar citas legales usando RAG + enriquecimiento con tabla"""
    query = f"{pregunta} {explicacion[:200]}"
    
    for intento in range(max_retries):
        try:
            response = requests.post(
                f"{BACKEND}/api/rag/search",
                json={"query": query, "top_k": 3, "min_score": 0.3},
                timeout=120
            )
            
            if response.status_code == 200:
                docs = response.json().get('documents', [])
                
                citas = []
                for doc in docs:
                    metadata = doc.get('metadata', {})
                    
                    # Extraer BOE ID del metadata de Qdrant
                    boe_id = None
                    
                    # Intentar diferentes fuentes de BOE ID
                    # 1. Directamente en metadata
                    if 'boe_id' in metadata:
                        boe_id = metadata['boe_id']
                    
                    # 2. En metadata anidado
                    elif isinstance(metadata, dict):
                        data = metadata.get('data', {})
                        if isinstance(data, dict):
                            metadatos = data.get('metadatos', {})
                            if isinstance(metadatos, dict):
                                identificador = metadatos.get('identificador', {})
                                if isinstance(identificador, dict):
                                    boe_id = identificador.get('_text', '')
                    
                    # 3. Consultar tabla leyes_catalogo si tenemos BOE ID
                    if boe_id:
                        law_metadata = get_law_metadata_from_catalog(boe_id)
                        
                        if law_metadata:
                            # Extraer artículo del contenido
                            articulo = metadata.get('articulo', 'N/A')
                            norma_nombre = law_metadata.get('nombre_corto', metadata.get('norma_nombre', 'LGSS'))
                            
                            citas.append({
                                'articulo': articulo,
                                'ley': norma_nombre,
                                'url': law_metadata['url_boe'],
                                'url_eli': law_metadata.get('url_eli'),
                                'boe_id': boe_id,
                                'fecha_vigor': law_metadata.get('fecha_vigor'),
                                'verificado': True
                            })
                        else:
                            # Si no está en catálogo, usar metadata básico
                            citas.append({
                                'articulo': metadata.get('articulo', 'N/A'),
                                'ley': metadata.get('norma_nombre', 'LGSS'),
                                'url': f'https://www.boe.es/buscar/doc.php?id={boe_id}',
                                'boe_id': boe_id,
                                'verificado': False
                            })
                
                return citas
            else:
                print(f"  ⚠️ Intento {intento+1}/{max_retries}: Status {response.status_code}", flush=True)
        
        except requests.exceptions.Timeout:
            print(f"  ⚠️ Intento {intento+1}/{max_retries}: Timeout", flush=True)
            if intento < max_retries - 1:
                wait_time = 2 ** intento
                print(f"  ⏳ Esperando {wait_time}s antes de reintentar...", flush=True)
                time.sleep(wait_time)
        
        except Exception as e:
            print(f"  ❌ Intento {intento+1}/{max_retries}: Error - {str(e)[:100]}", flush=True)
            if intento < max_retries - 1:
                time.sleep(2 ** intento)
    
    return []

def enriquecer_item(item, index):
    """Enriquecer un item con citas y URLs"""
    cambios = []
    
    try:
        pregunta = item.get('pregunta', '')
        explicacion = item.get('explicacion', '')
        
        # 1. Verificar si ya tiene citas
        articulos_existentes = extract_articulos(explicacion)
        
        # 2. Si no tiene citas, buscar en RAG
        if not articulos_existentes and pregunta and explicacion:
            citas = buscar_citas_rag(pregunta, explicacion)
            
            if citas:
                # Añadir citas a la explicación
                cita_texto = citas[0]
                if cita_texto['articulo'] != 'N/A':
                    nueva_explicacion = f"{explicacion} (Art. {cita_texto['articulo']} {cita_texto['ley']})"
                    item['explicacion'] = nueva_explicacion
                    cambios.append('cita_añadida')
                    print(f"  ✅ {index}: Cita añadida - Art. {cita_texto['articulo']} {cita_texto['ley']}", flush=True)
                
                # Añadir URL BOE si está disponible
                if cita_texto.get('url'):
                    item['url_boe'] = cita_texto['url']
                    item['verificado'] = cita_texto.get('verificado', False)
                    cambios.append('url_añadida')
                    print(f"  ✅ {index}: URL añadida - {cita_texto['url']}", flush=True)
                    
                    # Añadir metadata adicional si está disponible
                    if cita_texto.get('fecha_vigor'):
                        item['fecha_vigor'] = cita_texto['fecha_vigor']
                    if cita_texto.get('url_eli'):
                        item['url_eli'] = cita_texto['url_eli']
        
        # 3. Si tiene citas pero no URL, buscar URL
        elif articulos_existentes and not item.get('url_boe'):
            citas = buscar_citas_rag(pregunta, explicacion)
            
            if citas and citas[0].get('url'):
                item['url_boe'] = citas[0]['url']
                item['verificado'] = citas[0].get('verificado', False)
                cambios.append('url_añadida')
                print(f"  ✅ {index}: URL añadida a item con citas", flush=True)
    
    except Exception as e:
        print(f"  ❌ {index}: Error - {str(e)[:100]}", flush=True)
    
    return item, cambios

def main():
    print("="*70, flush=True)
    print("🔧 FASE 2: ENRIQUECIMIENTO DEL DATASET - VERSIÓN CORREGIDA", flush=True)
    print("="*70, flush=True)
    print(f"📁 Input: {DATASET}", flush=True)
    print(f"📁 Output: {OUTPUT}", flush=True)
    print(f"🌐 Backend: {BACKEND}", flush=True)
    print(f"💾 PostgreSQL: {DB_HOST}:{DB_PORT}/{DB_NAME}", flush=True)
    
    # Verificar backend
    try:
        response = requests.get(f"{BACKEND}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ Backend funcionando", flush=True)
        else:
            print(f"❌ Backend no responde", flush=True)
            return
    except Exception as e:
        print(f"❌ Error conectando al backend: {e}", flush=True)
        return
    
    # Verificar PostgreSQL
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM leyes_catalogo;")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        print(f"✅ PostgreSQL funcionando ({count} leyes en catálogo)", flush=True)
    except Exception as e:
        print(f"❌ Error conectando a PostgreSQL: {e}", flush=True)
        return
    
    items = []
    stats = {
        'total': 0,
        'citas_añadidas': 0,
        'urls_añadidas': 0,
        'sin_cambios': 0
    }
    
    print("\n📖 Leyendo dataset limpio...", flush=True)
    with open(DATASET, 'r', encoding='utf-8') as f:
        for line in f:
            items.append(json.loads(line))
    
    print(f"Total items: {len(items)}", flush=True)
    print("\n🔄 Enriqueciendo items...", flush=True)
    print("   (Esto puede tardar 30-60 minutos)\n", flush=True)
    
    items_enriquecidos = []
    
    for i, item in enumerate(items, 1):
        item_enriquecido, cambios = enriquecer_item(item, i)
        items_enriquecidos.append(item_enriquecido)
        
        stats['total'] += 1
        if 'cita_añadida' in cambios:
            stats['citas_añadidas'] += 1
        if 'url_añadida' in cambios:
            stats['urls_añadidas'] += 1
        if not cambios:
            stats['sin_cambios'] += 1
        
        if i % 100 == 0:
            print(f"   Progreso: {i}/{len(items)}", flush=True)
            print(f"      Citas añadidas: {stats['citas_añadidas']}", flush=True)
            print(f"      URLs añadidas: {stats['urls_añadidas']}", flush=True)
            
            # DETECCIÓN DE FALLOS: Si después de 100 items no hay cambios, parar
            if i == 100 and stats['citas_añadidas'] == 0 and stats['urls_añadidas'] == 0:
                print("\n⚠️ WARNING: 0 cambios después de 100 items", flush=True)
                print("Deteniendo para revisión...", flush=True)
                break
            
            # Pausa cada 100 items
            if i < len(items):
                print(f"   ⏸️  Pausa de 5s (lote completado)...", flush=True)
                time.sleep(5)
    
    # Guardar dataset enriquecido
    print(f"\n💾 Guardando dataset enriquecido...", flush=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        for item in items_enriquecidos:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print("\n" + "="*70, flush=True)
    print("📊 RESULTADOS DE ENRIQUECIMIENTO", flush=True)
    print("="*70, flush=True)
    print(f"Total items procesados: {stats['total']}", flush=True)
    print(f"Citas añadidas:         {stats['citas_añadidas']} ({stats['citas_añadidas']/stats['total']*100:.1f}%)", flush=True)
    print(f"URLs añadidas:          {stats['urls_añadidas']} ({stats['urls_añadidas']/stats['total']*100:.1f}%)", flush=True)
    print(f"Sin cambios:            {stats['sin_cambios']} ({stats['sin_cambios']/stats['total']*100:.1f}%)", flush=True)
    
    # Calcular mejora
    mejora_total = stats['citas_añadidas'] + stats['urls_añadidas']
    print(f"\n✅ Items mejorados: {mejora_total} ({mejora_total/stats['total']*100:.1f}%)", flush=True)
    
    print("\n" + "="*70, flush=True)
    print("✅ FASE 2 COMPLETADA", flush=True)
    print("="*70, flush=True)
    print(f"Dataset enriquecido guardado: {OUTPUT}", flush=True)

if __name__ == "__main__":
    main()
