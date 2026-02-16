#!/bin/bash
# ==============================================================================
# WSL2 + Docker Desktop + VS Code Setup Script
# ==============================================================================
# Purpose: Automated setup for production-grade development environment
# Machine: DESKTOP-6NMJEGK (Intel i7-6500U, 12GB RAM)
# Author: Development Team
# Usage: ./setup.sh
# ==============================================================================

set -e  # Exit on error
set -u  # Exit on undefined variable

# ------------------------------------------------------------------------------
# COLORS FOR OUTPUT
# ------------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ------------------------------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------------------------------
print_header() {
    echo -e "\n${BLUE}===================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}===================================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

check_command() {
    if command -v "$1" &> /dev/null; then
        print_success "$1 is installed"
        return 0
    else
        print_error "$1 is NOT installed"
        return 1
    fi
}

# ------------------------------------------------------------------------------
# SYSTEM REQUIREMENTS CHECK
# ------------------------------------------------------------------------------
print_header "Step 1: System Requirements Check"

echo "Checking WSL version..."
if wsl.exe --version &> /dev/null; then
    print_success "WSL is installed"
    wsl.exe --version
else
    print_error "WSL is not installed or not accessible"
    exit 1
fi

echo -e "\nChecking required tools..."
TOOLS_OK=true

for tool in git curl wget; do
    if ! check_command "$tool"; then
        TOOLS_OK=false
    fi
done

if [ "$TOOLS_OK" = false ]; then
    print_warning "Installing missing tools..."
    sudo apt-get update
    sudo apt-get install -y git curl wget
fi

# ------------------------------------------------------------------------------
# CREATE .wslconfig (WINDOWS SIDE)
# ------------------------------------------------------------------------------
print_header "Step 2: Creating .wslconfig (Windows Side)"

WINDOWS_USER=$(cmd.exe /c "echo %USERNAME%" 2>/dev/null | tr -d '\r')
WSLCONFIG_PATH="/mnt/c/Users/$WINDOWS_USER/.wslconfig"

print_warning "Creating .wslconfig at: $WSLCONFIG_PATH"

cat > "$WSLCONFIG_PATH" << 'WSLCONFIG_EOF'
[wsl2]
memory=6GB
processors=3
swap=2GB
localhostForwarding=true
networkingMode=mirrored
dnsTunneling=true
autoProxy=true
sparseVhd=true
nestedVirtualization=true
pageReporting=true
autoMemoryReclaim=gradual
WSLCONFIG_EOF

print_success ".wslconfig created successfully"
print_warning "You must run 'wsl --shutdown' from PowerShell to apply these settings"

# ------------------------------------------------------------------------------
# CREATE wsl.conf (WSL SIDE)
# ------------------------------------------------------------------------------
print_header "Step 3: Creating wsl.conf (WSL Side)"

print_warning "Creating /etc/wsl.conf (requires sudo)..."

sudo tee /etc/wsl.conf > /dev/null << 'WSLCONF_EOF'
[boot]
systemd=true

[automount]
enabled=true
root=/mnt/
mountFsTab=true
options="metadata,umask=022,fmask=11,dmask=022,case=off"

[network]
generateHosts=true
generateResolvConf=true

[interop]
enabled=true
appendWindowsPath=true
WSLCONF_EOF

print_success "/etc/wsl.conf created successfully"

# ------------------------------------------------------------------------------
# INSTALL DOCKER (if not present)
# ------------------------------------------------------------------------------
print_header "Step 4: Docker Installation Check"

if check_command docker; then
    print_success "Docker is already installed"
else
    print_warning "Docker not found. Installing Docker..."
    
    # Update package index
    sudo apt-get update
    
    # Install prerequisites
    sudo apt-get install -y \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    
    # Add Docker's official GPG key
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    
    # Set up repository
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Install Docker Engine
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    
    # Add current user to docker group
    sudo usermod -aG docker "$USER"
    
    print_success "Docker installed successfully"
    print_warning "You may need to log out and back in for group changes to take effect"
fi

# ------------------------------------------------------------------------------
# INSTALL DOCKER COMPOSE
# ------------------------------------------------------------------------------
print_header "Step 5: Docker Compose Installation Check"

if docker compose version &> /dev/null; then
    print_success "Docker Compose is already installed"
    docker compose version
else
    print_error "Docker Compose plugin not found"
    print_warning "Installing Docker Compose plugin..."
    sudo apt-get update
    sudo apt-get install -y docker-compose-plugin
fi

# ------------------------------------------------------------------------------
# CREATE PROJECT DIRECTORY STRUCTURE
# ------------------------------------------------------------------------------
print_header "Step 6: Creating Project Directory Structure"

PROJECT_ROOT="$HOME/projects"

print_warning "Creating directory structure in: $PROJECT_ROOT"

mkdir -p "$PROJECT_ROOT"/{web-apps,databases,microservices,ml-models,mcp-services,_templates,_shared,_docs}
mkdir -p "$PROJECT_ROOT/_shared"/{docker-networks,configs,scripts,volumes}

print_success "Project directories created"

# Create shared Docker networks compose file
cat > "$PROJECT_ROOT/_shared/docker-networks/docker-compose.yml" << 'NETWORK_EOF'
version: '3.8'

networks:
  app-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
  
  db-network:
    driver: bridge
    internal: true
  
  mcp-network:
    driver: bridge
NETWORK_EOF

print_success "Shared Docker networks configured"

# ------------------------------------------------------------------------------
# CREATE PROJECT TEMPLATE
# ------------------------------------------------------------------------------
print_header "Step 7: Creating Project Template"

TEMPLATE_DIR="$PROJECT_ROOT/_templates/python-microservice"
mkdir -p "$TEMPLATE_DIR"/{src,tests,docker,.devcontainer,.vscode,docs}

# Create basic files
touch "$TEMPLATE_DIR"/{README.md,.gitignore,.dockerignore,docker-compose.yml,Dockerfile,requirements.txt}

print_success "Project template created at: $TEMPLATE_DIR"

# ------------------------------------------------------------------------------
# INSTALL PYTHON DEPENDENCIES
# ------------------------------------------------------------------------------
print_header "Step 8: Python Environment Setup"

if check_command python3; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python is installed: $PYTHON_VERSION"
else
    print_warning "Installing Python..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-venv
fi

# Install useful Python tools
print_warning "Installing Python development tools..."
pip3 install --user --upgrade pip black pylint pytest pytest-cov

print_success "Python tools installed"

# ------------------------------------------------------------------------------
# CONFIGURE GIT
# ------------------------------------------------------------------------------
print_header "Step 9: Git Configuration"

if [ -z "$(git config --global user.name)" ]; then
    print_warning "Git user.name not set"
    read -p "Enter your Git name: " git_name
    git config --global user.name "$git_name"
fi

if [ -z "$(git config --global user.email)" ]; then
    print_warning "Git user.email not set"
    read -p "Enter your Git email: " git_email
    git config --global user.email "$git_email"
fi

# Configure Git for better performance on WSL2
git config --global core.autocrlf input
git config --global core.filemode false
git config --global pull.rebase false

print_success "Git configured"
echo "  Name:  $(git config --global user.name)"
echo "  Email: $(git config --global user.email)"

# ------------------------------------------------------------------------------
# CREATE HELPER SCRIPTS
# ------------------------------------------------------------------------------
print_header "Step 10: Creating Helper Scripts"

# Create project creation script
cat > "$PROJECT_ROOT/_shared/scripts/create-project.sh" << 'CREATE_PROJ_EOF'
#!/bin/bash
# Create new project from template

if [ -z "$1" ]; then
    echo "Usage: ./create-project.sh <project-name> [category]"
    echo "Categories: web-apps, microservices, ml-models, databases, mcp-services"
    exit 1
fi

PROJECT_NAME=$1
CATEGORY=${2:-microservices}
PROJECT_ROOT="$HOME/projects"
TEMPLATE="$PROJECT_ROOT/_templates/python-microservice"
TARGET="$PROJECT_ROOT/$CATEGORY/$PROJECT_NAME"

if [ -d "$TARGET" ]; then
    echo "Error: Project $TARGET already exists"
    exit 1
fi

echo "Creating project: $PROJECT_NAME in $CATEGORY"
cp -r "$TEMPLATE" "$TARGET"

cd "$TARGET"
git init
git add .
git commit -m "Initial commit from template"

echo "✓ Project created: $TARGET"
echo "  Next steps:"
echo "    cd $TARGET"
echo "    code ."
CREATE_PROJ_EOF

chmod +x "$PROJECT_ROOT/_shared/scripts/create-project.sh"
print_success "Helper scripts created"

# ------------------------------------------------------------------------------
# FINAL INSTRUCTIONS
# ------------------------------------------------------------------------------
print_header "Setup Complete!"

cat << 'FINAL_EOF'

╔═══════════════════════════════════════════════════════════════════════════╗
║                         SETUP COMPLETED SUCCESSFULLY                      ║
╚═══════════════════════════════════════════════════════════════════════════╝

CRITICAL: Complete these final steps:

1. RESTART WSL2 (from PowerShell on Windows):
   
   wsl --shutdown
   
   Then restart WSL

2. VERIFY WSL2 CONFIGURATION:
   
   wsl --status
   systemctl status docker

3. INSTALL VS CODE EXTENSIONS:
   - Remote - WSL
   - Docker
   - Python
   - Dev Containers

4. CREATE YOUR FIRST PROJECT:
   
   cd ~/projects/_shared/scripts
   ./create-project.sh my-first-app microservices
   code ~/projects/microservices/my-first-app

5. CONFIGURE DOCKER DESKTOP (Windows):
   - Open Docker Desktop
   - Settings → Resources → WSL Integration
   - Enable integration with Ubuntu
   - Settings → Resources → Memory: 4GB
   - Settings → Resources → CPUs: 2

6. TEST SETUP:
   
   cd ~/projects/microservices/my-first-app
   docker-compose up -d
   docker-compose ps
   docker-compose down

╔═══════════════════════════════════════════════════════════════════════════╗
║                            DIRECTORY STRUCTURE                            ║
╚═══════════════════════════════════════════════════════════════════════════╝

~/projects/
├── web-apps/          # Web applications
├── microservices/     # Microservices
├── ml-models/         # Machine learning projects
├── databases/         # Database containers
├── mcp-services/      # MCP services
├── _templates/        # Project templates
├── _shared/           # Shared configs & scripts
└── _docs/             # Documentation

Files created:
✓ C:\Users\<Username>\.wslconfig
✓ /etc/wsl.conf
✓ ~/projects/* (directory structure)

╔═══════════════════════════════════════════════════════════════════════════╗
║                            TROUBLESHOOTING                                ║
╚═══════════════════════════════════════════════════════════════════════════╝

If Docker won't start:
  sudo systemctl enable docker
  sudo systemctl start docker

If VS Code can't connect to WSL:
  Install "Remote - WSL" extension
  Open folder in WSL: Ctrl+Shift+P → "Remote-WSL: Open Folder"

If resource usage is high:
  Reduce limits in .wslconfig
  Close unused containers: docker-compose down

If Git commits fail:
  Always work in ~/projects (not /mnt/c)
  Ensure you're in WSL2 filesystem

FINAL_EOF

print_success "All done! Follow the instructions above to complete setup."