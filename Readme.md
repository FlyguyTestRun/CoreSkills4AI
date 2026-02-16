# CoreSkills4AI Training Platform

**Professional training modules for AI, DevOps, and enterprise infrastructure education**

---

## Overview

CoreSkills4AI is a comprehensive training platform designed for hands-on learning in artificial intelligence, DevOps practices, and enterprise infrastructure management. The platform provides production-ready environments, real-world scenarios, and practical automation tools for building advanced technical skills.

**Target Audience:**
- DevOps engineers learning AI integration patterns
- IT professionals transitioning to cloud-native architectures
- Students building enterprise infrastructure skills
- Teams implementing agentic AI workflows

---

## Training Modules

### [01: Docker Microservices](./training-modules/01-docker-microservices/)
**Production VM Training Environment**

A complete Docker-based training platform featuring:
- 6-container microservices architecture (API Gateway, PostgreSQL, Redis, PowerShell worker, Grafana, Prometheus)
- Enterprise device & identity lifecycle management simulation
- One-command startup with automated health checks (`start.py`)
- Comprehensive API testing suite (`test_api.py`)
- Real-world observability with Grafana dashboards and Prometheus metrics

**Technologies:** Docker, Python 3.12, PowerShell 7.4, PostgreSQL, Redis, Flask, Grafana, Prometheus

**Use Cases:**
- Classroom training (supports 20+ concurrent VMs)
- DevOps bootcamp demonstrations
- API development & testing labs
- Monitoring & observability workshops

---

### [02: PowerShell Automation](./training-modules/02-powershell-automation/)
**Identity Management & Infrastructure Automation**

Production-quality PowerShell modules for enterprise automation:
- **KISDIdentity.psm1** - Student/staff identity lifecycle management for K-12 environments
- Active Directory automation with grade-level OUs (9-12)
- FERPA-compliant audit logging
- Batch account provisioning from CSV (SIS integration ready)

**Technologies:** PowerShell 7.4+, Active Directory, Azure AD/Entra ID

**Skills Developed:**
- Enterprise identity management patterns
- PowerShell module development
- Compliance & audit logging
- CSV data processing and validation

---

### [03: Docker Labs](./training-modules/03-docker-labs/)
**Advanced Docker Techniques**

Hands-on labs covering advanced Docker concepts:
- Container debugging and troubleshooting
- Volume persistence patterns
- Build optimization strategies
- Multi-stage Dockerfile best practices

**Technologies:** Docker, Docker Compose, Container debugging tools

**Learning Objectives:**
- Debug containers in production environments
- Optimize Docker images for size and performance
- Implement data persistence strategies
- Apply security best practices

---

### [04: Agentic AI Engineering](./training-modules/04-agentic-ai-engineering/)
**AI-Assisted Development with PIV Workflow**

Learn to build AI-powered applications using the Prime-Implement-Validate (PIV) workflow:
- **Habit Tracker Demo** - Full-stack FastAPI + React application
- Claude-assisted development patterns
- Agentic workflow automation
- Production deployment strategies

**Technologies:** FastAPI, React, SQLite, Claude AI, Python async patterns

**PIV Workflow:**
1. **Prime** - Define requirements with AI assistance
2. **Implement** - Build features with AI pair programming
3. **Validate** - Test and refine with AI-powered quality checks

---

### [05: Docker Examples](./training-modules/05-docker-examples/)
**Beginner-Friendly Docker Tutorials**

Introductory Docker examples for newcomers:
- Bind mount applications
- Multi-container applications
- Welcome to Docker tutorials

**Technologies:** Docker basics, Docker Compose fundamentals

**Target Audience:** Docker beginners, bootcamp students

---

## Quick Start

### Prerequisites
- Docker Desktop or Docker Engine installed
- Python 3.12+ (for Docker Microservices module)
- PowerShell 7.4+ (for PowerShell Automation module)
- WSL2 (Windows users - see [Setup Guides](#setup-guides))

### Running Module 01: Docker Microservices

```bash
cd training-modules/01-docker-microservices

# One-command startup
python start.py

# Access services:
# - API Gateway: http://localhost:5000
# - Grafana Dashboard: http://localhost:3000 (admin/admin)
# - Prometheus Metrics: http://localhost:9090

# Run automated tests
python test_api.py

# View demo automation
python scripts/demo.py

# Graceful shutdown
python stop.py
```

---

## Module Templates

The `module-templates/` folder provides scaffolding for creating new training modules:
- `.devcontainer/` - VS Code development container configuration
- `docker-template/` - Docker service templates
- `test-template/` - Automated testing patterns

Use these templates to contribute new training modules to the platform.

---

## Technology Stack

**Core Technologies:**
- **Containerization:** Docker, Docker Compose
- **Backend:** Python 3.12+, FastAPI, Flask
- **Automation:** PowerShell 7.4+, Python scripting
- **Databases:** PostgreSQL, Redis, SQLite
- **Monitoring:** Grafana, Prometheus
- **AI Integration:** Claude AI, agentic workflows

**Cloud & Infrastructure:**
- Microsoft Azure (Azure AD/Entra ID)
- Active Directory Domain Services
- Infrastructure as Code patterns

---

## Learning Path

**Beginner Track:**
1. Module 05: Docker Examples (basics)
2. Module 01: Docker Microservices (production environment)
3. Module 03: Docker Labs (advanced techniques)

**DevOps Track:**
1. Module 01: Docker Microservices (orchestration)
2. Module 03: Docker Labs (optimization)
3. Module 02: PowerShell Automation (infrastructure automation)

**AI Engineering Track:**
1. Module 04: Agentic AI Engineering (PIV workflow)
2. Module 01: Docker Microservices (backend patterns)
3. Module 02: PowerShell Automation (automation patterns)

---

## Professional Background

This training platform was developed by **Bryan Shaw**, Senior AI Architect-Engineer with 22+ years of enterprise experience. The modules reflect real-world consulting projects, enterprise deployments, and production-grade patterns used in Fortune 500 environments.

**Areas of Expertise:**
- Enterprise GenAI & RAG systems
- Microsoft 365 / Azure / Entra ID administration
- Docker containerization & microservices
- FastAPI & async Python patterns
- PowerShell infrastructure automation
- K-12 educational technology

---

## Related Projects

- **[Keller ISD Systems Engineering Showcase](https://github.com/FlyguyTestRun/Keller-ISD-Showcase)** - K-12 identity management, Veeam DR, Dell iDRAC automation
- **[Professional Portfolio](https://github.com/FlyguyTestRun/Portfolio)** - Consulting work, case studies, technical expertise

---

## License

This project is licensed under the terms specified in the [LICENSE](./LICENSE) file.

---

## Contact & Support

- **Author:** Bryan Shaw
- **Email:** BryanJShaw@gmail.com
- **LinkedIn:** [linkedin.com/in/bryan-shaw-45a23124](https://www.linkedin.com/in/bryan-shaw-45a23124/)
- **GitHub:** [github.com/FlyguyTestRun](https://github.com/FlyguyTestRun/)

---

**Built with Claude AI | Production-Ready Training Modules | Real-World Expertise**
