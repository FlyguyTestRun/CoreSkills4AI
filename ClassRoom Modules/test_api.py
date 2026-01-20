#!/usr/bin/env python3
"""
CoreSkills4ai Command Center - API Test Script
Tests all API endpoints with sample data
"""
import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"

def print_section(title):
    """Print formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def test_health():
    """Test health endpoint"""
    print_section("1. Testing Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_users():
    """Test getting all users"""
    print_section("2. Testing GET Users")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/users", timeout=5)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Found {len(data.get('users', []))} users")
        if data.get('users'):
            print(f"Sample: {json.dumps(data['users'][0], indent=2)}")
        else:
            print("No users in database")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_create_student():
    """Test creating a student"""
    print_section("3. Testing POST Create Student")

    student_data = {
        "student_id": "S2026001",
        "first_name": "Test",
        "last_name": "Student",
        "grade_level": 11,
        "graduation_year": 2027
    }

    try:
        print(f"Sending: {json.dumps(student_data, indent=2)}")
        response = requests.post(
            f"{BASE_URL}/api/v1/users/student",
            json=student_data,
            timeout=5
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")

        if response.status_code == 202:
            job_id = result.get('job_id')
            print(f"\n✅ Job queued: {job_id}")
            return job_id
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_job_status(job_id):
    """Test getting job status"""
    print_section(f"4. Testing GET Job Status: {job_id}")

    try:
        # Poll job status a few times
        for i in range(5):
            response = requests.get(f"{BASE_URL}/api/v1/jobs/{job_id}", timeout=5)
            print(f"\nAttempt {i+1}:")
            print(f"Status Code: {response.status_code}")
            data = response.json()
            print(f"Job Status: {data.get('status')}")

            if data.get('status') == 'completed':
                print(f"✅ Job completed!")
                print(f"Result: {json.dumps(data.get('result'), indent=2)}")
                return True

            if i < 4:
                print(f"Waiting 3 seconds...")
                time.sleep(3)

        print("⚠️  Job still processing after 15 seconds")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_devices():
    """Test getting all devices"""
    print_section("5. Testing GET Devices")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/devices", timeout=5)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Found {len(data.get('devices', []))} devices")
        if data.get('devices'):
            print(f"Sample: {json.dumps(data['devices'][0], indent=2)}")
        else:
            print("No devices in database")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_metrics():
    """Test Prometheus metrics endpoint"""
    print_section("6. Testing Metrics Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/metrics", timeout=5)
        print(f"Status Code: {response.status_code}")

        # Count metrics
        lines = response.text.split('\n')
        metric_lines = [l for l in lines if not l.startswith('#') and l.strip()]
        print(f"Found {len(metric_lines)} metric data points")

        # Show sample Flask metrics
        print("\nSample Flask metrics:")
        for line in lines[:20]:
            if 'flask' in line.lower():
                print(f"  {line}")

        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   CoreSkills4ai Command Center - API Test Suite          ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    results = {
        "Health Check": False,
        "Get Users": False,
        "Create Student": False,
        "Job Status": False,
        "Get Devices": False,
        "Metrics": False
    }

    # Run tests
    results["Health Check"] = test_health()
    results["Get Users"] = test_get_users()

    job_id = test_create_student()
    results["Create Student"] = job_id is not None

    if job_id:
        results["Job Status"] = test_job_status(job_id)

    results["Get Devices"] = test_get_devices()
    results["Metrics"] = test_metrics()

    # Print summary
    print_section("Test Summary")
    passed = sum(results.values())
    total = len(results)

    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}  {test}")

    print(f"\n{'='*60}")
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print('='*60 + "\n")

    if passed == total:
        print("🎉 All tests passed! System is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        exit(1)
