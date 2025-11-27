# 🔄 Guía de Migración VPS

**Fecha**: 2024-11-16

---

## ¿Es difícil migrar a otro VPS?

**Respuesta**: NO, es fácil con Docker

---

## Estrategia de Migración

### Opción A: Docker Compose ⭐ RECOMENDADO

**Ventaja**: Portabilidad total

**Pasos**:
1. Backup de datos
2. En nuevo VPS: `docker-compose up -d`
3. Restaurar backups
4. Cambiar DNS

**Tiempo**: 1-2 horas  
**Downtime**: <30 minutos

---

## Checklist de Migración

### 1. Backup PostgreSQL
```bash
pg_dump opositaia > backup.sql
```

### 2. Backup Qdrant
```bash
curl -X POST http://localhost:6333/collections/opositaia_documents/snapshots
```

### 3. Backup .env
```bash
cp .env .env.backup
cp .env.backend .env.backend.backup
```

### 4. Nuevo VPS: Instalar Docker
```bash
curl -fsSL https://get.docker.com | sh
```

### 5. Clonar repo
```bash
git clone https://github.com/tu-usuario/opositaia.git
cd opositaia
```

### 6. Restaurar .env
```bash
cp .env.backup .env
cp .env.backend.backup .env.backend
```

### 7. Docker Compose up
```bash
docker-compose up -d
```

### 8. Restaurar PostgreSQL
```bash
psql opositaia < backup.sql
```

### 9. Restaurar Qdrant
```bash
curl -X PUT http://localhost:6333/collections/opositaia_documents/snapshots/upload \
  --data-binary @snapshot.tar
```

### 10. Verificar
```bash
curl http://localhost:8000/health
```

### 11. Cambiar DNS
```
A record: tu-dominio.com → nueva-ip-vps
```

### 12. Monitorear 24h

---

## Proveedores VPS Recomendados

| Proveedor | RAM | CPU | Disco | Precio/Mes |
|-----------|-----|-----|-------|------------|
| Hostinger (actual) | 16 GB | 4 vCPU | 200 GB | 7€? |
| **Hetzner** ⭐ | 16 GB | 4 vCPU | 160 GB | **€15** |
| DigitalOcean | 16 GB | 4 vCPU | 320 GB | €90 |
| Linode | 16 GB | 6 vCPU | 320 GB | €90 |
| Vultr | 16 GB | 4 vCPU | 320 GB | €90 |

**Recomendación**: Hetzner (mejor precio/calidad en Europa)

---

## 🎯 Conclusión

**Migrar es FÁCIL** si:
1. ✅ Usas Docker Compose
2. ✅ Tienes backups automáticos
3. ✅ Documentas el proceso

**Tiempo**: 1-2 horas  
**Downtime**: <30 minutos
