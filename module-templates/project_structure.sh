#!/bin/bash
# ==============================================================================
# Project Structure Setup Script
# ==============================================================================
# Purpose: Creates production-grade directory structure for containerized projects
# Location: Run from WSL2 Ubuntu terminal
# Machine: DESKTOP-6NMJEGK
# ==============================================================================

# ------------------------------------------------------------------------------
# CONFIGURATION VARIABLES
# ------------------------------------------------------------------------------
PROJECT_ROOT="$HOME/projects"
CONFIG_DIR="$HOME/.config/dev-environment"
TEMPLATE_DIR="$PROJECT_ROOT/_templates"

# ------------------------------------------------------------------------------
# CREATE BASE DIRECTORY STRUCTURE
# ------------------------------------------------------------------------------
echo "Creating base project structure in $PROJECT_ROOT..."

mkdir -p "$PROJECT_ROOT"/{
  web-apps,
  databases,
  microservices,
  ml-models,
  mcp-services,
  _templates,
  _shared,
  _docs
}

# ------------------------------------------------------------------------------
# SHARED RESOURCES DIRECTORY
# ------------------------------------------------------------------------------
# Stores common configs, utilities, and Docker networks
mkdir -p "$PROJECT_ROOT/_shared"/{
  docker-networks,
  configs,
  scripts,
  volumes
}

# Create shared Docker network configuration
cat > "$PROJECT_ROOT/_shared/docker-networks/docker-compose.yml" << 'EOF'
# Shared Docker Networks for Inter-Container Communication
version: '3.8'

networks:
  # Primary application network
  app-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
  
  # Database-only network (isolated)
  db-network:
    driver: bridge
    internal: true
  
  # MCP services network
  mcp-network:
    driver: bridge

# Use these networks in your project docker-compose.yml with:
# networks:
#   - app-network
#   - db-network
EOF

# ------------------------------------------------------------------------------
# DOCUMENTATION DIRECTORY
# ------------------------------------------------------------------------------
mkdir -p "$PROJECT_ROOT/_docs"

cat > "$PROJECT_ROOT/_docs/README.md" << 'EOF'
# Development Environment Documentation

## Directory Structure

```
~/projects/
├── web-apps/          # Web application projects
├── databases/         # Database containers & configs
├── microservices/     # Microservice projects
├── ml-models/         # Machine learning projects
├── mcp-services/      # MCP (Model Context Protocol) services
├── _templates/        # Project templates
├── _shared/           # Shared configs & Docker networks
└── _docs/             # Documentation
```

## Quick Start

1. Navigate to project category: `cd ~/projects/web-apps`
2. Create new project from template: `./create-project.sh my-app`
3. Start development: `code ~/projects/web-apps/my-app`
4. Start containers: `docker-compose up -d`

## Git Workflow

- Each project is a separate Git repository
- Push/pull before switching machines
- Use `.gitignore` to exclude containers, volumes, logs

## Resource Management

- Start only needed containers: `docker-compose up <service>`
- Stop unused containers: `docker-compose down`
- Check resources: `docker stats`
EOF

# ------------------------------------------------------------------------------
# CREATE PROJECT TEMPLATE
# ------------------------------------------------------------------------------
echo "Creating project template..."

mkdir -p "$TEMPLATE_DIR/python-microservice"

# Template directory structure
mkdir -p "$TEMPLATE_DIR/python-microservice"/{
  src,
  tests,
  docker,
  .devcontainer,
  .vscode,
  docs
}

# Create template files (these will be detailed in separate artifacts)
touch "$TEMPLATE_DIR/python-microservice"/{
  README.md,
  .gitignore,
  .dockerignore,
  docker-compose.yml,
  Dockerfile,
  requirements.txt,
  setup.py
}

# ------------------------------------------------------------------------------
# CREATE CONFIGURATION DIRECTORY
# ------------------------------------------------------------------------------
echo "Creating configuration directory..."

mkdir -p "$CONFIG_DIR"/{
  docker,
  git,
  vscode,
  scripts
}

# ------------------------------------------------------------------------------
# COMPLETION MESSAGE
# ------------------------------------------------------------------------------
echo "✅ Project structure created successfully!"
echo ""
echo "Directory: $PROJECT_ROOT"
echo ""
echo "Next steps:"
echo "1. Review structure: tree ~/projects -L 2"
echo "2. Initialize git in each project: cd ~/projects/<project> && git init"
echo "3. Open in VS Code: code ~/projects"
echo ""
echo "Template location: $TEMPLATE_DIR"