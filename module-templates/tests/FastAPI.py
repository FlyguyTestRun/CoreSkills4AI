"""
==============================================================================
Unit Tests for FastAPI Application
==============================================================================
Location: tests/test_main.py
Purpose: Test API endpoints and functionality
Framework: pytest with FastAPI TestClient
==============================================================================
"""

import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch

from src.main import app, get_db_pool

# ==============================================================================
# TEST FIXTURES
# ==============================================================================

@pytest.fixture
def client():
    """
    Create a test client for the FastAPI app.
    
    This fixture provides a TestClient instance that can make
    requests to the API without running a server.
    
    Yields:
        TestClient: FastAPI test client
    
    Example:
        def test_endpoint(client):
            response = client.get("/")
            assert response.status_code == 200
    """
    return TestClient(app)


@pytest.fixture
def mock_db_pool():
    """
    Mock database connection pool.
    
    Creates a mock pool that simulates database operations
    without requiring an actual database connection.
    
    Returns:
        MagicMock: Mocked asyncpg pool
    """
    pool = MagicMock()
    
    # Mock connection context manager
    mock_conn = MagicMock()
    mock_acquire = MagicMock()
    mock_acquire.__aenter__ = AsyncMock(return_value=mock_conn)
    mock_acquire.__aexit__ = AsyncMock(return_value=None)
    pool.acquire.return_value = mock_acquire
    
    return pool


@pytest.fixture
def override_get_db_pool(mock_db_pool):
    """
    Override the database dependency with a mock.
    
    This fixture replaces the real database pool with a mock,
    allowing tests to run without a database.
    
    Args:
        mock_db_pool: Mocked database pool
    
    Yields:
        MagicMock: Mocked database pool
    """
    app.dependency_overrides[get_db_pool] = lambda: mock_db_pool
    yield mock_db_pool
    app.dependency_overrides.clear()


# ==============================================================================
# SECTION 1: ROOT ENDPOINT TESTS
# ==============================================================================

class TestRootEndpoint:
    """Tests for the root endpoint (/)"""
    
    def test_root_returns_200(self, client):
        """Test that root endpoint returns 200 OK"""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_returns_json(self, client):
        """Test that root endpoint returns JSON"""
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"
    
    def test_root_contains_message(self, client):
        """Test that root endpoint contains welcome message"""
        response = client.get("/")
        data = response.json()
        
        assert "message" in data
        assert "Professional Microservice API" in data["message"]
    
    def test_root_contains_links(self, client):
        """Test that root endpoint provides documentation links"""
        response = client.get("/")
        data = response.json()
        
        assert "docs" in data
        assert "redoc" in data
        assert "health" in data
        assert data["docs"] == "/docs"
        assert data["redoc"] == "/redoc"
        assert data["health"] == "/health"


# ==============================================================================
# SECTION 2: HEALTH CHECK TESTS
# ==============================================================================

class TestHealthEndpoint:
    """Tests for the health check endpoint"""
    
    def test_health_returns_200(self, client, override_get_db_pool):
        """Test that health endpoint returns 200 OK"""
        # Mock database check
        mock_conn = MagicMock()
        mock_conn.fetchval = AsyncMock(return_value=1)
        override_get_db_pool.acquire.return_value.__aenter__.return_value = mock_conn
        
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_response_structure(self, client, override_get_db_pool):
        """Test health response contains required fields"""
        # Mock database check
        mock_conn = MagicMock()
        mock_conn.fetchval = AsyncMock(return_value=1)
        override_get_db_pool.acquire.return_value.__aenter__.return_value = mock_conn
        
        response = client.get("/health")
        data = response.json()
        
        # Check required fields
        assert "status" in data
        assert "environment" in data
        assert "version" in data
        assert "timestamp" in data
        assert "database" in data
    
    def test_health_status_healthy(self, client, override_get_db_pool):
        """Test that health status is 'healthy' when DB is connected"""
        # Mock successful database check
        mock_conn = MagicMock()
        mock_conn.fetchval = AsyncMock(return_value=1)
        override_get_db_pool.acquire.return_value.__aenter__.return_value = mock_conn
        
        response = client.get("/health")
        data = response.json()
        
        assert data["status"] == "healthy"
        assert data["database"] == "connected"
    
    def test_health_database_disconnected(self, client, override_get_db_pool):
        """Test health check when database is unavailable"""
        # Mock database failure
        mock_conn = MagicMock()
        mock_conn.fetchval = AsyncMock(side_effect=Exception("DB Error"))
        override_get_db_pool.acquire.return_value.__aenter__.return_value = mock_conn
        
        response = client.get("/health")
        data = response.json()
        
        assert data["database"] == "disconnected"


