"""
Verificación completa antes de Sprint 3
"""
from qdrant_client import QdrantClient
from pathlib import Path

def verify_all():
    """Verificación completa del sistema"""
    
    print("\n" + "="*70)
    print("🔍 VERIFICACIÓN PRE-SPRINT 3")
    print("="*70 + "\n")
    
    errors = []
    warnings = []
    
    # 1. Verificar Qdrant
    print("1️⃣  Verificando Qdrant...")
    try:
        client = QdrantClient(url="http://localhost:6333")
        collection_name = "opositaia_leyes_seguridad_social"
        info = client.get_collection(collection_name)
        print(f"   ✅ Qdrant operativo")
        print(f"   ✅ Colección: {collection_name}")
        print(f"   ✅ Puntos: {info.points_count}")
    except Exception as e:
        errors.append(f"Qdrant no disponible: {e}")
        print(f"   ❌ Error: {e}")
    
    # 2. Verificar leyes indexadas
    print("\n2️⃣  Verificando leyes indexadas...")
    
    expected_laws = {
        "LGSS": {"tipo": "ley", "min_chunks": 500},
        "Constitución_Española": {"tipo": "constitucion", "min_chunks": 60}
    }
    
    for law_name, specs in expected_laws.items():
        try:
            result = client.scroll(
                collection_name=collection_name,
                limit=1,
                with_payload=True,
                with_vectors=False,
                scroll_filter={
                    "must": [
                        {
                            "key": "norma_nombre",
                            "match": {"value": law_name}
                        }
                    ]
                }
            )
            
            points, _ = result
            
            if points:
                # Contar total
                all_points = []
                offset = None
                while True:
                    result = client.scroll(
                        collection_name=collection_name,
                        limit=100,
                        offset=offset,
                        with_payload=True,
                        with_vectors=False,
                        scroll_filter={
                            "must": [
                                {
                                    "key": "norma_nombre",
                                    "match": {"value": law_name}
                                }
                            ]
                        }
                    )
                    pts, offset = result
                    all_points.extend(pts)
                    if offset is None:
                        break
                
                count = len(all_points)
                
                if count >= specs['min_chunks']:
                    print(f"   ✅ {law_name}: {count} chunks")
                else:
                    warnings.append(f"{law_name}: solo {count} chunks (esperado: {specs['min_chunks']})")
                    print(f"   ⚠️  {law_name}: {count} chunks (esperado: >{specs['min_chunks']})")
            else:
                errors.append(f"{law_name} no encontrado")
                print(f"   ❌ {law_name}: No encontrado")
                
        except Exception as e:
            errors.append(f"Error verificando {law_name}: {e}")
            print(f"   ❌ Error: {e}")
    
    # 3. Verificar archivos Sprint 3
    print("\n3️⃣  Verificando archivos Sprint 3...")
    
    data_dir = Path("backend/data/leyes")
    sprint3_files = ["Ley_39_2015.pdf", "Ley_40_2015.pdf", "EBEP.pdf"]
    
    for filename in sprint3_files:
        filepath = data_dir / filename
        if filepath.exists():
            size_mb = filepath.stat().st_size / (1024 * 1024)
            print(f"   ✅ {filename} ({size_mb:.2f} MB)")
        else:
            errors.append(f"Falta archivo: {filename}")
            print(f"   ❌ {filename}: No encontrado")
    
    # 4. Verificar espacio en Qdrant
    print("\n4️⃣  Verificando espacio...")
    
    current_size_mb = (info.points_count * 768 * 4) / (1024 * 1024)
    estimated_new = 1500  # ~500 chunks por ley x 3
    estimated_size_mb = (estimated_new * 768 * 4) / (1024 * 1024)
    total_estimated = current_size_mb + estimated_size_mb
    
    print(f"   📊 Tamaño actual: {current_size_mb:.2f} MB")
    print(f"   📊 Estimado Sprint 3: {estimated_size_mb:.2f} MB")
    print(f"   📊 Total estimado: {total_estimated:.2f} MB")
    
    if total_estimated < 100:
        print(f"   ✅ Espacio suficiente")
    else:
        warnings.append(f"Tamaño grande: {total_estimated:.2f} MB")
        print(f"   ⚠️  Tamaño considerable: {total_estimated:.2f} MB")
    
    # Resumen
    print("\n" + "="*70)
    print("📊 RESUMEN")
    print("="*70 + "\n")
    
    if not errors and not warnings:
        print("✅ SISTEMA LISTO PARA SPRINT 3")
        print("\nTodo verificado correctamente. Puedes proceder con:")
        print("   python backend/index_sprint3.py")
        return True
    
    if errors:
        print("❌ ERRORES CRÍTICOS:")
        for err in errors:
            print(f"   - {err}")
        print("\n⚠️  Resuelve los errores antes de continuar")
        return False
    
    if warnings:
        print("⚠️  ADVERTENCIAS:")
        for warn in warnings:
            print(f"   - {warn}")
        print("\n✅ Puedes continuar, pero revisa las advertencias")
        return True

if __name__ == "__main__":
    success = verify_all()
    exit(0 if success else 1)
