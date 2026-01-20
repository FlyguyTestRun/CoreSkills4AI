-- ==============================================================================
-- Database Initialization Script
-- ==============================================================================
-- Location: docker/init-db/01-init.sql
-- Purpose: Initialize PostgreSQL database schema on first container startup
-- Execution: Runs automatically when PostgreSQL container starts (if db is empty)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- SECTION 1: Database Setup
-- ------------------------------------------------------------------------------
-- Create extensions (if needed)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text search
CREATE EXTENSION IF NOT EXISTS "pgcrypto";  -- For encryption functions

-- Set timezone
SET timezone = 'UTC';

-- ------------------------------------------------------------------------------
-- SECTION 2: Users Table
-- ------------------------------------------------------------------------------
-- Core users table for authentication
CREATE TABLE IF NOT EXISTS users (
    -- Primary key
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- User credentials
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    
    -- User profile
    full_name VARCHAR(100),
    avatar_url TEXT,
    
    -- Account status
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    is_admin BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE,
    
    -- Soft delete
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Indexes for performance
CREATE INDEX idx_users_email ON users(email) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_username ON users(username) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_created_at ON users(created_at DESC);

-- ------------------------------------------------------------------------------
-- SECTION 3: Projects Table
-- ------------------------------------------------------------------------------
-- Example domain table (customize for your application)
CREATE TABLE IF NOT EXISTS projects (
    -- Primary key
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Foreign key to users
    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Project details
    name VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'archived', 'deleted')),
    
    -- Metadata
    tags TEXT[],
    metadata JSONB DEFAULT '{}',
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Soft delete
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Indexes
CREATE INDEX idx_projects_owner_id ON projects(owner_id);
CREATE INDEX idx_projects_status ON projects(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_projects_created_at ON projects(created_at DESC);
CREATE INDEX idx_projects_tags ON projects USING GIN(tags);

-- ------------------------------------------------------------------------------
-- SECTION 4: Tasks Table (Example Many-to-One Relationship)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS tasks (
    -- Primary key
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Foreign keys
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    assigned_to UUID REFERENCES users(id) ON DELETE SET NULL,
    
    -- Task details
    title VARCHAR(200) NOT NULL,
    description TEXT,
    priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    status VARCHAR(20) DEFAULT 'todo' CHECK (status IN ('todo', 'in_progress', 'review', 'done')),
    
    -- Dates
    due_date TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Soft delete
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Indexes
CREATE INDEX idx_tasks_project_id ON tasks(project_id);
CREATE INDEX idx_tasks_assigned_to ON tasks(assigned_to);
CREATE INDEX idx_tasks_status ON tasks(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_tasks_due_date ON tasks(due_date) WHERE deleted_at IS NULL;

-- ------------------------------------------------------------------------------
-- SECTION 5: Audit Log Table
-- ------------------------------------------------------------------------------
-- Track all changes to important tables
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- What changed
    table_name VARCHAR(50) NOT NULL,
    record_id UUID NOT NULL,
    action VARCHAR(20) NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    
    -- Who changed it
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    
    -- Change details
    old_values JSONB,
    new_values JSONB,
    
    -- Metadata
    ip_address INET,
    user_agent TEXT,
    
    -- When
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_audit_log_table_name ON audit_log(table_name);
CREATE INDEX idx_audit_log_record_id ON audit_log(record_id);
CREATE INDEX idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX idx_audit_log_created_at ON audit_log(created_at DESC);

-- ------------------------------------------------------------------------------
-- SECTION 6: Triggers for Updated_at
-- ------------------------------------------------------------------------------
-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to all tables with updated_at
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projects_updated_at
    BEFORE UPDATE ON projects
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ------------------------------------------------------------------------------
-- SECTION 7: Sample Data (Development Only)
-- ------------------------------------------------------------------------------
-- Insert test user (password: 'password123' - hashed with bcrypt)
-- In production, remove this section!
INSERT INTO users (username, email, password_hash, full_name, is_verified, is_admin)
VALUES 
    ('admin', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYKKVrCAnNm', 'Admin User', TRUE, TRUE),
    ('testuser', 'test@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYKKVrCAnNm', 'Test User', TRUE, FALSE)
ON CONFLICT (username) DO NOTHING;

-- Insert sample project
INSERT INTO projects (owner_id, name, description, status, tags)
SELECT 
    u.id,
    'Sample Project',
    'This is a test project for development',
    'active',
    ARRAY['development', 'sample']
FROM users u
WHERE u.username = 'admin'
ON CONFLICT DO NOTHING;

-- Insert sample tasks
INSERT INTO tasks (project_id, assigned_to, title, description, priority, status)
SELECT 
    p.id,
    u.id,
    'Setup Development Environment',
    'Configure WSL2, Docker, and VS Code',
    'high',
    'done'
FROM projects p
CROSS JOIN users u
WHERE p.name = 'Sample Project' AND u.username = 'testuser'
ON CONFLICT DO NOTHING;

-- ------------------------------------------------------------------------------
-- SECTION 8: Views (Optional)
-- ------------------------------------------------------------------------------
-- Useful view: Active projects with task counts
CREATE OR REPLACE VIEW active_projects_summary AS
SELECT 
    p.id,
    p.name,
    p.description,
    u.username AS owner_username,
    COUNT(t.id) AS total_tasks,
    COUNT(t.id) FILTER (WHERE t.status = 'done') AS completed_tasks,
    COUNT(t.id) FILTER (WHERE t.status IN ('todo', 'in_progress')) AS active_tasks,
    p.created_at,
    p.updated_at
FROM projects p
LEFT JOIN users u ON p.owner_id = u.id
LEFT JOIN tasks t ON p.id = t.project_id AND t.deleted_at IS NULL
WHERE p.deleted_at IS NULL AND p.status = 'active'
GROUP BY p.id, p.name, p.description, u.username, p.created_at, p.updated_at;

-- ------------------------------------------------------------------------------
-- SECTION 9: Grants (Security)
-- ------------------------------------------------------------------------------
-- Grant appropriate permissions
-- Note: Adjust these based on your application's needs

-- Revoke all public permissions
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;

-- Grant select, insert, update, delete to application user
-- (Uncomment and modify for production)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO myapp_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO myapp_user;

-- ==============================================================================
-- COMPLETION MESSAGE
-- ==============================================================================
DO $$
BEGIN
    RAISE NOTICE '============================================';
    RAISE NOTICE 'Database initialization completed!';
    RAISE NOTICE 'Tables created: users, projects, tasks, audit_log';
    RAISE NOTICE 'Sample users: admin, testuser';
    RAISE NOTICE 'Default password: password123';
    RAISE NOTICE 'IMPORTANT: Change passwords in production!';
    RAISE NOTICE '============================================';
END $$;

-- ==============================================================================
-- NOTES FOR STUDENTS
-- ==============================================================================
-- 
-- This script demonstrates:
-- 1. Table creation with proper constraints
-- 2. Indexes for query performance
-- 3. Foreign key relationships
-- 4. Triggers for automatic timestamp updates
-- 5. Sample data for development
-- 6. Views for complex queries
-- 7. Security considerations
--
-- Best Practices:
-- - Always use UUID for primary keys (better than auto-increment)
-- - Include created_at/updated_at timestamps
-- - Use soft deletes (deleted_at) instead of hard deletes
-- - Add indexes on foreign keys and frequently queried columns
-- - Use CHECK constraints for data validation
-- - Document your schema with comments
--
-- ==============================================================================