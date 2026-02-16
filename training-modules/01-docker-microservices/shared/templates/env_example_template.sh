# ==============================================================================
# .env.example - Environment Variables Template
# ==============================================================================
# Purpose: Template for project configuration (commit this file to git)
# Usage: Copy to .env and customize for your environment
#        cp .env.example .env
# Security: NEVER commit the actual .env file (it's in .gitignore)
# ==============================================================================

# ------------------------------------------------------------------------------
# PROJECT CONFIGURATION
# ------------------------------------------------------------------------------
# Project name (used in container names)
PROJECT_NAME=myapp

# Environment (development, staging, production)
ENVIRONMENT=development

# ------------------------------------------------------------------------------
# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# PostgreSQL credentials
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=myapp
DB_HOST=db
DB_PORT=5432

# Full database URL (auto-constructed from above)
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}

# ------------------------------------------------------------------------------
# REDIS CONFIGURATION
# ------------------------------------------------------------------------------
REDIS_HOST=cache
REDIS_PORT=6379
REDIS_DB=0
REDIS_URL=redis://${REDIS_HOST}:${REDIS_PORT}/${REDIS_DB}

# ------------------------------------------------------------------------------
# APPLICATION SETTINGS
# ------------------------------------------------------------------------------
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=2

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Secret key (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
SECRET_KEY=change-me-in-production

# CORS settings
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# ------------------------------------------------------------------------------
# MCP SERVICE CONFIGURATION
# ------------------------------------------------------------------------------
MCP_ENABLED=false
MCP_HOST=mcp-service
MCP_PORT=8001
MCP_API_KEY=change-me

# ------------------------------------------------------------------------------
# EXTERNAL SERVICES
# ------------------------------------------------------------------------------
# AWS (if needed)
# AWS_ACCESS_KEY_ID=
# AWS_SECRET_ACCESS_KEY=
# AWS_REGION=us-east-1
# S3_BUCKET=

# OpenAI (if needed)
# OPENAI_API_KEY=

# ------------------------------------------------------------------------------
# DOCKER RESOURCE LIMITS
# ------------------------------------------------------------------------------
# Override default resource limits per service
WEB_CPU_LIMIT=1.0
WEB_MEMORY_LIMIT=1G
DB_MEMORY_LIMIT=512M
CACHE_MEMORY_LIMIT=256M

# ------------------------------------------------------------------------------
# DEVELOPMENT SETTINGS
# ------------------------------------------------------------------------------
# Enable debug mode (DO NOT use in production)
DEBUG=true

# Hot reload for development
RELOAD=true

# ------------------------------------------------------------------------------
# MACHINE-SPECIFIC SETTINGS
# ------------------------------------------------------------------------------
# Machine identifier (for tracking which machine last modified code)
MACHINE_ID=DESKTOP-6NMJEGK

# Local file paths (adjust for your machine)
# LOCAL_DATA_PATH=/mnt/c/Users/YourUsername/data
# LOCAL_MODELS_PATH=/mnt/c/Users/YourUsername/models

# ==============================================================================
# SETUP INSTRUCTIONS
# ==============================================================================
#
# 1. Copy this file:
#    cp .env.example .env
#
# 2. Edit .env with your actual values:
#    nano .env
#
# 3. Generate secure secrets:
#    python -c "import secrets; print(secrets.token_urlsafe(32))"
#
# 4. Update credentials (especially DB_PASSWORD and SECRET_KEY)
#
# 5. NEVER commit .env to git (it's already in .gitignore)
#
# ==============================================================================

# ==============================================================================
# NOTES FOR STUDENTS
# ==============================================================================
#
# - Use strong passwords in production (not "postgres")
# - Rotate secrets regularly
# - Keep .env.example updated when adding new variables
# - Use different .env files for dev, staging, production
# - Consider using secret management tools (AWS Secrets Manager, etc.)
#
# ==============================================================================