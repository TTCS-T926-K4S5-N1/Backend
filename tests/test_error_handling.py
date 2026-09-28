import pytest

class TestAuthenticationErrors:
    """Bộ kiểm thử cho các trường hợp lỗi Xác thực - HTTP 401"""

    def test_unauthenticated_request_no_token(self, client):
        """
        Kịch bản 1: Người dùng chưa đăng nhập, gọi API yêu cầu bảo mật không kèm Token.
        Kỳ vọng: HTTP 401, error_code='UNAUTHORIZED', action='LOGIN'.
        """
        response = client.get("/api/auth/me")
        assert response.status_code == 401
        
        data = response.json()
        assert data["success"] is False
        assert data["error_code"] == "UNAUTHORIZED"
        assert data["action"] == "LOGIN"
        assert "đăng nhập" in data["message"].lower()
        assert data["status_code"] == 401
        assert "path" in data

    def test_unauthenticated_request_invalid_token(self, client, invalid_token):
        """
        Kịch bản 2: Người dùng gửi Token sai cấu trúc hoặc bị giả mạo chữ ký.
        Kỳ vọng: HTTP 401, error_code='UNAUTHORIZED', action='LOGIN'.
        """
        headers = {"Authorization": f"Bearer {invalid_token}"}
        response = client.get("/api/auth/me", headers=headers)
        assert response.status_code == 401
        
        data = response.json()
        assert data["success"] is False
        assert data["error_code"] == "UNAUTHORIZED"
        assert data["action"] == "LOGIN"
        assert data["status_code"] == 401

    def test_unauthenticated_request_expired_token(self, client, expired_token):
        """
        Kịch bản 3: Token của người dùng đã hết hạn (expired).
        Kỳ vọng: HTTP 401, error_code='UNAUTHORIZED', action='LOGIN', thông báo hết hạn.
        """
        headers = {"Authorization": f"Bearer {expired_token}"}
        response = client.get("/api/crm/customers", headers=headers)
        assert response.status_code == 401
        
        data = response.json()
        assert data["success"] is False
        assert data["error_code"] == "UNAUTHORIZED"
        assert data["action"] == "LOGIN"
        assert "hết hạn" in data["message"].lower()

    def test_login_failure_wrong_credentials(self, client):
        """
        Kịch bản 4: Đăng nhập với mật khẩu sai.
        Kỳ vọng: HTTP 401, error_code='UNAUTHORIZED', action='LOGIN'.
        """
        payload = {"username": "admin", "password": "wrong_password_123"}
        response = client.post("/api/auth/login", json=payload)
        assert response.status_code == 401
        
        data = response.json()
        assert data["success"] is False
        assert data["error_code"] == "UNAUTHORIZED"
        assert data["action"] == "LOGIN"


class TestAuthorizationErrors:
    """Bộ kiểm thử cho các trường hợp lỗi Phân quyền - HTTP 403"""

    def test_forbidden_request_employee_access_admin_api(self, client, employee_token):
        """
        Kịch bản 5: Đã đăng nhập với tài khoản EMPLOYEE nhưng truy cập API của ADMIN.
        Xử lý tại Backend, không phụ thuộc vào Frontend.
        Kỳ vọng: HTTP 403, error_code='FORBIDDEN', action='GO_BACK'.
        """
        headers = {"Authorization": f"Bearer {employee_token}"}
        response = client.get("/api/admin/settings", headers=headers)
        assert response.status_code == 403
        
        data = response.json()
        assert data["success"] is False
        assert data["error_code"] == "FORBIDDEN"
        assert data["action"] == "GO_BACK"
        assert "không có quyền" in data["message"].lower()
        assert data["status_code"] == 403
        assert data["path"] == "/api/admin/settings"

    def test_forbidden_request_manager_access_admin_api(self, client, manager_token):
        """
        Kịch bản 6: Đã đăng nhập với tài khoản MANAGER nhưng truy cập API chỉ dành riêng cho ADMIN.
        Kỳ vọng: HTTP 403, error_code='FORBIDDEN', action='GO_BACK'.
        """
        headers = {"Authorization": f"Bearer {manager_token}"}
        response = client.get("/api/admin/settings", headers=headers)
        assert response.status_code == 403
        
        data = response.json()
        assert data["success"] is False
        assert data["error_code"] == "FORBIDDEN"
        assert data["action"] == "GO_BACK"


