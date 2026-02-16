#!/usr/bin/env python3
"""
CoreSkills4ai Command Center - Database Seeding Script

Loads sample data into PostgreSQL database:
- 20 students (grades 9-12)
- 12 devices (Windows, Mac, Chromebook, iPad)
- 7 compliance policies

Run this after starting containers to populate the database with realistic test data.
"""
import psycopg2
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Database connection parameters
DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'database': os.getenv('POSTGRES_DB', 'eduops'),
    'user': os.getenv('POSTGRES_USER', 'eduops_user'),
    'password': os.getenv('POSTGRES_PASSWORD', 'changeme123'),
    'port': 5432
}

def print_section(title):
    """Print formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def load_json_file(filepath):
    """Load data from JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {filepath}: {e}")
        return []

def connect_db():
    """Connect to PostgreSQL database"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Connected to database")
        return conn
    except psycopg2.Error as e:
        print(f"❌ Database connection failed: {e}")
        sys.exit(1)

def clear_existing_data(conn):
    """Clear existing sample data (optional - prompts user)"""
    print("\n⚠️  Clear existing data before seeding?")
    print("   This will DELETE all users, devices, and policies.")
    response = input("   Type 'yes' to confirm: ").strip().lower()

    if response != 'yes':
        print("Skipping data clear. Existing data will remain.")
        return

    try:
        cur = conn.cursor()

        # Clear tables in reverse dependency order
        cur.execute("DELETE FROM audit_logs")
        cur.execute("DELETE FROM jobs")
        cur.execute("DELETE FROM devices")
        cur.execute("DELETE FROM policies")
        cur.execute("DELETE FROM users")

        conn.commit()
        cur.close()
        print("✅ Existing data cleared")
    except psycopg2.Error as e:
        print(f"❌ Error clearing data: {e}")
        conn.rollback()

def seed_students(conn, students_data):
    """Insert student records into users table"""
    print_section("Seeding Students")

    if not students_data:
        print("⚠️  No student data to seed")
        return 0

    try:
        cur = conn.cursor()
        count = 0

        for student in students_data:
            # Generate username and email
            username = f"{student['first_name'][0].lower()}{student['last_name'].lower()}{student['student_id'][-4:]}"
            email = f"{username}@students.keller.edu"

            cur.execute("""
                INSERT INTO users (
                    user_type, student_id, first_name, last_name,
                    email, username, grade_level, graduation_year, is_active
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (student_id) DO NOTHING
            """, (
                'student',
                student['student_id'],
                student['first_name'],
                student['last_name'],
                email,
                username,
                student['grade_level'],
                student['graduation_year'],
                True
            ))

            if cur.rowcount > 0:
                count += 1
                print(f"  ✓ {student['first_name']} {student['last_name']} ({username})")

        conn.commit()
        cur.close()
        print(f"\n✅ Seeded {count} students")
        return count

    except psycopg2.Error as e:
        print(f"❌ Error seeding students: {e}")
        conn.rollback()
        return 0

def seed_devices(conn, devices_data):
    """Insert device records into devices table"""
    print_section("Seeding Devices")

    if not devices_data:
        print("⚠️  No device data to seed")
        return 0

    try:
        cur = conn.cursor()
        count = 0

        for device in devices_data:
            # Get user_id if device is assigned
            user_id = None
            if device.get('assigned_to'):
                cur.execute("SELECT id FROM users WHERE student_id = %s", (device['assigned_to'],))
                result = cur.fetchone()
                if result:
                    user_id = result[0]

            cur.execute("""
                INSERT INTO devices (
                    device_id, device_name, device_type,
                    assigned_to_user_id, compliance_status, last_check_in
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (device_id) DO NOTHING
            """, (
                device['device_id'],
                device['device_name'],
                device['device_type'],
                user_id,
                device['compliance_status'],
                datetime.utcnow()
            ))

            if cur.rowcount > 0:
                count += 1
                status_icon = "✓" if device['compliance_status'] == 'compliant' else "⚠"
                print(f"  {status_icon} {device['device_name']} ({device['device_id']})")

        conn.commit()
        cur.close()
        print(f"\n✅ Seeded {count} devices")
        return count

    except psycopg2.Error as e:
        print(f"❌ Error seeding devices: {e}")
        conn.rollback()
        return 0

def seed_policies(conn, policies_data):
    """Insert policy records into policies table"""
    print_section("Seeding Policies")

    if not policies_data:
        print("⚠️  No policy data to seed")
        return 0

    try:
        cur = conn.cursor()
        count = 0

        for policy in policies_data:
            cur.execute("""
                INSERT INTO policies (
                    policy_name, policy_type, description,
                    applies_to, enforcement_level, is_active
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                policy['policy_name'],
                policy['policy_type'],
                policy['description'],
                policy['applies_to'],
                policy['enforcement_level'],
                True
            ))

            count += 1
            enforcement_icon = "🔒" if policy['enforcement_level'] == 'required' else "💡"
            print(f"  {enforcement_icon} {policy['policy_name']} ({policy['policy_type']})")

        conn.commit()
        cur.close()
        print(f"\n✅ Seeded {count} policies")
        return count

    except psycopg2.Error as e:
        print(f"❌ Error seeding policies: {e}")
        conn.rollback()
        return 0

def verify_seeding(conn):
    """Verify data was seeded correctly"""
    print_section("Verification")

    try:
        cur = conn.cursor()

        # Count records
        cur.execute("SELECT COUNT(*) FROM users WHERE user_type = 'student'")
        student_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM devices")
        device_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM policies")
        policy_count = cur.fetchone()[0]

        cur.close()

        print(f"  📊 Students in database: {student_count}")
        print(f"  📊 Devices in database:  {device_count}")
        print(f"  📊 Policies in database: {policy_count}")

        return student_count > 0 and device_count > 0 and policy_count > 0

    except psycopg2.Error as e:
        print(f"❌ Error verifying data: {e}")
        return False

def main():
    """Main seeding sequence"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   CoreSkills4ai Command Center - Database Seeder         ║
    ║   Loading sample data for classroom demonstrations       ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    # Get script directory
    script_dir = Path(__file__).parent
    data_dir = script_dir / "sample_data"

    # Load data files
    print_section("Loading Data Files")
    students = load_json_file(data_dir / "students.json")
    devices = load_json_file(data_dir / "devices.json")
    policies = load_json_file(data_dir / "policies.json")

    print(f"  📄 Loaded {len(students)} students")
    print(f"  📄 Loaded {len(devices)} devices")
    print(f"  📄 Loaded {len(policies)} policies")

    if not students and not devices and not policies:
        print("\n❌ No data to seed. Check sample_data directory.")
        sys.exit(1)

    # Connect to database
    print_section("Database Connection")
    conn = connect_db()

    # Optional: Clear existing data
    clear_existing_data(conn)

    # Seed data
    student_count = seed_students(conn, students)
    device_count = seed_devices(conn, devices)
    policy_count = seed_policies(conn, policies)

    # Verify
    success = verify_seeding(conn)

    # Close connection
    conn.close()

    # Summary
    print("\n" + "="*60)
    if success:
        print("✅ Database Seeding Complete!")
    else:
        print("⚠️  Database Seeding Incomplete")
    print("="*60)

    print(f"\n📊 Summary:")
    print(f"   {student_count} students added")
    print(f"   {device_count} devices added")
    print(f"   {policy_count} policies added")

    print("\n💡 Next Steps:")
    print("   1. Run: python test_api.py")
    print("   2. Open Grafana: http://localhost:3000")
    print("   3. Test API: curl http://localhost:5000/api/v1/users")

    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Seeding interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
