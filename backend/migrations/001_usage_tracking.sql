-- Migration: Usage Tracking Table
-- Date: 2025-11-30

CREATE TABLE IF NOT EXISTS usage_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255),
    session_id VARCHAR(255),
    provider_id VARCHAR(50) NOT NULL,
    model_name VARCHAR(100),
    input_tokens INTEGER NOT NULL,
    output_tokens INTEGER NOT NULL,
    total_tokens INTEGER NOT NULL,
    input_cost_eur DECIMAL(10,6),
    output_cost_eur DECIMAL(10,6),
    total_cost_eur DECIMAL(10,6),
    endpoint VARCHAR(100),
    request_type VARCHAR(50),
    request_duration_ms INTEGER,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_usage_user_date ON usage_logs(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_usage_provider ON usage_logs(provider_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_usage_session ON usage_logs(session_id);
