#!/usr/bin/env python3
"""
CoreSkills4ai Command Center - Shutdown Script
Gracefully stops all services
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description, shell=True, check=True):
    """Run a command and handle errors"""
    print(f"\n⚙️  {description}")
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

def main():
    """Main shutdown sequence"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   CoreSkills4ai Command Center - Shutdown Script         ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    # Stop monitoring stack
    print("\n📊 Stopping monitoring stack...")
    run_command(
        "docker-compose -f docker/monitoring/docker-compose.monitoring.yml down",
        "Stopping Grafana and Prometheus",
        check=False
    )

    # Stop core services
    print("\n🛑 Stopping core services...")
    run_command(
        "docker-compose down",
        "Stopping API, automation, postgres, redis",
        check=False
    )

    # Show remaining containers
    print("\n" + "="*60)
    print("📦 Remaining Containers:")
    print("="*60)
    result = run_command(
        "docker ps --format 'table {{.Names}}\t{{.Status}}'",
        "",
        check=False
    )

    if "eduops" not in result.stdout:
        print("✅ All CoreSkills4ai containers stopped")
    else:
        print("⚠️  Some containers still running. Run 'docker ps' to check.")

    print("\n" + "="*60)
    print("✅ Shutdown Complete!")
    print("="*60)
    print("\n💡 To start again, run: python start.py")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Shutdown interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
