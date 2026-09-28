from typing import Dict, Any, List, Optional
from app.core.security import hash_password

# Bảng người dùng giả lập trong bộ nhớ
MOCK_USERS: Dict[str, Dict[str, Any]] = {
    "admin": {
        "id": "USR-001",
        "username": "admin",
        "password_hash": hash_password("admin123"),
        "full_name": "Quản trị viên Hệ thống",
        "email": "admin@crm.ictu.vn",
        "role": "ADMIN",
        "is_active": True,
    },
    "manager": {
        "id": "USR-002",
        "username": "manager",
        "password_hash": hash_password("manager123"),
        "full_name": "Trần Quản Lý",
        "email": "manager@crm.ictu.vn",
        "role": "MANAGER",
        "is_active": True,
    },
    "staff": {
        "id": "USR-003",
        "username": "staff",
        "password_hash": hash_password("staff123"),
        "full_name": "Nguyễn Nhân Viên",
        "email": "staff@crm.ictu.vn",
        "role": "EMPLOYEE",
        "is_active": True,
    }
}

# Bảng khách hàng CRM
MOCK_CUSTOMERS: Dict[str, Dict[str, Any]] = {
    "CUST001": {
        "id": "CUST001",
        "name": "Công ty Cổ phần Công nghệ ABC",
        "tax_code": "0102030405",
        "phone": "0987654321",
        "email": "contact@abc.vn",
        "address": "Số 1 Đại Cồ Việt, Hà Nội",
        "owner_id": "staff",
        "status": "ACTIVE"
    },
    "CUST002": {
        "id": "CUST002",
        "name": "Tập đoàn Đầu tư & Xây dựng Toàn Cầu",
        "tax_code": "0203040506",
        "phone": "0912345678",
        "email": "info@global.vn",
        "address": "Tầng 12 Landmark 81, TP. Hồ Chí Minh",
        "owner_id": "manager",
        "status": "ACTIVE"
    },
    "CUST003": {
        "id": "CUST003",
        "name": "Công ty TNHH Dịch vụ Thương mại Sao Mai",
        "tax_code": "0304050607",
        "phone": "0933221100",
        "email": "support@saomai.vn",
        "address": "Đường Z115, Thành phố Thái Nguyên",
        "owner_id": "staff",
        "status": "PROSPECT"
    }
}

# Cấu hình hệ thống (Dành riêng cho ADMIN)
MOCK_SYSTEM_SETTINGS: Dict[str, Any] = {
    "system_name": "ICTU CRM Cloud",
    "maintenance_mode": False,
    "max_login_attempts": 5,
    "session_timeout_minutes": 1440,
    "audit_log_enabled": True
}

def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    return MOCK_USERS.get(username)

def get_customer_by_id(customer_id: str) -> Optional[Dict[str, Any]]:
    return MOCK_CUSTOMERS.get(customer_id)

def get_all_customers() -> List[Dict[str, Any]]:
    return list(MOCK_CUSTOMERS.values())
