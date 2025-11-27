-- OpositAIA PostgreSQL Schema
-- Multi-Agent Architecture: User Progress Tracking
-- Created: 2024-11-16

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- 1. USER PROGRESS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS user_progress (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    
    -- Progress metrics
    temas_completados INTEGER[] DEFAULT '{}',
    temas_debiles INTEGER[] DEFAULT '{}',
    precision_global FLOAT DEFAULT 0.0,
    total_preguntas INTEGER DEFAULT 0,
    total_correctas INTEGER DEFAULT 0,
    
    -- Study stats
    dias_estudiados INTEGER DEFAULT 0,
    racha_actual INTEGER DEFAULT 0,
    racha_maxima INTEGER DEFAULT 0,
    ultima_sesion TIMESTAMP,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast lookups
CREATE INDEX idx_user_progress_email ON user_progress(email);
CREATE INDEX idx_user_progress_ultima_sesion ON user_progress(ultima_sesion);

-- ============================================
-- 2. ANSWER HISTORY TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS answer_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES user_progress(user_id) ON DELETE CASCADE,
    
    -- Question details
    pregunta_id UUID,
    pregunta_texto TEXT NOT NULL,
    tema_id INTEGER NOT NULL,
    tema_nombre VARCHAR(255),
    dificultad VARCHAR(50), -- 'facil', 'media', 'dificil'
    
    -- Answer details
    respuesta_usuario TEXT NOT NULL,
    respuesta_correcta TEXT NOT NULL,
    es_correcta BOOLEAN NOT NULL,
    
    -- Metadata
    tiempo_respuesta INTEGER, -- segundos
    intentos INTEGER DEFAULT 1,
    ayuda_usada BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for analytics
CREATE INDEX idx_answer_history_user_id ON answer_history(user_id);
CREATE INDEX idx_answer_history_tema_id ON answer_history(tema_id);
CREATE INDEX idx_answer_history_es_correcta ON answer_history(es_correcta);
CREATE INDEX idx_answer_history_created_at ON answer_history(created_at);

-- ============================================
-- 3. USER CASES TABLE (Casos Prácticos)
-- ============================================
CREATE TABLE IF NOT EXISTS user_cases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES user_progress(user_id) ON DELETE CASCADE,
    
    -- Case details
    titulo VARCHAR(500) NOT NULL,
    descripcion TEXT NOT NULL,
    tema_id INTEGER NOT NULL,
    tema_nombre VARCHAR(255),
    
    -- Solution
    solucion TEXT,
    referencias_boe TEXT[], -- URLs o artículos BOE
    
    -- Metadata
    es_publico BOOLEAN DEFAULT FALSE,
    likes INTEGER DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_user_cases_user_id ON user_cases(user_id);
CREATE INDEX idx_user_cases_tema_id ON user_cases(tema_id);
CREATE INDEX idx_user_cases_es_publico ON user_cases(es_publico);

-- ============================================
-- 4. SIMULACROS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS simulacros (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES user_progress(user_id) ON DELETE CASCADE,
    
    -- Simulacro details
    tipo VARCHAR(50) NOT NULL, -- 'oficial', 'personalizado', 'tematico'
    nombre VARCHAR(255),
    
    -- Results
    puntuacion FLOAT NOT NULL,
    tiempo_total INTEGER NOT NULL, -- segundos
    preguntas_correctas INTEGER NOT NULL,
    preguntas_totales INTEGER NOT NULL,
    
    -- Topics evaluated
    temas_evaluados INTEGER[] NOT NULL,
    
    -- Detailed results (JSON)
    resultados_detallados JSONB, -- {pregunta_id, correcta, tiempo, etc}
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_simulacros_user_id ON simulacros(user_id);
CREATE INDEX idx_simulacros_tipo ON simulacros(tipo);
CREATE INDEX idx_simulacros_created_at ON simulacros(created_at);

-- ============================================
-- 5. MIND MAPS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS mind_maps (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES user_progress(user_id) ON DELETE CASCADE,
    
    -- Mind map details
    tema_id INTEGER NOT NULL,
    tema_nombre VARCHAR(255) NOT NULL,
    titulo VARCHAR(500) NOT NULL,
    
    -- Content (JSON structure)
    contenido JSONB NOT NULL, -- {nodes: [], edges: [], layout: {}}
    
    -- Metadata
    es_publico BOOLEAN DEFAULT FALSE,
    likes INTEGER DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_mind_maps_user_id ON mind_maps(user_id);
CREATE INDEX idx_mind_maps_tema_id ON mind_maps(tema_id);

-- ============================================
-- 6. STUDY SESSIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS study_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES user_progress(user_id) ON DELETE CASCADE,
    
    -- Session details
    duracion INTEGER NOT NULL, -- segundos
    preguntas_respondidas INTEGER DEFAULT 0,
    preguntas_correctas INTEGER DEFAULT 0,
    temas_estudiados INTEGER[] DEFAULT '{}',
    
    -- Timestamps
    started_at TIMESTAMP NOT NULL,
    ended_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_study_sessions_user_id ON study_sessions(user_id);
CREATE INDEX idx_study_sessions_started_at ON study_sessions(started_at);

-- ============================================
-- 7. RECOMMENDATIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES user_progress(user_id) ON DELETE CASCADE,
    
    -- Recommendation details
    tipo VARCHAR(50) NOT NULL, -- 'tema', 'practica', 'repaso', 'simulacro'
    titulo VARCHAR(500) NOT NULL,
    descripcion TEXT NOT NULL,
    prioridad INTEGER DEFAULT 1, -- 1=baja, 2=media, 3=alta
    
    -- Action
    accion_url VARCHAR(500), -- Link to action
    accion_tipo VARCHAR(50), -- 'quiz', 'case', 'simulacro', 'mapa'
    
    -- Status
    vista BOOLEAN DEFAULT FALSE,
    completada BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP -- Recomendaciones pueden expirar
);

-- Indexes
CREATE INDEX idx_recommendations_user_id ON recommendations(user_id);
CREATE INDEX idx_recommendations_vista ON recommendations(vista);
CREATE INDEX idx_recommendations_completada ON recommendations(completada);

-- ============================================
-- 8. RAG QUERIES TABLE (Para análisis)
-- ============================================
CREATE TABLE IF NOT EXISTS rag_queries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES user_progress(user_id) ON DELETE SET NULL,
    
    -- Query details
    query_text TEXT NOT NULL,
    query_embedding VECTOR(1024), -- Para bge-m3 (1024 dims)
    
    -- Results
    documentos_encontrados INTEGER,
    top_score FLOAT,
    tiempo_busqueda INTEGER, -- milisegundos
    
    -- Feedback
    fue_util BOOLEAN,
    feedback_texto TEXT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_rag_queries_user_id ON rag_queries(user_id);
CREATE INDEX idx_rag_queries_created_at ON rag_queries(created_at);

-- ============================================
-- VIEWS FOR ANALYTICS
-- ============================================

-- View: User performance by topic
CREATE OR REPLACE VIEW user_performance_by_topic AS
SELECT 
    ah.user_id,
    ah.tema_id,
    ah.tema_nombre,
    COUNT(*) as total_preguntas,
    SUM(CASE WHEN ah.es_correcta THEN 1 ELSE 0 END) as correctas,
    ROUND(
        (SUM(CASE WHEN ah.es_correcta THEN 1 ELSE 0 END)::FLOAT / COUNT(*)::FLOAT) * 100, 
        2
    ) as precision_porcentaje,
    AVG(ah.tiempo_respuesta) as tiempo_promedio
FROM answer_history ah
GROUP BY ah.user_id, ah.tema_id, ah.tema_nombre;

-- View: User weak topics (precision < 70%)
CREATE OR REPLACE VIEW user_weak_topics AS
SELECT 
    user_id,
    tema_id,
    tema_nombre,
    total_preguntas,
    correctas,
    precision_porcentaje
FROM user_performance_by_topic
WHERE precision_porcentaje < 70
ORDER BY precision_porcentaje ASC;

-- View: User study streak
CREATE OR REPLACE VIEW user_study_streaks AS
SELECT 
    user_id,
    COUNT(DISTINCT DATE(started_at)) as dias_estudiados,
    MIN(started_at) as primera_sesion,
    MAX(started_at) as ultima_sesion,
    SUM(duracion) as tiempo_total_segundos,
    ROUND(SUM(duracion)::FLOAT / 3600, 2) as tiempo_total_horas
FROM study_sessions
GROUP BY user_id;

-- ============================================
-- FUNCTIONS
-- ============================================

-- Function: Update user progress after answer
CREATE OR REPLACE FUNCTION update_user_progress_after_answer()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE user_progress
    SET 
        total_preguntas = total_preguntas + 1,
        total_correctas = total_correctas + CASE WHEN NEW.es_correcta THEN 1 ELSE 0 END,
        precision_global = ROUND(
            ((total_correctas + CASE WHEN NEW.es_correcta THEN 1 ELSE 0 END)::FLOAT / 
             (total_preguntas + 1)::FLOAT) * 100, 
            2
        ),
        updated_at = CURRENT_TIMESTAMP
    WHERE user_id = NEW.user_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Update progress after answer
CREATE TRIGGER trigger_update_user_progress
AFTER INSERT ON answer_history
FOR EACH ROW
EXECUTE FUNCTION update_user_progress_after_answer();

-- Function: Calculate weak topics
CREATE OR REPLACE FUNCTION calculate_weak_topics(p_user_id UUID)
RETURNS INTEGER[] AS $$
DECLARE
    weak_topics INTEGER[];
BEGIN
    SELECT ARRAY_AGG(tema_id)
    INTO weak_topics
    FROM user_weak_topics
    WHERE user_id = p_user_id;
    
    RETURN COALESCE(weak_topics, '{}');
END;
$$ LANGUAGE plpgsql;

-- Function: Update weak topics for user
CREATE OR REPLACE FUNCTION update_weak_topics(p_user_id UUID)
RETURNS VOID AS $$
BEGIN
    UPDATE user_progress
    SET 
        temas_debiles = calculate_weak_topics(p_user_id),
        updated_at = CURRENT_TIMESTAMP
    WHERE user_id = p_user_id;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- SEED DATA (Optional)
-- ============================================

-- Insert test user
INSERT INTO user_progress (username, email)
VALUES ('test_user', 'test@opositaia.com')
ON CONFLICT (email) DO NOTHING;

-- ============================================
-- COMMENTS
-- ============================================

COMMENT ON TABLE user_progress IS 'Tracks overall user progress and statistics';
COMMENT ON TABLE answer_history IS 'Stores every answer submitted by users for analytics';
COMMENT ON TABLE user_cases IS 'User-created practical cases';
COMMENT ON TABLE simulacros IS 'Mock exam results';
COMMENT ON TABLE mind_maps IS 'User-created mind maps for topics';
COMMENT ON TABLE study_sessions IS 'Tracks study session duration and activity';
COMMENT ON TABLE recommendations IS 'AI-generated personalized recommendations';
COMMENT ON TABLE rag_queries IS 'Logs RAG search queries for analysis';

-- ============================================
-- GRANTS (Adjust based on your setup)
-- ============================================

-- Grant permissions to backend user (adjust username)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO opositaia_backend;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO opositaia_backend;
-- GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO opositaia_backend;
