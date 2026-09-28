from fastapi import FastAPI

# Import đích danh biến router từ từng file và đổi tên để tránh xung đột
from app.routers.admin import router as admin_router
from app.routers.users import router as users_router

app = FastAPI(title="CRM Backend - TTCS")

# ... (Giữ nguyên các đoạn code cấu hình khác ở giữa nếu có) ...

# Đăng ký router bằng tên biến vừa đặt
app.include_router(admin_router)
app.include_router(users_router)