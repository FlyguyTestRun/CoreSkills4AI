# 🎓 CoreSkills4ai Command Center

> **Enterprise Device & Identity Lifecycle Management Platform**
> VM training environment for Microsoft infrastructure automation, Agentic AI-assisted operations, and modern DevOps practices.

[![Docker](https://img.shields.io/badge/Docker-20.10+-blue.svg)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.12-green.svg)](https://www.python.org/)
[![PowerShell](https://img.shields.io/badge/PowerShell-7.4-blue.svg)](https://github.com/PowerShell/PowerShell)
[![License](https://img.shields.io/badge/License-Educational-orange.svg)]()

---

## 📋 Table of Contents

- [Overview](#-overview)
- [System Architecture](#-system-architecture)
- [Quick Start Guide](#-quick-start-guide)
- [Python Scripts Reference](#-python-scripts-reference)
- [Technology Stack](#-technology-stack)
- [API Documentation](#-api-documentation)
- [Monitoring & Metrics](#-monitoring--metrics)
- [Troubleshooting](#-troubleshooting)
- [Advanced Usage](#-advanced-usage)

---

## 🌟 Overview

CoreSkills4ai Command Center is a **containerized training platform** designed for hands-on learning of:

- 🔧 **DevOps Automation** - Docker, REST APIs, Infrastructure as Code
- 🖥️ **PowerShell Administration** - Identity management, batch processing
- 📊 **Observability** - Grafana dashboards, Prometheus metrics, system monitoring
- 🗄️ **Database Operations** - PostgreSQL, Redis queue management
- 🔐 **Enterprise IT** - Student/staff lifecycle, device compliance, policy enforcement

### Use Cases

✅ Classroom training environments (20+ concurrent VMs)
✅ DevOps bootcamp demonstrations
✅ PowerShell automation workshops
✅ API development & testing labs
✅ Monitoring & observability training

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CoreSkills4ai Platform                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐   │
│  │   Grafana    │◄─────│  Prometheus  │◄─────│  API Gateway │   │
│  │   :3000      │      │    :9090     │      │    :5000     │   │
│  │  (Dashboard) │      │  (Metrics)   │      │   (Flask)    │   │
│  └──────────────┘      └──────────────┘      └──────┬───────┘   │
│                                                      │          │
│                        ┌─────────────────────────────┘          │
│                        │                                        │
│         ┌──────────────▼──────────┐        ┌─────────────────┐  │
│         │   PostgreSQL :5432      │◄───────│   Redis :6379   │  │
│         │   (Data Storage)        │        │  (Job Queue)    │  │
│         └─────────────────────────┘        └────────┬────────┘  │
│                                                      │          │
│                                    ┌─────────────────▼────────┐ │
│                                    │  PowerShell Automation   │ │
│                                    │      (Worker Engine)     │ │
│                                    └──────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **API Request** → Student creation via REST API
2. **Job Queue** → Redis stores job for async processing
3. **Worker** → PowerShell polls queue and processes job
4. **Database** → PostgreSQL stores result
5. **Metrics** → Prometheus scrapes API metrics
6. **Visualization** → Grafana displays real-time dashboards

---

## 🚀 Quick Start Guide

### Prerequisites

- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
- **Python 3.8+** (for automation scripts)
- **Git** (for cloning repository)
- **4GB RAM** minimum, 8GB recommended
- **10GB free disk space**

### 1. Installation

```bash
# Clone repository
git clone https://github.com/FlyguyTestRun/Class-Room-Modules.git
cd "ClassRoom Modules"

# Verify Docker is running
docker --version
docker ps
```

### 2. Start the System (Method 1: Python Script - Recommended)

```bash
# One-command startup
python start.py
```

**What it does:**
- ✅ Checks Docker is running
- ✅ Creates `.env` file from template
- ✅ Builds all container images
- ✅ Starts 6 containers (API, DB, Redis, Worker, Grafana, Prometheus)
- ✅ Waits for health checks
- ✅ Displays access URLs

**Expected output:**
```
╔══════════════════════════════════════════════════════════╗
║   CoreSkills4ai Command Center - Startup Script          ║
╚══════════════════════════════════════════════════════════╝

✅ Docker is ready
✅ .env file exists
...
✅ Startup Complete!

📍 Access URLs:
   API Gateway:    http://localhost:5000
   Grafana:        http://localhost:3000 (admin/admin)
   Prometheus:     http://localhost:9090
```

### 2. Start the System (Method 2: Manual)

```bash
# Start core services
docker-compose up -d

# Start monitoring stack
docker-compose -f docker/monitoring/docker-compose.monitoring.yml up -d

# Verify all containers running
docker ps
```

### 3. Seed Sample Data

```bash
# Load 20 students, 12 devices, 7 policies
python scripts/seed_database.py
```

**What it does:**
- Loads realistic test data from JSON files
- Populates PostgreSQL with sample records
- Prompts before clearing existing data
- Verifies successful insertion

### 4. Verify System Health

```bash
# Run comprehensive health check
python scripts/health_check.py
```

**Checks:**
- ✅ All 6 containers running
- ✅ Database connectivity
- ✅ API endpoints responding
- ✅ Seed data present
- ✅ Metrics flowing to Prometheus
- ✅ Grafana accessible

### 5. Run Demo (Optional)

```bash
# Automated 5-minute demonstration
python scripts/demo.py
```

**Demonstrates:**
- Creating students via API
- Job queue processing
- Database verification
- Traffic generation
- Metrics collection

---

## 📜 Python Scripts Reference

All scripts located in project root and `scripts/` directory.

### Core Startup Scripts

#### `start.py` - System Startup

```bash
python start.py
```

**Purpose:** One-command startup for all services
**Duration:** ~60 seconds
**Requirements:** Docker running

**Process:**
1. Validates Docker installation and daemon
2. Creates `.env` from template if missing
3. Stops any existing containers
4. Builds container images (cached after first run)
5. Starts 6 containers with health checks
6. Waits for API to be ready
7. Displays access URLs and quick commands

**Output Indicators:**
- ✅ Green checkmarks = Success
- ⚠️ Yellow warnings = Non-critical issues
- ❌ Red X = Failures requiring attention

**Common Issues:**
- "Docker daemon not running" → Start Docker Desktop
- "Port already in use" → Check for conflicting services
- "Build failed" → Check internet connection for image downloads

---

#### `stop.py` - System Shutdown

```bash
python stop.py
```

**Purpose:** Graceful shutdown of all services
**Duration:** ~10 seconds
**What it does:**
- Stops Grafana and Prometheus
- Stops API, worker, database, Redis
- Removes containers (preserves volumes)
- Shows any remaining containers

**Use when:**
- Finished working with the system
- Need to free up system resources
- Troubleshooting requires clean restart

---

### Database Management

#### `scripts/seed_database.py` - Load Sample Data

```bash
python scripts/seed_database.py
```

**Purpose:** Populate database with realistic test data
**Duration:** ~10 seconds
**Data loaded:**
- 20 students (grades 9-12, balanced distribution)
- 12 devices (Windows, Mac, Chromebook, iPad)
- 7 compliance policies (security, network, updates)

**Process:**
1. Loads JSON files from `scripts/sample_data/`
2. Connects to PostgreSQL
3. Optionally clears existing data (prompts for confirmation)
4. Inserts students → devices → policies (order matters for foreign keys)
5. Verifies counts in database

**Sample Data Files:**
- `scripts/sample_data/students.json` - 20 realistic student records
- `scripts/sample_data/devices.json` - 12 device assignments
- `scripts/sample_data/policies.json` - 7 enterprise policies

**Customization:**
Edit JSON files to add your own test data. Schema:
```json
{
  "student_id": "S2026001",
  "first_name": "Emma",
  "last_name": "Johnson",
  "grade_level": 12,
  "graduation_year": 2026
}
```

---

### Testing & Validation

#### `test_api.py` - Comprehensive API Tests

```bash
python test_api.py
```

**Purpose:** Validate all API endpoints and features
**Duration:** ~20 seconds
**Tests performed (6 total):**

1. **Health Check** - `/health` endpoint returns 200 + DB/Redis status
2. **Get Users** - `/api/v1/users` returns user list
3. **Create Student** - `POST /api/v1/users/student` queues job
4. **Job Status** - `/api/v1/jobs/{id}` polls until completion
5. **Get Devices** - `/api/v1/devices` returns device list
6. **Metrics** - `/metrics` exports Prometheus data

**Output Example:**
```
╔══════════════════════════════════════════════════════════╗
║   CoreSkills4ai Command Center - API Test Suite          ║
╚══════════════════════════════════════════════════════════╝

=============================================================
  1. Testing Health Check
=============================================================
Status Code: 200
Response: {
  "status": "healthy",
  "database": "connected",
  "redis": "connected"
}

...

Test Summary
=============================================================
✅ PASS  Health Check
✅ PASS  Get Users
✅ PASS  Create Student
✅ PASS  Job Status
✅ PASS  Get Devices
✅ PASS  Metrics

Results: 6/6 tests passed (100%)
🎉 All tests passed! System is working correctly.
```

**Exit Codes:**
- `0` = All tests passed
- `1` = One or more tests failed

---

#### `scripts/health_check.py` - System Validation

```bash
python scripts/health_check.py
```

**Purpose:** Comprehensive system health validation
**Duration:** ~15 seconds
**Checks performed:**

**1. Docker Environment**
- Docker installed
- Docker daemon running

**2. Container Status (9 checks)**
- All 6 containers running
- Postgres healthy
- Redis healthy
- API healthy

**3. API Gateway**
- Health endpoint responding
- All endpoints (5) accessible

**4. Database**
- Contains seed data
- Connection pool working

**5. Monitoring Stack**
- Grafana accessible at :3000
- Prometheus accessible at :9090

**6. Metrics & Monitoring**
- Prometheus scraping API
- Flask metrics available

**Output Example:**
```
╔════════════════════════════════════════════════════════════╗
║   CoreSkills4ai Command Center - System Health Check      ║
╚════════════════════════════════════════════════════════════╝

===============================================================
  1. Docker Environment
===============================================================
✅ PASS  Docker installed

===============================================================
  2. Container Status
===============================================================
✅ PASS  All containers running
✅ PASS  eduops-postgres healthy
✅ PASS  eduops-redis healthy
✅ PASS  eduops-api healthy

...

Health Check Summary
===============================================================

  Results: 15/15 checks passed (100%)

  🎉 System Status: HEALTHY
  All components operational and ready for use!
```

**Remediation Suggestions:**
- Missing containers → `python start.py`
- No seed data → `python scripts/seed_database.py`
- No metrics → `python test_api.py` (generates traffic)

---

#### `scripts/demo.py` - Automated Demonstration

```bash
python scripts/demo.py
```

**Purpose:** 5-minute instructor demonstration of full workflow
**Duration:** ~5 minutes
**Interactive:** Waits for ENTER key to start

**Demo Sequence:**

**Step 1: Create Students (30s)**
- Creates 3 demo students via POST requests
- Shows job IDs returned by API
- Demonstrates REST API usage

**Step 2: Monitor Jobs (60-120s)**
- Polls job status every 3 seconds
- Shows Redis queue processing
- Displays when PowerShell worker completes jobs
- May take time depending on worker performance

**Step 3: Verify Database (10s)**
- Queries `/api/v1/users` endpoint
- Shows created students in database
- Displays usernames, emails, status

**Step 4: Generate Traffic (30s)**
- Sends 30 requests across 3 endpoints
- Populates Grafana with real metrics
- Demonstrates load generation

**Step 5: Show Metrics (10s)**
- Queries Prometheus for request counts
- Displays breakdown by endpoint
- Shows total request volume

**Use Cases:**
- Instructor demonstrations
- System capability showcase
- End-to-end workflow testing
- Training new team members

---

## 🔧 Technology Stack

### Core Infrastructure

#### Docker (Required)
**What it is:** Container orchestration platform
**Why we use it:** Consistent environments across all VMs
**Version:** 20.10+ recommended
**Download:** https://www.docker.com/products/docker-desktop

**Containers in use:**
- `eduops-postgres` - PostgreSQL 15 (Alpine Linux)
- `eduops-redis` - Redis 7 (Alpine Linux)
- `eduops-api` - Python 3.12 Flask application
- `eduops-automation` - PowerShell 7.4 (Alpine Linux)
- `eduops-grafana` - Grafana latest
- `eduops-prometheus` - Prometheus latest

---

### Backend Services

#### PostgreSQL (Database)
**What it is:** Open-source relational database
**Port:** 5432
**Default Credentials:** `eduops_user` / `changeme123` (in `.env`)
**Learn more:** https://www.postgresql.org/docs/

**Tables:**
- `users` - Students and staff accounts
- `devices` - Managed devices and compliance status
- `policies` - Compliance and security policies
- `audit_logs` - Activity tracking
- `jobs` - Async job queue records

**How to connect:**
```bash
# From host machine
psql -h localhost -U eduops_user -d eduops

# From Docker
docker exec -it eduops-postgres psql -U eduops_user -d eduops
```

**Common queries:**
```sql
-- Count students
SELECT COUNT(*) FROM users WHERE user_type = 'student';

-- Show recent jobs
SELECT * FROM jobs ORDER BY created_at DESC LIMIT 5;

-- Device compliance status
SELECT compliance_status, COUNT(*)
FROM devices
GROUP BY compliance_status;
```

---

#### Redis (Job Queue)
**What it is:** In-memory data store for caching and queuing
**Port:** 6379
**Learn more:** https://redis.io/docs/

**Why Redis:**
- ✅ Fast in-memory operations
- ✅ Simple pub/sub for job queue
- ✅ Persistence with AOF (Append-Only File)
- ✅ No complex setup needed

**How to interact:**
```bash
# Connect to Redis CLI
docker exec -it eduops-redis redis-cli

# Check queue length
LLEN job_queue

# Peek at queued jobs
LRANGE job_queue 0 -1

# Get job details
GET job_1737785123.456
```

**Job Queue Pattern:**
1. API pushes job ID to `job_queue` list
2. API stores job data with `job_{timestamp}` key
3. Worker pops from queue with `LPOP job_queue`
4. Worker processes and updates job key
5. Client polls job key for status

---

#### Flask (API Gateway)
**What it is:** Python web framework for REST APIs
**Port:** 5000
**Learn more:** https://flask.palletsprojects.com/

**Key Features:**
- ✅ Connection pooling (5-20 connections)
- ✅ CORS enabled for cross-origin requests
- ✅ Prometheus metrics integration
- ✅ Health checks with DB/Redis validation

**Endpoints:**
- `GET /health` - System health status
- `GET /api/v1/users` - List all users
- `POST /api/v1/users/student` - Create student (async)
- `GET /api/v1/jobs/{id}` - Check job status
- `GET /api/v1/devices` - List devices
- `GET /metrics` - Prometheus metrics

**Example requests:**
```bash
# Health check
curl http://localhost:5000/health

# Create student
curl -X POST http://localhost:5000/api/v1/users/student \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "S2026999",
    "first_name": "Test",
    "last_name": "User",
    "grade_level": 11,
    "graduation_year": 2027
  }'

# Check job status
curl http://localhost:5000/api/v1/jobs/job_1737785123.456
```

---

#### PowerShell (Automation Engine)
**What it is:** Task automation and configuration management framework
**Version:** PowerShell 7.4 (cross-platform)
**Learn more:** https://docs.microsoft.com/en-us/powershell/

**Custom Module:** `KISDIdentity.psm1`

**Functions:**
- `New-KISDStudentAccount` - Create student with username generation
- `New-KISDStaffAccount` - Create staff account
- `Remove-KISDAccount` - Deactivate account
- `Test-KISDAccountExists` - Check if account exists
- `Write-KISDAuditLog` - Log administrative actions

**Worker Pattern:**
```powershell
# Worker polls Redis queue
while ($true) {
    $jobKey = redis-cli LPOP job_queue
    if ($jobKey) {
        $jobData = redis-cli GET $jobKey | ConvertFrom-Json
        # Process job with KISDIdentity module
        $result = New-KISDStudentAccount @jobData.data
        # Update job status
        redis-cli SET $jobKey $updatedJob
    }
    Start-Sleep -Seconds 2
}
```

---

### Monitoring & Observability

#### Grafana (Dashboard)
**What it is:** Open-source analytics and monitoring visualization
**Port:** 3000
**Default Login:** `admin` / `admin` (prompts to change on first login)
**Learn more:** https://grafana.com/docs/

**Dashboard:** "CoreSkills4ai Command Center"

**Panels (8 total):**
1. **System Health** - All services UP/DOWN status (line graph)
2. **PostgreSQL Status** - Database health (gauge)
3. **Redis Status** - Queue health (gauge)
4. **API Gateway Status** - API health (gauge)
5. **API Request Rate** - Requests per second (timeseries)
6. **API Response Time** - Latency in seconds (timeseries with mean/max)
7. **API Error Rate** - 5xx errors as percentage (gauge with thresholds)
8. **HTTP Status Codes** - Distribution of 2xx/4xx/5xx (pie chart)

**How to access:**
```
URL: http://localhost:3000
Username: admin
Password: admin

Navigate to: Dashboards → CoreSkills4ai Command Center
```

**Features:**
- ✅ Auto-refresh every 5 seconds
- ✅ 15-minute time window
- ✅ Real-time metric visualization
- ✅ Drill-down into specific endpoints
- ✅ Threshold-based color coding

**Customization:**
- Edit dashboard by clicking gear icon (⚙️)
- Add new panels with "+ Add Panel"
- Change time range with picker (top right)
- Export dashboard as JSON

---

#### Prometheus (Metrics)
**What it is:** Time-series database for metrics collection
**Port:** 9090
**Learn more:** https://prometheus.io/docs/

**What it collects:**
- API request counts by endpoint
- Response times (histogram buckets)
- Error rates by status code
- Container health status
- Python runtime metrics (GC, memory, threads)

**Scrape Configuration:**
- **Interval:** 15 seconds
- **Targets:**
  - `eduops-api:5000/metrics` (Flask metrics)
  - `eduops-postgres:5432` (health only)
  - `eduops-redis:6379` (health only)

**How to query:**
```
URL: http://localhost:9090

Example queries:
- flask_http_request_total              # Total requests
- rate(flask_http_request_total[1m])    # Requests per second
- flask_http_request_duration_seconds   # Latency histogram
- up{job="api-gateway"}                 # API health (1=up, 0=down)
```

**Useful Pages:**
- `/` - Home and query builder
- `/targets` - Scrape target status
- `/graph` - Graph metrics over time
- `/alerts` - Alert rules (if configured)

---

## 📊 API Documentation

### Base URL
```
http://localhost:5000
```

### Authentication
None (classroom sandbox environment)

---

### Endpoints

#### 1. Health Check

```http
GET /health
```

**Purpose:** Verify API, database, and Redis connectivity

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-15T12:00:00.000000",
  "service": "api-gateway",
  "database": "connected",
  "redis": "connected"
}
```

**Response (503 Service Unavailable):**
```json
{
  "status": "unhealthy",
  "timestamp": "2026-01-15T12:00:00.000000",
  "service": "api-gateway",
  "error": "Database connection failed"
}
```

---

#### 2. List Users

```http
GET /api/v1/users
```

**Purpose:** Retrieve all users (students and staff)

**Response (200 OK):**
```json
{
  "users": [
    {
      "id": 1,
      "type": "student",
      "first_name": "Emma",
      "last_name": "Johnson",
      "email": "ejohnson0001@students.keller.edu",
      "username": "ejohnson0001",
      "is_active": true
    }
  ]
}
```

---

#### 3. Create Student

```http
POST /api/v1/users/student
Content-Type: application/json
```

**Purpose:** Queue student creation job (async)

**Request Body:**
```json
{
  "student_id": "S2026999",
  "first_name": "John",
  "last_name": "Doe",
  "grade_level": 11,
  "graduation_year": 2027
}
```

**Validation:**
- `student_id`: Required, string
- `first_name`: Required, string
- `last_name`: Required, string
- `grade_level`: Required, integer (9-12)
- `graduation_year`: Required, integer

**Response (202 Accepted):**
```json
{
  "job_id": "job_1737785123.456",
  "status": "queued"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Missing fields: ['student_id', 'first_name', ...]"
}
```

---

#### 4. Get Job Status

```http
GET /api/v1/jobs/{job_id}
```

**Purpose:** Check async job status

**Response (200 OK - Queued):**
```json
{
  "type": "create_student",
  "status": "queued",
  "data": { ... },
  "created_at": "2026-01-15T12:00:00.000000"
}
```

**Response (200 OK - Completed):**
```json
{
  "type": "create_student",
  "status": "completed",
  "result": {
    "StudentID": "S2026999",
    "Username": "jdoe6999",
    "Email": "jdoe6999@students.keller.edu",
    "Created": "2026-01-15T12:00:15"
  },
  "created_at": "2026-01-15T12:00:00.000000"
}
```

**Response (404 Not Found):**
```json
{
  "error": "Job not found"
}
```

**Polling Pattern:**
```python
import time

job_id = response.json()['job_id']
for _ in range(10):  # Max 10 attempts
    status = requests.get(f'/api/v1/jobs/{job_id}').json()
    if status['status'] == 'completed':
        print("Job done:", status['result'])
        break
    time.sleep(3)  # Poll every 3 seconds
```

---

#### 5. List Devices

```http
GET /api/v1/devices
```

**Purpose:** Retrieve all managed devices

**Response (200 OK):**
```json
{
  "devices": [
    {
      "id": 1,
      "device_id": "WIN-LAB-001",
      "device_name": "Lab Computer 1",
      "device_type": "Windows Workstation",
      "compliance_status": "compliant"
    }
  ]
}
```

---

#### 6. Prometheus Metrics

```http
GET /metrics
```

**Purpose:** Export metrics for Prometheus scraping

**Response (200 OK):**
```
# HELP flask_http_request_total Total HTTP requests
# TYPE flask_http_request_total counter
flask_http_request_total{method="GET",path="/health",status="200"} 42.0

# HELP flask_http_request_duration_seconds HTTP request latency
# TYPE flask_http_request_duration_seconds histogram
flask_http_request_duration_seconds_sum 1.234
flask_http_request_duration_seconds_count 42
...
```

---

## 🔍 Monitoring & Metrics

### Accessing Dashboards

**Grafana:**
```
URL: http://localhost:3000
Username: admin
Password: admin
Dashboard: "CoreSkills4ai Command Center"
```

**Prometheus:**
```
URL: http://localhost:9090
No authentication
Query Builder: Available on homepage
```

### Key Metrics to Monitor

**1. Request Rate**
- **Metric:** `rate(flask_http_request_total[1m])`
- **Good:** 0-10 req/sec (classroom use)
- **Warning:** >20 req/sec (may indicate issues)

**2. Response Time**
- **Metric:** `flask_http_request_duration_seconds`
- **Good:** <100ms average
- **Warning:** >500ms (investigate slow endpoints)
- **Critical:** >1s (performance degradation)

**3. Error Rate**
- **Metric:** `rate(flask_http_request_total{status=~"5.."}[5m])`
- **Good:** 0%
- **Warning:** >1%
- **Critical:** >5%

**4. Container Health**
- **Metric:** `up{job="api-gateway"}`
- **Good:** 1 (up)
- **Critical:** 0 (down)

### Alert Thresholds (Informational)

| Metric | Warning | Critical |
|--------|---------|----------|
| API Response Time | >500ms | >1s |
| Error Rate | >1% | >5% |
| Request Rate | >20 req/s | >50 req/s |
| Container Down | N/A | Any container |

---

## ❓ Troubleshooting

### Common Issues & Solutions

#### 1. "Docker daemon not running"

**Symptoms:** `start.py` fails with connection error

**Solution:**
```bash
# Windows/Mac
Open Docker Desktop application

# Linux
sudo systemctl start docker
sudo systemctl status docker
```

---

#### 2. "Port already in use"

**Symptoms:** Container fails to start, port conflict error

**Ports used:** 5000, 5432, 6379, 3000, 9090

**Solution:**
```bash
# Find what's using port 5000
netstat -ano | findstr :5000          # Windows
lsof -i :5000                        # Mac/Linux

# Kill process or change .env ports
```

---

#### 3. "Container unhealthy / keeps restarting"

**Symptoms:** `docker ps` shows container restarting

**Solution:**
```bash
# Check logs
docker logs eduops-api
docker logs eduops-postgres

# Restart specific container
docker restart eduops-api

# Nuclear option: full rebuild
python stop.py
docker system prune -f
python start.py
```

---

#### 4. "No seed data in database"

**Symptoms:** `health_check.py` fails, empty user list

**Solution:**
```bash
# Run seeder
python scripts/seed_database.py

# If fails, check database connection
docker exec -it eduops-postgres psql -U eduops_user -d eduops -c "SELECT COUNT(*) FROM users;"
```

---

#### 5. "Grafana dashboard not showing metrics"

**Symptoms:** Panels show "No Data"

**Solution:**
```bash
# 1. Generate traffic
python test_api.py

# 2. Check Prometheus targets
# Visit: http://localhost:9090/targets
# Verify api-gateway target is UP

# 3. Wait 15-30 seconds for scrape
# Prometheus scrapes every 15 seconds
```

---

#### 6. "PowerShell worker not processing jobs"

**Symptoms:** Jobs stuck in "queued" status

**Solution:**
```bash
# Check worker logs
docker logs eduops-automation

# Restart worker
docker restart eduops-automation

# Manually test module
docker exec eduops-automation pwsh -Command "Import-Module /automation/modules/KISDIdentity.psm1; Get-Command -Module KISDIdentity"
```

---

#### 7. "Connection pool exhausted"

**Symptoms:** API returns 500 errors, logs show "too many connections"

**Solution:**
```bash
# Check pool settings in docker/api-gateway/app.py
# Default: min=5, max=20

# Restart API to reset pool
docker restart eduops-api
```

---

### Debug Commands

```bash
# View all container logs
docker-compose logs -f

# View specific container logs
docker logs -f eduops-api

# Enter container shell
docker exec -it eduops-api /bin/sh

# Check container resource usage
docker stats

# Full system reset
python stop.py
docker system prune -af --volumes  # ⚠️ DELETES ALL DATA
python start.py
python scripts/seed_database.py
```

---

## 🎓 Advanced Usage

### Custom Data

Edit JSON files in `scripts/sample_data/`:
- `students.json` - Add/modify students
- `devices.json` - Add/modify devices
- `policies.json` - Add/modify policies

Then run: `python scripts/seed_database.py`

---

### Environment Customization

Edit `.env` file:
```bash
# Database
POSTGRES_DB=eduops
POSTGRES_USER=eduops_user
POSTGRES_PASSWORD=your_secure_password

# API
API_PORT=5000

# Grafana
GF_SECURITY_ADMIN_PASSWORD=your_admin_password
```

After changes: `python stop.py && python start.py`

---

### Adding New API Endpoints

1. Edit `docker/api-gateway/app.py`
2. Add route with proper error handling
3. Use connection pooling pattern
4. Rebuild container: `docker-compose up -d --build api-gateway`

---

### Performance Testing

```bash
# Install Apache Bench
apt-get install apache2-utils  # Linux
brew install ab                # Mac

# Load test (100 requests, 10 concurrent)
ab -n 100 -c 10 http://localhost:5000/health

# Watch metrics in Grafana during test
```

---

## 📞 Support & Resources

### Official Documentation

- **Docker:** https://docs.docker.com/
- **Flask:** https://flask.palletsprojects.com/
- **PostgreSQL:** https://www.postgresql.org/docs/
- **Redis:** https://redis.io/docs/
- **PowerShell:** https://docs.microsoft.com/en-us/powershell/
- **Grafana:** https://grafana.com/docs/
- **Prometheus:** https://prometheus.io/docs/

### Repository

- **GitHub:** https://github.com/FlyguyTestRun/Class-Room-Modules
- **Issues:** https://github.com/FlyguyTestRun/Class-Room-Modules/issues

### Additional Files

- `BUILD_LOG.md` - Development history and technical notes
- `SESSION_3_PLAN.md` - Future enhancement roadmap
- `RECOMMENDATIONS.md` - Development priorities
- `DEMO.md` - Quick demo script (legacy)

---

## 📄 License

Educational use only. Not licensed for commercial deployment.

---

## 🙏 Acknowledgments

Built for CoreSkills4ai training platform.
Powered by open-source technologies.

---

**Last Updated:** 2026-01-15
**Version:** 2.0 (Session 2 Complete)
