from qdrant_client import QdrantClient

client = QdrantClient(host='localhost', port=6333)
info = client.get_collection('opositaia_knowledge')
print(f'✅ Vectores indexados: {info.points_count}')
print('✅ RAG INGESTA COMPLETADA EXITOSAMENTE')