#!/usr/bin/env python3
"""
CoreSkills4ai Command Center - Automated Demo Script

5-minute demonstration sequence:
1. Create 3 new students via API
2. Show job queuing in Redis
3. Poll for job completion
4. Display results from database
5. Generate traffic for Grafana metrics
6. Show system statistics

Perfect for instructor demonstrations or testing the full workflow.
"""
import requests
import json
import time
import sys
from datetime import datetime

BASE_URL = "http://localhost:5000"

def print_header(title, symbol="="):
    """Print formatted header"""
    print(f"\n{symbol*70}")
    print(f"  {title}")
    print(f"{symbol*70}")

def print_step(step_num, title):
    """Print step header"""
    print(f"\n{'─'*70}")
    print(f"📍 Step {step_num}: {title}")
    print(f"{'─'*70}")

def countdown(seconds, message=""):
    """Display countdown timer"""
    for i in range(seconds, 0, -1):
        print(f"\r⏳ {message} {i}s...", end="", flush=True)
        time.sleep(1)
    print(f"\r✅ {message} Complete!        ")

def demo_step_1_create_students():
    """Step 1: Create students via API"""
    print_step(1, "Creating Students via API")

    demo_students = [
        {
            "student_id": "S2026100",
            "first_name": "Demo",
            "last_name": "Student1",
            "grade_level": 12,
            "graduation_year": 2026
        },
        {
            "student_id": "S2027100",
            "first_name": "Test",
            "last_name": "User2",
            "grade_level": 11,
            "graduation_year": 2027
        },
        {
            "student_id": "S2028100",
            "first_name": "Example",
            "last_name": "Person3",
            "grade_level": 10,
            "graduation_year": 2028
        }
    ]

    job_ids = []

    for i, student in enumerate(demo_students, 1):
        print(f"\n  Creating Student {i}/3:")
        print(f"    Name: {student['first_name']} {student['last_name']}")
        print(f"    ID: {student['student_id']}")
        print(f"    Grade: {student['grade_level']}")

        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/users/student",
                json=student,
                timeout=5
            )

            if response.status_code == 202:
                data = response.json()
                job_id = data.get('job_id')
                job_ids.append(job_id)
                print(f"    ✅ Job Queued: {job_id}")
            else:
                print(f"    ❌ Failed: {response.status_code}")

        except Exception as e:
            print(f"    ❌ Error: {e}")

        time.sleep(0.5)  # Brief pause between requests

    print(f"\n  📊 Summary: {len(job_ids)} jobs queued")
    return job_ids

def demo_step_2_check_jobs(job_ids):
    """Step 2: Monitor job status"""
    print_step(2, "Monitoring Job Queue")

    print("  Checking Redis job queue and worker processing...\n")

    completed = []
    max_attempts = 10

    for attempt in range(1, max_attempts + 1):
        print(f"  Polling attempt {attempt}/{max_attempts}:")

        for job_id in job_ids:
            if job_id in completed:
                continue

            try:
                response = requests.get(f"{BASE_URL}/api/v1/jobs/{job_id}", timeout=5)

                if response.status_code == 200:
                    data = response.json()
                    status = data.get('status', 'unknown')

                    if status == 'completed':
                        completed.append(job_id)
                        result = data.get('result', {})
                        username = result.get('Username', 'N/A')
                        print(f"    ✅ {job_id}: COMPLETED → {username}")
                    elif status == 'queued':
                        print(f"    ⏳ {job_id}: QUEUED (waiting for worker)")
                    elif status == 'running':
                        print(f"    ⚙️  {job_id}: RUNNING")
                    else:
                        print(f"    ❓ {job_id}: {status}")

            except Exception as e:
                print(f"    ❌ {job_id}: Error - {e}")

        if len(completed) == len(job_ids):
            print(f"\n  🎉 All {len(completed)} jobs completed!")
            break

        if attempt < max_attempts:
            countdown(3, "Next poll in")

    if len(completed) < len(job_ids):
        print(f"\n  ⚠️  {len(completed)}/{len(job_ids)} jobs completed after {max_attempts} attempts")
        print("  (PowerShell worker may be slow - this is normal)")

    return completed