class TestNotFoundErrors:
    """Bộ kiểm thử cho các trường hợp không tìm thấy tài nguyên / URL - HTTP 404"""

    def test_resource_not_found_customer(self, client, employee_token):
        """
        Kịch bản 7: Truy vấn một khách hàng không tồn tại trong database CRM.
        Kỳ vọng: HTTP 404, error_code='NOT_FOUND', action='GO_BACK'.
        """
        headers = {"Authorization": f"Bearer {employee_token}"}
        response = client.get("/api/crm/customers/CUST_KHONG_TON_TAI_999", headers=headers)
        assert response.status_code == 404
        
        data = response.json()
        assert data["success"] is False
        assert data["error_code"] == "NOT_FOUND"
        assert data["action"] == "GO_BACK"
        assert "không tìm thấy" in data["message"].lower()
        assert data["status_code"] == 404

    def test_unmatched_route_not_found(self, client):
        """
        Kịch bản 8: Người dùng gõ nhầm URL hoặc truy cập đường dẫn không tồn tại trên hệ thống.
        Kỳ vọng: HTTP 404, error_code='NOT_FOUND', action='GO_BACK'. Không trả về trang trắng.
        """
        response = client.get("/api/duong-dan-hoan-toan-khong-ton-tai")
        assert response.status_code == 404
        
        data = response.json()
        assert data["success"] is False
        assert data["error_code"] == "NOT_FOUND"
        assert data["action"] == "GO_BACK"
        assert "không tìm thấy" in data["message"].lower()
        assert data["status_code"] == 404


class TestValidRequests:
    """Bộ kiểm thử cho các trường hợp hợp lệ - HTTP 200"""

    def test_login_success(self, client):
        """Kịch bản 9: Đăng nhập thành công trả về access token"""
        payload = {"username": "admin", "password": "admin123"}
        response = client.post("/api/auth/login", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "access_token" in data["data"]
        assert data["data"]["user"]["role"] == "ADMIN"

    def test_get_me_success(self, client, admin_token):
        """Kịch bản 10: Lấy thông tin tài khoản hợp lệ khi đã đăng nhập"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.get("/api/auth/me", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert data["data"]["username"] == "admin"
        assert data["data"]["role"] == "ADMIN"

    def test_admin_access_settings_success(self, client, admin_token):
        """Kịch bản 11: ADMIN truy cập API cấu hình thành công"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.get("/api/admin/settings", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert data["data"]["system_name"] == "ICTU CRM Cloud"

    def test_list_customers_success(self, client, employee_token):
        """Kịch bản 12: Lấy danh sách khách hàng thành công"""
        headers = {"Authorization": f"Bearer {employee_token}"}
        response = client.get("/api/crm/customers", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert isinstance(data["data"], list)
        assert len(data["data"]) >= 1

    def test_get_existing_customer_detail_success(self, client, employee_token):
        """Kịch bản 13: Lấy chi tiết khách hàng CUST001 thành công"""
        headers = {"Authorization": f"Bearer {employee_token}"}
        response = client.get("/api/crm/customers/CUST001", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert data["data"]["id"] == "CUST001"
        assert data["data"]["name"] == "Công ty Cổ phần Công nghệ ABC"


class TestSecurityAndDataSanitization:
    """Bộ kiểm thử kiểm tra an toàn thông tin & không rò rỉ dữ liệu nhạy cảm"""

    def test_validation_error_format(self, client):
        """Kịch bản 14: Lỗi validation (422) có format chuẩn, không làm crash server"""
        payload = {"invalid_key": "xyz"}  # Thiếu username & password bắt buộc
        response = client.post("/api/auth/login", json=payload)
        assert response.status_code == 422
        
        data = response.json()
        assert data["success"] is False
        assert data["error_code"] == "VALIDATION_ERROR"
        assert data["action"] == "CHECK_INPUT"

    def test_internal_server_error_sanitization(self, client, admin_token):
        """
        Kịch bản 15: Lỗi 500 hệ thống không trả stack trace, database info ra client.
        Kỳ vọng: HTTP 500, error_code='INTERNAL_SERVER_ERROR', action='RETRY'.
        """
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.get("/api/admin/trigger-server-error", headers=headers)
        assert response.status_code == 500
        
        data = response.json()
        assert data["success"] is False
        assert data["error_code"] == "INTERNAL_SERVER_ERROR"
        assert data["action"] == "RETRY"
        
        # Đảm bảo không chứa stack trace hoặc thông tin kỹ thuật nhạy cảm trong response JSON
        raw_text = response.text
        assert "Traceback" not in raw_text
        assert "RuntimeError" not in raw_text
        assert "Database Timeout" not in raw_text

    def test_swagger_and_openapi_docs_available(self, client):
        """Kịch bản 16: Swagger UI và OpenAPI schema hoạt động bình thường"""
        docs_res = client.get("/docs")
        assert docs_res.status_code == 200
        
        openapi_res = client.get("/openapi.json")
        assert openapi_res.status_code == 200
        openapi_data = openapi_res.json()
        assert "openapi" in openapi_data
        assert openapi_data["info"]["title"] == "CRM Management System - TTCS"
