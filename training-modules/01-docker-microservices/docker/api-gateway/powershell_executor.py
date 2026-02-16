"""
PowerShell execution bridge for API Gateway
Executes PowerShell commands in automation container via Docker exec
"""
import subprocess
import json
import logging

logger = logging.getLogger(__name__)

def execute_powershell(module, function, params):
    """
    Execute PowerShell function in automation container

    Args:
        module: PowerShell module name (e.g., 'KISDIdentity')
        function: Function name (e.g., 'New-KISDStudentAccount')
        params: Dict of parameters

    Returns:
        dict: Execution result with stdout, stderr, success status
    """
    try:
        # Build PowerShell command
        param_str = ' '.join([f"-{k} '{v}'" for k, v in params.items()])
        ps_cmd = f"Import-Module /automation/modules/{module}.psm1 -Force; {function} {param_str} | ConvertTo-Json -Compress"

        # Execute via docker exec
        cmd = [
            'docker', 'exec', 'eduops-automation',
            'pwsh', '-Command', ps_cmd
        ]

        logger.info(f"Executing: {function} with params {params}")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            try:
                output = json.loads(result.stdout.strip())
            except json.JSONDecodeError:
                output = {'raw_output': result.stdout.strip()}

            return {
                'success': True,
                'output': output,
                'stderr': result.stderr
            }
        else:
            logger.error(f"PowerShell execution failed: {result.stderr}")
            return {
                'success': False,
                'error': result.stderr,
                'stdout': result.stdout
            }

    except subprocess.TimeoutExpired:
        logger.error(f"PowerShell execution timed out")
        return {
            'success': False,
            'error': 'Execution timed out after 30 seconds'
        }
    except Exception as e:
        logger.error(f"PowerShell execution exception: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

def create_student_account(student_id, first_name, last_name, grade_level, graduation_year):
    """Wrapper for New-KISDStudentAccount"""
    return execute_powershell(
        module='KISDIdentity',
        function='New-KISDStudentAccount',
        params={
            'StudentID': student_id,
            'FirstName': first_name,
            'LastName': last_name,
            'GradeLevel': grade_level,
            'GraduationYear': graduation_year
        }
    )

def create_staff_account(employee_id, first_name, last_name, department, role):
    """Wrapper for New-KISDStaffAccount"""
    return execute_powershell(
        module='KISDIdentity',
        function='New-KISDStaffAccount',
        params={
            'EmployeeID': employee_id,
            'FirstName': first_name,
            'LastName': last_name,
            'Department': department,
            'Role': role
        }
    )
