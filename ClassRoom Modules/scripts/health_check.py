#!/usr/bin/env python3
"""
CoreSkills4ai Command Center - Health Check Script

Comprehensive system validation:
- Docker containers running and healthy
- API endpoints responding correctly
- Database connectivity and seed data
- Redis queue operational
- Grafana and Prometheus accessible
- Metrics flowing correctly

Run this after starting the system to verify everything works.
"""
import subprocess
import requests
import json
import sys
import time
from datetime import datetime

def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print('='*70)

def print_check(name, passed, message=""):
    """Print check result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status}  {name}")
    if message:
        print(f"       {message}")
    return passed

def check_docker_installed():
    """Check if Docker is installed"""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False

def check_containers_running():
    """Check if all required containers are running"""
    required_containers = [
        "eduops-postgres",
        "eduops-redis",
        "eduops-api",
        "eduops-automation",
        "eduops-grafana",
        "eduops-prometheus"
    ]

    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            return False, []

        running_containers = result.stdout.strip().split('\n')
        missing = [c for c in required_containers if c not in running_containers]

        return len(missing) == 0, missing

    except Exception as e:
        return False, []

def check_container_health(container_name):
    """Check if a specific container is healthy"""
    try:
        result = subprocess.run(
            ["docker", "inspect", "--format", "{{.State.Health.Status}}", container_name],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            health = result.stdout.strip()
            # Some containers don't have health checks
            return health in ["healthy", ""]

        return False
    except Exception:
        return False

def check_api_health():
    """Check API health endpoint"""
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return (
                data.get('status') == 'healthy' and
                data.get('database') == 'connected' and
                data.get('redis') == 'connected'
            ), data
        return False, None
    except Exception as e:
        return False, None

def check_api_endpoints():
    """Check all API endpoints"""
    endpoints = {
        "GET /api/v1/users": "http://localhost:5000/api/v1/users",
        "GET /api/v1/devices": "http://localhost:5000/api/v1/devices",
        "GET /metrics": "http://localhost:5000/metrics"
    }

    results = {}
    for name, url in endpoints.items():
        try:
            response = requests.get(url, timeout=5)
            results[name] = response.status_code == 200
        except Exception:
            results[name] = False

    return all(results.values()), results

def check_database_seeded():
    """Check if database has seed data"""
    try:
        response = requests.get("http://localhost:5000/api/v1/users", timeout=5)
        if response.status_code == 200:
            data = response.json()
            user_count = len(data.get('users', []))
            return user_count > 0, user_count
        return False, 0
    except Exception:
        return False, 0

def check_grafana():
    """Check if Grafana is accessible"""
    try:
        response = requests.get("http://localhost:3000/api/health", timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def check_prometheus():
    """Check if Prometheus is accessible"""
    try:
        response = requests.get("http://localhost:9090/-/healthy", timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def check_prometheus_targets():
    """Check if Prometheus is scraping targets"""
    try:
        response = requests.get("http://localhost:9090/api/v1/targets", timeout=5)
        if response.status_code == 200:
            data = response.json()
            active_targets = data.get('data', {}).get('activeTargets', [])
            api_target = [t for t in active_targets if t.get('labels', {}).get('job') == 'api-gateway']
            return len(api_target) > 0 and api_target[0].get('health') == 'up', active_targets
        return False, []
    except Exception:
        return False, []

def check_metrics_flowing():
    """Check if metrics are being collected"""
    try:
        response = requests.get(
            "http://localhost:9090/api/v1/query?query=flask_http_request_total",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            results = data.get('data', {}).get('result', [])
            return len(results) > 0, results
        return False, []
    except Exception:
        return False, []

def main():
    """Run all health checks"""
    print("""
    ╔════════════════════════════════════════════════════════════════════╗
    ║   CoreSkills4ai Command Center - System Health Check              ║
    ║   Validating all components and services                          ║
    ╚════════════════════════════════════════════════════════════════════╝
    """)

    checks_passed = 0
    checks_total = 0
    failed_checks = []

    # 1. Docker Installation
    print_header("1. Docker Environment")
    checks_total += 1
    if print_check("Docker installed", check_docker_installed()):
        checks_passed += 1
    else:
        failed_checks.append("Docker not installed or not in PATH")

    # 2. Container Status
    print_header("2. Container Status")
    checks_total += 1
    running, missing = check_containers_running()
    if print_check("All containers running", running):
        checks_passed += 1
        # Check individual health
        for container in ["eduops-postgres", "eduops-redis", "eduops-api"]:
            checks_total += 1
            healthy = check_container_health(container)
            if print_check(f"{container} healthy", healthy):
                checks_passed += 1
            else:
                failed_checks.append(f"{container} not healthy")
    else:
        failed_checks.append(f"Missing containers: {', '.join(missing)}")

    # 3. API Health
    print_header("3. API Gateway")
    checks_total += 1
    healthy, data = check_api_health()
    if print_check("API health endpoint", healthy):
        checks_passed += 1
        if data:
            print(f"       Status: {data.get('status')}")
            print(f"       Database: {data.get('database')}")
            print(f"       Redis: {data.get('redis')}")
    else:
        failed_checks.append("API health check failed")

    # 4. API Endpoints
    checks_total += 1
    all_ok, endpoint_results = check_api_endpoints()
    if print_check("All API endpoints responding", all_ok):
        checks_passed += 1
        for endpoint, status in endpoint_results.items():
            icon = "✓" if status else "✗"
            print(f"       {icon} {endpoint}")
    else:
        failed_endpoints = [e for e, s in endpoint_results.items() if not s]
        failed_checks.append(f"Failed endpoints: {', '.join(failed_endpoints)}")

    # 5. Database Seed Data
    print_header("4. Database")
    checks_total += 1
    seeded, count = check_database_seeded()
    if print_check("Database has seed data", seeded, f"{count} users found"):
        checks_passed += 1
    else:
        failed_checks.append("No seed data in database - run: python scripts/seed_database.py")

    # 6. Monitoring Stack
    print_header("5. Monitoring Stack")
    checks_total += 1
    if print_check("Grafana accessible", check_grafana(), "http://localhost:3000"):
        checks_passed += 1
    else:
        failed_checks.append("Grafana not accessible")

    checks_total += 1
    if print_check("Prometheus accessible", check_prometheus(), "http://localhost:9090"):
        checks_passed += 1
    else:
        failed_checks.append("Prometheus not accessible")

    # 7. Metrics Collection
    print_header("6. Metrics & Monitoring")
    checks_total += 1
    targets_ok, targets = check_prometheus_targets()
    if print_check("Prometheus scraping API", targets_ok):
        checks_passed += 1
    else:
        failed_checks.append("Prometheus not scraping API gateway")

    checks_total += 1
    metrics_ok, metrics = check_metrics_flowing()
    if print_check("Flask metrics available", metrics_ok, f"{len(metrics)} metric series"):
        checks_passed += 1
    else:
        failed_checks.append("Flask metrics not found - generate traffic first")

    # Summary
    print_header("Health Check Summary")
    percentage = (checks_passed / checks_total * 100) if checks_total > 0 else 0

    print(f"\n  Results: {checks_passed}/{checks_total} checks passed ({percentage:.0f}%)")

    if checks_passed == checks_total:
        print("\n  🎉 System Status: HEALTHY")
        print("  All components operational and ready for use!")
    elif percentage >= 80:
        print("\n  ⚠️  System Status: DEGRADED")
        print("  Most components working, but some issues detected.")
    else:
        print("\n  ❌ System Status: UNHEALTHY")
        print("  Critical issues detected. System may not function correctly.")

    # Failed checks
    if failed_checks:
        print("\n  ⚠️  Issues Found:")
        for i, issue in enumerate(failed_checks, 1):
            print(f"     {i}. {issue}")

    # Remediation
    print("\n  💡 Quick Fixes:")
    if not running:
        print("     → Run: python start.py")
    if not seeded:
        print("     → Run: python scripts/seed_database.py")
    if not metrics_ok:
        print("     → Generate traffic: python test_api.py")

    print("\n" + "="*70)
    print(f"  Health check completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")

    return checks_passed == checks_total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Health check interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error during health check: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