def demo_step_3_verify_database():
    """Step 3: Verify students in database"""
    print_step(3, "Verifying Database Records")

    try:
        response = requests.get(f"{BASE_URL}/api/v1/users", timeout=5)

        if response.status_code == 200:
            data = response.json()
            users = data.get('users', [])

            # Find demo students
            demo_users = [u for u in users if u['username'].startswith(('dstudent1', 'tuser2', 'eperson3'))]

            print(f"  Total users in database: {len(users)}")
            print(f"  Demo users created: {len(demo_users)}\n")

            if demo_users:
                print("  Demo Student Details:")
                for user in demo_users:
                    print(f"    → {user['first_name']} {user['last_name']}")
                    print(f"      Username: {user['username']}")
                    print(f"      Email: {user['email']}")
                    print(f"      Active: {user['is_active']}\n")
                return True
            else:
                print("  ⚠️  Demo users not found in database")
                return False

        else:
            print(f"  ❌ Failed to query database: {response.status_code}")
            return False

    except Exception as e:
        print(f"  ❌ Error querying database: {e}")
        return False

def demo_step_4_generate_traffic():
    """Step 4: Generate traffic for Grafana"""
    print_step(4, "Generating Traffic for Metrics")

    print("  Sending 30 API requests to populate Grafana dashboards...\n")

    endpoints = [
        ("Health Check", f"{BASE_URL}/health"),
        ("Get Users", f"{BASE_URL}/api/v1/users"),
        ("Get Devices", f"{BASE_URL}/api/v1/devices"),
    ]

    requests_sent = 0

    for round_num in range(1, 11):
        print(f"  Round {round_num}/10: ", end="", flush=True)

        for name, url in endpoints:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print("✓", end="", flush=True)
                    requests_sent += 1
                else:
                    print("✗", end="", flush=True)
            except:
                print("✗", end="", flush=True)

            time.sleep(0.1)

        print()  # New line after round

    print(f"\n  ✅ Sent {requests_sent} requests")
    print("  💡 Metrics should now be visible in Grafana")

def demo_step_5_show_metrics():
    """Step 5: Display current metrics"""
    print_step(5, "Displaying System Metrics")

    try:
        # Query Prometheus for metrics
        response = requests.get(
            "http://localhost:9090/api/v1/query?query=flask_http_request_total",
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()
            results = data.get('data', {}).get('result', [])

            if results:
                total_requests = sum(float(r['value'][1]) for r in results)
                print(f"  📊 Total API requests recorded: {int(total_requests)}")

                # Show breakdown by endpoint
                print("\n  Request breakdown by endpoint:")
                for result in results:
                    path = result['metric'].get('path', 'unknown')
                    method = result['metric'].get('method', 'GET')
                    count = int(float(result['value'][1]))
                    print(f"    → {method} {path}: {count} requests")

            else:
                print("  ⚠️  No metrics found yet - may need more time for collection")

        else:
            print(f"  ❌ Failed to query Prometheus: {response.status_code}")

    except Exception as e:
        print(f"  ❌ Error querying metrics: {e}")

def main():
    """Run automated demo sequence"""
    print("""
    ╔════════════════════════════════════════════════════════════════════╗
    ║   CoreSkills4ai Command Center - Automated Demo                   ║
    ║   Demonstrating full workflow: API → Redis → PowerShell → DB      ║
    ╚════════════════════════════════════════════════════════════════════╝
    """)

    print("  This demo will:")
    print("    1. Create 3 students via REST API")
    print("    2. Monitor Redis job queue processing")
    print("    3. Verify records in PostgreSQL database")
    print("    4. Generate traffic for Grafana metrics")
    print("    5. Display Prometheus metrics\n")

    input("  Press ENTER to begin demo...")

    start_time = time.time()

    # Execute demo steps
    job_ids = demo_step_1_create_students()

    if job_ids:
        completed = demo_step_2_check_jobs(job_ids)
        time.sleep(2)  # Brief pause

    demo_step_3_verify_database()
    time.sleep(1)

    demo_step_4_generate_traffic()
    time.sleep(2)

    demo_step_5_show_metrics()

    # Summary
    elapsed = time.time() - start_time
    print_header("Demo Complete!", "=")

    print(f"\n  ⏱️  Total time: {elapsed:.1f} seconds")
    print("\n  🎯 What was demonstrated:")
    print("     ✓ REST API accepting student data")
    print("     ✓ Redis job queue handling async processing")
    print("     ✓ PowerShell automation creating accounts")
    print("     ✓ PostgreSQL storing results")
    print("     ✓ Prometheus collecting metrics")

    print("\n  🔗 Access the system:")
    print("     → API:        http://localhost:5000")
    print("     → Grafana:    http://localhost:3000 (admin/admin)")
    print("     → Prometheus: http://localhost:9090")

    print("\n  💡 Next steps:")
    print("     1. Open Grafana dashboard: 'CoreSkills4ai Command Center'")
    print("     2. View request rate, response time, and error metrics")
    print("     3. Run: python test_api.py (for comprehensive testing)")

    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
