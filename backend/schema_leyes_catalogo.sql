-- =====================================================
-- TABLA LEYES_CATALOGO - METADATA COMPLETA DE BOE
-- =====================================================
-- Fecha: 26 Diciembre 2025
-- Objetivo: Centralizar TODA la metadata de leyes del BOE
-- Fuente: API datos abiertos BOE + XML consolidado + Análisis
-- =====================================================

CREATE TABLE IF NOT EXISTS leyes_catalogo (
    -- ============================================
    -- IDENTIFICACIÓN
    -- ============================================
    id SERIAL PRIMARY KEY,
    boe_id TEXT UNIQUE NOT NULL,                    -- BOE-A-1984-26864
    identificador_eli TEXT,                         -- Identificador ELI europeo
    
    -- ============================================
    -- INFORMACIÓN BÁSICA
    -- ============================================
    nombre_corto TEXT,                              -- LGSS, TREBEP, etc.
    titulo TEXT NOT NULL,                           -- Título completo oficial
    titulo_resumido TEXT,                           -- Título corto
    
    -- ============================================
    -- CLASIFICACIÓN
    -- ============================================
    tipo_norma TEXT,                                -- Ley, RD, LO, Decreto, etc.
    rango_codigo INTEGER,                           -- Código numérico del rango
    rango_nombre TEXT,                              -- Nombre del rango
    
    -- ============================================
    -- ORGANISMO EMISOR
    -- ============================================
    departamento_codigo INTEGER,                    -- Código del departamento
    departamento_nombre TEXT,                       -- Jefatura del Estado, Ministerio, etc.
    organismo_emisor TEXT,                          -- Organismo específico
    
    -- ============================================
    -- FECHAS CRÍTICAS
    -- ============================================
    fecha_publicacion DATE,                         -- Fecha publicación en BOE
    fecha_entrada_vigor DATE,                       -- ⭐ CRÍTICO: Cuándo entró en vigor
    fecha_derogacion DATE,                          -- Si está derogada
    fecha_actualizacion TIMESTAMP,                  -- Última actualización en BOE
    
    -- ============================================
    -- ESTADO Y VIGENCIA
    -- ============================================
    vigente BOOLEAN DEFAULT TRUE,                   -- Si está vigente
    consolidado BOOLEAN DEFAULT FALSE,              -- Si es texto consolidado
    version_consolidada TEXT,                       -- Versión del consolidado
    
    -- ============================================
    -- URLs OFICIALES
    -- ============================================
    url_boe TEXT,                                   -- https://www.boe.es/buscar/doc.php?id=...
    url_eli TEXT,                                   -- URL ELI oficial europea
    url_pdf TEXT,                                   -- PDF oficial
    url_pdf_consolidado TEXT,                       -- PDF consolidado
    url_xml TEXT,                                   -- XML del documento
    url_html TEXT,                                  -- HTML del documento
    
    -- ============================================
    -- ANÁLISIS Y MODIFICACIONES (PESTAÑA ANÁLISIS)
    -- ============================================
    analisis_modificaciones JSONB,                  -- Array de modificaciones
    /*
    Estructura:
    [
        {
            "fecha": "2024-01-15",
            "boe_id": "BOE-A-2024-1234",
            "tipo": "modificacion",
            "descripcion": "Modifica art. 25",
            "articulos_afectados": ["25", "26"]
        }
    ]
    */
    
    analisis_afecta_a JSONB,                        -- Leyes que esta ley afecta
    /*
    Estructura:
    [
        {
            "boe_id": "BOE-A-2015-11724",
            "nombre": "LGSS",
            "tipo_afectacion": "modifica"
        }
    ]
    */
    
    analisis_afectada_por JSONB,                    -- Leyes que afectan a esta
    
    -- ============================================
    -- ESTRUCTURA Y CONTENIDO
    -- ============================================
    num_articulos INTEGER,                          -- Número de artículos
    num_disposiciones_adicionales INTEGER,
    num_disposiciones_transitorias INTEGER,
    num_disposiciones_finales INTEGER,
    num_disposiciones_derogatorias INTEGER,
    
    tiene_anexos BOOLEAN DEFAULT FALSE,
    num_anexos INTEGER,
    
    -- ============================================
    -- METADATA COMPLETA (XML ORIGINAL)
    -- ============================================
    metadata_xml JSONB,                             -- TODO el XML parseado a JSON
    /*
    Incluye TODOS los campos del XML:
    - ambito (Estatal, Autonómico, etc.)
    - materias (array de materias)
    - referencias (a otras normas)
    - notas
    - observaciones
    - etc.
    */
    
    -- ============================================
    -- CONTENIDO COMPLETO
    -- ============================================
    texto_completo TEXT,                            -- Texto completo de la ley
    xml_original TEXT,                              -- XML original del BOE
    
    -- ============================================
    -- ÍNDICES Y NAVEGACIÓN
    -- ============================================
    indice_estructurado JSONB,                      -- Índice de la ley
    /*
    Estructura:
    {
        "titulos": [
            {
                "numero": "I",
                "nombre": "Disposiciones generales",
                "capitulos": [...]
            }
        ]
    }
    */
    
    -- ============================================
    -- BÚSQUEDA Y TAGS
    -- ============================================
    materias TEXT[],                                -- Array de materias
    palabras_clave TEXT[],                          -- Keywords para búsqueda
    tags TEXT[],                                    -- Tags adicionales
    
    -- ============================================
    -- RELACIONES
    -- ============================================
    ley_padre_id TEXT,                              -- Si es modificación de otra ley
    leyes_relacionadas TEXT[],                      -- Array de BOE IDs relacionados
    
    -- ============================================
    -- METADATOS DEL SISTEMA
    -- ============================================
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    ingested_at TIMESTAMP,                          -- Cuándo se ingirió en el sistema
    source TEXT DEFAULT 'BOE_API',                  -- Fuente de los datos
    
    -- ============================================
    -- NOTAS Y OBSERVACIONES
    -- ============================================
    notas TEXT,                                     -- Notas adicionales
    observaciones TEXT                              -- Observaciones importantes
);

