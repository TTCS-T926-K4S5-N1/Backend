import pytest
from datetime import timedelta
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token

@pytest.fixture(scope="session")
def client():
    """
    Khởi tạo TestClient cho toàn bộ test session.
    raise_server_exceptions=False để cho phép TestClient kiểm tra response 500 do ServerErrorMiddleware trả về.
    """
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client

@pytest.fixture
def admin_token():
    """Token của người dùng có quyền Quản trị viên (ADMIN)"""
    payload = {
        "sub": "admin",
        "role": "ADMIN",
        "user_id": "USR-001"
    }
    return create_access_token(payload)

@pytest.fixture
def employee_token():
    """Token của nhân viên kinh doanh thông thường (EMPLOYEE)"""
    payload = {
        "sub": "staff",
        "role": "EMPLOYEE",
        "user_id": "USR-003"
    }
    return create_access_token(payload)

@pytest.fixture
def manager_token():
    """Token của trưởng phòng kinh doanh (MANAGER)"""
    payload = {
        "sub": "manager",
        "role": "MANAGER",
        "user_id": "USR-002"
    }
    return create_access_token(payload)

@pytest.fixture
def expired_token():
    """Token đã hết hạn (expired)"""
    payload = {
        "sub": "staff",
        "role": "EMPLOYEE",
        "user_id": "USR-003"
    }
    return create_access_token(payload, expires_delta=timedelta(seconds=-3600))

@pytest.fixture
def invalid_token():
    """Token giả mạo hoặc sai chữ ký"""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalidpayload.invalidsignature"
