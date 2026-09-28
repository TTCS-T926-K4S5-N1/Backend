from fastapi import APIRouter, Depends
from app.schemas.customer import SystemSettingsResponse
from app.schemas.response import SuccessResponse
from app.dependencies.auth import require_roles
from app.database.mock_db import MOCK_SYSTEM_SETTINGS

router = APIRouter(prefix="/admin", tags=["Admin System Management"])

@router.get("/settings", response_model=SuccessResponse[SystemSettingsResponse], summary="Xem cấu hình hệ thống (Chỉ Admin)")
def get_system_settings(admin_user: dict = Depends(require_roles(["ADMIN"]))):
    """
    Endpoint quản trị hệ thống:
    - Nếu chưa đăng nhập: HTTP 401 (UNAUTHORIZED)
    - Nếu đăng nhập với tài khoản không phải ADMIN (ví dụ EMPLOYEE/MANAGER): HTTP 403 (FORBIDDEN, action: GO_BACK)
    - Nếu là ADMIN: HTTP 200 kèm dữ liệu cấu hình
    """
    return SuccessResponse[SystemSettingsResponse](
        message="Lấy cấu hình hệ thống thành công",
        data=SystemSettingsResponse(**MOCK_SYSTEM_SETTINGS)
    )

@router.get("/trigger-server-error", summary="Endpoint giả lập lỗi hệ thống 500 (Phục vụ test kiểm thử)")
def trigger_unhandled_error(admin_user: dict = Depends(require_roles(["ADMIN"]))):
    """
    Endpoint cố tình ném ra một lỗi chưa xử lý (unhandled error)
    để kiểm thử cơ chế bắt lỗi 500, đảm bảo server không để lộ thông tin nhạy cảm/stack trace ra client.
    """
    raise RuntimeError("Giả lập lỗi kết nối cơ sở dữ liệu CRM Database Timeout")