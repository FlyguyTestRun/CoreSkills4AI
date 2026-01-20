#!/usr/bin/env python3
"""
CoreSkills4ai Command Center - Quick Start Script
Activates venv, installs dependencies, and starts all services
"""
import subprocess
import sys
import os
import time
from pathlib import Path

def run_command(cmd, description, shell=True, check=True):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"⚙️  {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=shell, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(e.stderr)
        if check:
            sys.exit(1)
        return e

def check_docker():
    """Verify Docker is running"""
    print("\n🔍 Checking Docker...")
    result = run_command("docker --version", "Checking Docker installation", check=False)
    if result.returncode != 0:
        print("❌ Docker not found. Please install Docker Desktop first.")
        sys.exit(1)

    result = run_command("docker ps", "Checking Docker daemon", check=False)
    if result.returncode != 0:
        print("❌ Docker daemon not running. Please start Docker Desktop.")
        sys.exit(1)

    print("✅ Docker is ready")

def check_env_file():
    """Check if .env file exists"""
    if not Path(".env").exists():
        print("\n⚠️  .env file not found. Creating from template...")
        if Path(".env.template").exists():
            import shutil
            shutil.copy(".env.template", ".env")
            print("✅ Created .env from template")
            print("💡 You can customize credentials in .env if needed")
        else:
            print("❌ .env.template not found. Cannot create .env file.")
            sys.exit(1)
    else:
        print("✅ .env file exists")

def main():
    """Main startup sequence"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   CoreSkills4ai Command Center - Startup Script          ║
    ║   Starting Docker containers and monitoring stack        ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    # Step 1: Check prerequisites
    check_docker()
    check_env_file()

    # Step 2: Stop any existing containers
    print("\n🛑 Stopping any existing containers...")
    run_command("docker-compose down", "Stopping services", check=False)

    # Step 3: Build and start main services
    run_command(
        "docker-compose up -d --build",
        "Building and starting core services (postgres, redis, api, automation)"
    )

    # Step 4: Wait for services to be healthy
    print("\n⏳ Waiting for services to be healthy...")
    time.sleep(10)

    # Step 5: Start monitoring stack
    print("\n📊 Starting monitoring stack...")
    run_command(
        "docker-compose -f docker/monitoring/docker-compose.monitoring.yml up -d",
        "Starting Grafana and Prometheus"
    )

    # Step 6: Wait for monitoring to start
    time.sleep(5)

    # Step 7: Show container status
    print("\n" + "="*60)
    print("📦 Container Status:")
    print("="*60)
    run_command("docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'", "")

    # Step 8: Test API health
    print("\n" + "="*60)
    print("🏥 Testing API Health:")
    print("="*60)
    time.sleep(5)  # Give API a moment to fully start
    result = run_command(
        'curl -s http://localhost:5000/health | python -m json.tool',
        "API Health Check",
        check=False
    )

    # Step 9: Display access information
    print("\n" + "="*60)
    print("✅ Startup Complete!")
    print("="*60)
    print("\n📍 Access URLs:")
    print("   API Gateway:    http://localhost:5000")
    print("   API Health:     http://localhost:5000/health")
    print("   API Metrics:    http://localhost:5000/metrics")
    print("   Grafana:        http://localhost:3000 (admin/admin)")
    print("   Prometheus:     http://localhost:9090")
    print("\n📖 Quick Commands:")
    print("   View logs:      docker-compose logs -f")
    print("   Stop all:       docker-compose down && docker-compose -f docker/monitoring/docker-compose.monitoring.yml down")
    print("   Restart API:    docker restart eduops-api")
    print("\n💡 Pro Tip: Open Grafana and navigate to 'CoreSkills4ai Command Center' dashboard")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Startup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
