# CRM Backend - Thực tập cơ sở (TTCS)
## User Story SCRUM-38: Cơ chế Thông báo và Xử lý Lỗi Tập trung (Error Handling & Response Architecture)

> **Mô tả Story:**  
> “Là người dùng của hệ thống, tôi muốn nhận thông báo rõ ràng khi truy cập nhầm chỗ hoặc không đủ quyền, để biết mình nên làm gì tiếp thay vì gặp một trang trắng.”

---

### 1. Kiến trúc thư mục dự án

```
d:/TTCS/
├── app/
│   ├── core/
│   │   ├── config.py             # Cấu hình hệ thống, JWT Secret, Token Expire
│   │   ├── exceptions.py         # Custom AppException, Unauthorized, Forbidden, NotFound
│   │   └── security.py           # Quản lý mã hoá mật khẩu, JWT Encode/Decode
│   ├── database/
│   │   └── mock_db.py            # Cơ sở dữ liệu giả lập (Users, Roles, Customers)
│   ├── dependencies/
│   │   └── auth.py               # Dependency get_current_user & require_roles (RBAC)
│   ├── middlewares/
│   │   └── exception_handler.py  # Global Exception Handlers (401, 403, 404, 422, 500)
│   ├── routers/
│   │   ├── auth.py               # API Xác thực (/api/auth/login, /api/auth/me)
│   │   ├── crm.py                # API Nghiệp vụ Khách hàng (/api/crm/customers)
│   │   └── admin.py              # API Quản trị (/api/admin/settings - Role: ADMIN)
│   ├── schemas/
│   │   ├── auth.py               # Schema đăng nhập & thông tin người dùng
│   │   ├── customer.py           # Schema dữ liệu khách hàng CRM
│   │   └── response.py           # Schema chuẩn hoá ErrorResponse & SuccessResponse
│   └── main.py                   # Khởi tạo FastAPI App, CORS & gắn Handlers
├── tests/
│   ├── conftest.py               # Fixtures TestClient, Admin/Employee/Expired Tokens
│   └── test_error_handling.py    # Bộ 16 Test Cases tự động kiểm thử toàn diện
├── requirements.txt              # Danh sách thư viện phụ thuộc
└── README.md                     # Tài liệu hướng dẫn sử dụng & tích hợp Frontend
```

---

### 2. Chuẩn hoá cấu trúc phản hồi lỗi (Error Response Format)

Toàn bộ các lỗi hệ thống đều trả về JSON thống nhất theo định dạng:

```json
{
  "success": false,
  "error_code": "UNAUTHORIZED | FORBIDDEN | NOT_FOUND | VALIDATION_ERROR | INTERNAL_SERVER_ERROR",
  "message": "Thông điệp tiếng Việt rõ ràng, thân thiện với người dùng",
  "action": "LOGIN | GO_BACK | HOME | RETRY | CHECK_INPUT",
  "status_code": 401,
  "timestamp": "2026-09-28T07:15:00.000000+00:00",
  "path": "/api/crm/customers/999"
}
```

#### Chi tiết các trường hợp cốt lõi:

1. **Chưa đăng nhập hoặc Token không hợp lệ (HTTP 401)**:
   ```json
   {
     "success": false,
     "error_code": "UNAUTHORIZED",
     "message": "Bạn cần đăng nhập để tiếp tục.",
     "action": "LOGIN",
     "status_code": 401,
     "path": "/api/auth/me"
   }
   ```
2. **Đã đăng nhập nhưng không có quyền (HTTP 403)**:
   ```json
   {
     "success": false,
     "error_code": "FORBIDDEN",
     "message": "Bạn không có quyền truy cập chức năng này.",
     "action": "GO_BACK",
     "status_code": 403,
     "path": "/api/admin/settings"
   }
   ```
3. **Không tìm thấy tài nguyên hoặc gõ sai URL (HTTP 404)**:
   ```json
   {
     "success": false,
     "error_code": "NOT_FOUND",
     "message": "Không tìm thấy tài nguyên.",
     "action": "GO_BACK",
     "status_code": 404,
     "path": "/api/crm/customers/NON_EXISTENT"
   }
   ```
4. **Lỗi hệ thống máy chủ nội bộ (HTTP 500)**:
   ```json
   {
     "success": false,
     "error_code": "INTERNAL_SERVER_ERROR",
     "message": "Đã xảy ra lỗi máy chủ nội bộ. Vui lòng thử lại sau hoặc liên hệ quản trị viên.",
     "action": "RETRY",
     "status_code": 500,
     "path": "/api/..."
   }
   ```
   *(Không để lộ Stack Trace, Database table, hay thông tin nhạy cảm)*

---

### 3. Hướng dẫn chạy Server & Swagger

```bash
# Cài đặt thư viện
pip install -r requirements.txt

# Khởi chạy server FastAPI
python -m uvicorn app.main:app --reload --port 8000
```

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

---

### 4. Hướng dẫn chạy kiểm thử tự động (Automated Tests)

```bash
# Chạy toàn bộ 16 kịch bản kiểm thử
python -m pytest -v
```