# ==============================================================================
# SECTION 3: USER ENDPOINT TESTS
# ==============================================================================

class TestUserEndpoints:
    """Tests for user-related endpoints"""
    
    def test_list_users_returns_200(self, client, override_get_db_pool):
        """Test that GET /users returns 200 OK"""
        # Mock database response
        mock_conn = MagicMock()
        mock_conn.fetch = AsyncMock(return_value=[])
        override_get_db_pool.acquire.return_value.__aenter__.return_value = mock_conn
        
        response = client.get("/users")
        assert response.status_code == 200
    
    def test_list_users_returns_list(self, client, override_get_db_pool):
        """Test that GET /users returns a list"""
        # Mock database response
        mock_conn = MagicMock()
        mock_conn.fetch = AsyncMock(return_value=[])
        override_get_db_pool.acquire.return_value.__aenter__.return_value = mock_conn
        
        response = client.get("/users")
        data = response.json()
        
        assert isinstance(data, list)
    
    def test_list_users_with_data(self, client, override_get_db_pool):
        """Test GET /users with mock user data"""
        # Mock user data
        mock_users = [
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "username": "testuser",
                "email": "test@example.com",
                "full_name": "Test User",
                "is_active": True,
                "created_at": datetime.utcnow()
            }
        ]
        
        mock_conn = MagicMock()
        mock_conn.fetch = AsyncMock(return_value=mock_users)
        override_get_db_pool.acquire.return_value.__aenter__.return_value = mock_conn
        
        response = client.get("/users")
        data = response.json()
        
        assert len(data) == 1
        assert data[0]["username"] == "testuser"
        assert data[0]["email"] == "test@example.com"
    
    def test_list_users_pagination(self, client, override_get_db_pool):
        """Test GET /users with pagination parameters"""
        mock_conn = MagicMock()
        mock_conn.fetch = AsyncMock(return_value=[])
        override_get_db_pool.acquire.return_value.__aenter__.return_value = mock_conn
        
        response = client.get("/users?limit=5&offset=10")
        assert response.status_code == 200
    
    def test_get_user_by_id_returns_200(self, client, override_get_db_pool):
        """Test GET /users/{user_id} returns 200 OK"""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        
        # Mock user data
        mock_user = {
            "id": user_id,
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        
        mock_conn = MagicMock()
        mock_conn.fetchrow = AsyncMock(return_value=mock_user)
        override_get_db_pool.acquire.return_value.__aenter__.return_value = mock_conn
        
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
    
    def test_get_user_not_found(self, client, override_get_db_pool):
        """Test GET /users/{user_id} returns 404 when user doesn't exist"""
        user_id = "nonexistent-id"
        
        # Mock no user found
        mock_conn = MagicMock()
        mock_conn.fetchrow = AsyncMock(return_value=None)
        override_get_db_pool.acquire.return_value.__aenter__.return_value = mock_conn
        
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 404
    
    def test_get_user_response_structure(self, client, override_get_db_pool):
        """Test GET /users/{user_id} response structure"""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        
        mock_user = {
            "id": user_id,
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        
        mock_conn = MagicMock()
        mock_conn.fetchrow = AsyncMock(return_value=mock_user)
        override_get_db_pool.acquire.return_value.__aenter__.return_value = mock_conn
        
        response = client.get(f"/users/{user_id}")
        data = response.json()
        
        # Verify response structure
        assert "id" in data
        assert "username" in data
        assert "email" in data
        assert "is_active" in data
        assert "created_at" in data
        
        # Password should NOT be in response
        assert "password" not in data
        assert "password_hash" not in data


# ==============================================================================
# SECTION 4: PROJECT ENDPOINT TESTS
# ==============================================================================

class TestProjectEndpoints:
    """Tests for project-related endpoints"""
    
    def test_list_projects_returns_200(self, client, override_get_db_pool):
        """Test that GET /projects returns 200 OK"""
        mock_conn = MagicMock()
        mock_conn.fetch = AsyncMock(return_value=[])
        override_get_db_pool.acquire.return_value.__aenter__.return_value = mock_conn
        
        response = client.get("/projects")
        assert response.status_code == 200
    
    def test_list_projects_returns_list(self, client, override_get_db_pool):
        """Test that GET /projects returns a list"""
        mock_conn = MagicMock()
        mock_conn.fetch = AsyncMock(return_value=[])
        override_get_db_pool.acquire.return_value.__aenter__.return_value = mock_conn
        
        response = client.get("/projects")
        data = response.json()
        
        assert isinstance(data, list)
    
    def test_list_projects_with_data(self, client, override_get_db_pool):
        """Test GET /projects with mock project data"""
        mock_projects = [
            {
                "id": "456e7890-e89b-12d3-a456-426614174000",
                "name": "Test Project",
                "description": "A test project",
                "status": "active",
                "created_at": datetime.utcnow()
            }
        ]
        
        mock_conn = MagicMock()
        mock_conn.fetch = AsyncMock(return_value=mock_projects)
        override_get_db_pool.acquire.return_value.__aenter__.return_value = mock_conn
        
        response = client.get("/projects")
        data = response.json()
        
        assert len(data) == 1
        assert data[0]["name"] == "Test Project"
        assert data[0]["status"] == "active"


# ==============================================================================
# SECTION 5: ERROR HANDLING TESTS
# ==============================================================================

class TestErrorHandling:
    """Tests for error handling"""
    
    def test_404_endpoint(self, client):
        """Test that non-existent endpoint returns 404"""
        response = client.get("/nonexistent")
        assert response.status_code == 404
    
    def test_database_error_handling(self, client, override_get_db_pool):
        """Test proper error handling when database fails"""
        # Mock database error
        mock_conn = MagicMock()
        mock_conn.fetch = AsyncMock(side_effect=Exception("Database error"))
        override_get_db_pool.acquire.return_value.__aenter__.return_value = mock_conn
        
        response = client.get("/users")
        assert response.status_code == 500
    
    def test_error_response_format(self, client, override_get_db_pool):
        """Test error response format"""
        # Mock database error
        mock_conn = MagicMock()
        mock_conn.fetch = AsyncMock(side_effect=Exception("Database error"))
        override_get_db_pool.acquire.return_value.__aenter__.return_value = mock_conn
        
        response = client.get("/users")
        data = response.json()
        
        assert "error" in data
        assert "status_code" in data
        assert "timestamp" in data


# ==============================================================================
# SECTION 6: INTEGRATION TESTS
# ==============================================================================

class TestIntegration:
    """Integration tests (requires running services)"""
    
    @pytest.mark.integration
    def test_full_workflow(self, client):
        """
        Test complete workflow (requires real database).
        
        This test is marked with @pytest.mark.integration
        and will only run when explicitly requested:
        
            pytest -m integration
        
        To skip integration tests:
        
            pytest -m "not integration"
        """
        # This would test a complete workflow with a real database
        # For example: create user → create project → assign task
        pass


# ==============================================================================
# NOTES FOR STUDENTS
# ==============================================================================
#
# Testing Best Practices:
#
# 1. FIXTURES
#    - Use fixtures for reusable test setup
#    - Mock external dependencies (database, APIs)
#    - Keep fixtures simple and focused
#
# 2. TEST ORGANIZATION
#    - Group related tests in classes
#    - Use descriptive test names (test_what_when_expected)
#    - One assertion per test (when possible)
#
# 3. MOCKING
#    - Mock external services to avoid dependencies
#    - Use AsyncMock for async functions
#    - Verify mocks are called correctly
#
# 4. COVERAGE
#    - Aim for >80% code coverage
#    - Test happy paths AND error cases
#    - Test edge cases and boundary conditions
#
# 5. RUNNING TESTS
#    - Run all tests: pytest
#    - Run with coverage: pytest --cov=src
#    - Run specific file: pytest tests/test_main.py
#    - Run specific test: pytest tests/test_main.py::TestRootEndpoint::test_root_returns_200
#    - Run with verbose output: pytest -v
#    - Run with print statements: pytest -s
#
# 6. TEST MARKERS
#    - @pytest.mark.integration - Integration tests
#    - @pytest.mark.slow - Slow tests
#    - @pytest.mark.skip - Skip tests
#    - @pytest.mark.parametrize - Run test with multiple inputs
#
# Example parametrized test:
#
# @pytest.mark.parametrize("limit,offset", [(10, 0), (5, 10), (20, 5)])
# def test_pagination(client, limit, offset):
#     response = client.get(f"/users?limit={limit}&offset={offset}")
#     assert response.status_code == 200
#
# ==============================================================================