-- =====================================================
-- ÍNDICES PARA BÚSQUEDA RÁPIDA
-- =====================================================

CREATE INDEX idx_leyes_boe_id ON leyes_catalogo(boe_id);
CREATE INDEX idx_leyes_nombre_corto ON leyes_catalogo(nombre_corto);
CREATE INDEX idx_leyes_tipo_norma ON leyes_catalogo(tipo_norma);
CREATE INDEX idx_leyes_departamento ON leyes_catalogo(departamento_codigo);
CREATE INDEX idx_leyes_vigente ON leyes_catalogo(vigente);
CREATE INDEX idx_leyes_fecha_publicacion ON leyes_catalogo(fecha_publicacion);
CREATE INDEX idx_leyes_fecha_vigor ON leyes_catalogo(fecha_entrada_vigor);

-- Índice GIN para búsqueda en JSONB
CREATE INDEX idx_leyes_metadata_gin ON leyes_catalogo USING GIN (metadata_xml);
CREATE INDEX idx_leyes_modificaciones_gin ON leyes_catalogo USING GIN (analisis_modificaciones);

-- Índice para búsqueda de texto completo
CREATE INDEX idx_leyes_texto_completo ON leyes_catalogo USING GIN (to_tsvector('spanish', texto_completo));

-- =====================================================
-- COMENTARIOS
-- =====================================================

COMMENT ON TABLE leyes_catalogo IS 'Catálogo completo de leyes con metadata del BOE, análisis de modificaciones y URLs verificadas';
COMMENT ON COLUMN leyes_catalogo.boe_id IS 'Identificador único del BOE (ej: BOE-A-1984-26864)';
COMMENT ON COLUMN leyes_catalogo.fecha_entrada_vigor IS 'CRÍTICO: Fecha en que la ley entró en vigor (puede ser diferente a fecha_publicacion)';
COMMENT ON COLUMN leyes_catalogo.analisis_modificaciones IS 'Historial completo de modificaciones de la pestaña Análisis del BOE';
COMMENT ON COLUMN leyes_catalogo.metadata_xml IS 'Metadata completa del XML del BOE sin omitir ningún campo';
