# Leyes Pendientes de Scraping / Ingesta Alternativa

Estas leyes fallaron durante la ingesta automática vía API BOE (Error 404 en metadatos o texto consolidado).
Se deben procesar mediante scraping web directo o descarga de PDF y OCR si es necesario.

## Lista de IDs Fallidos
- BOE-A-2008-1782 (RD 34/2008 Registro entidades de formación)
- BOE-A-2008-4900 (Orden TAS/718/2008 Catálogo especialidades)
- BOE-A-2015-7058 (RD 7/2015 Programas comunes activación empleo)
- BOE-A-2022-21341 (Estrategia Apoyo Activo al Empleo 2024-2028)
- BOE-A-1995-1322 (RD 4/1995 Reglamento ETT)
- BOE-A-2010-18860 (RD 1796/2010 Agencias de colocación)
- BOE-A-2007-19991 (Ley 44/2007 Empresas de inserción)
- BOE-A-2022-6265 (RDL 4/2022 Transición al empleo estable)
- BOE-A-2011-17052 (RD 1543/2011 Prácticas no laborales)
- BOE-A-2019-3819 (RD 103/2019 Cartera Común Servicios SNE)
- BOE-A-1994-18814 (RD 1844/1994 Elecciones representación)
- BOE-A-1995-21112 (Jornadas especiales RD 1561/1995)
- BOE-A-2024-2790 (SMI 2024 RD 145/2024)
- BOE-A-2015-7867 (TR Ley de Empleo RDL 3/2015)
- BOE-A-2015-2770 (RDL 4/2015 reforma urgente FP Empleo)
- BOE-A-1977-8805 (RDL relaciones de trabajo 17/1977)

## Acción Requerida
1. Verificar si existen en formato web (HTML) en `boe.es`.
2. Crear un scraper específico o usar `fetch_webpage` para obtener su contenido.
3. Ingestar en Qdrant manualmente.
