from enum import Enum
from typing import Generic, Optional, TypeVar, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field

T = TypeVar("T")

class ActionEnum(str, Enum):
    """Các hành động gợi ý cho người dùng trên giao diện khi gặp lỗi"""
    LOGIN = "LOGIN"            # Yêu cầu người dùng đăng nhập lại (cho 401)
    GO_BACK = "GO_BACK"        # Gợi ý quay lại trang trước đó (cho 403, 404)
    HOME = "HOME"              # Quay về trang chủ
    RETRY = "RETRY"            # Thử lại thao tác (cho 500)
    CHECK_INPUT = "CHECK_INPUT"# Kiểm tra lại dữ liệu đầu vào (cho 422)

class ErrorCodeEnum(str, Enum):
    """Các mã lỗi chuẩn hoá để Frontend xác định loại trang báo lỗi"""
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    BAD_REQUEST = "BAD_REQUEST"

class ErrorResponse(BaseModel):
    """
    Format response lỗi thống nhất theo yêu cầu User Story SCRUM-38:
    {
      "success": false,
      "error_code": "UNAUTHORIZED",
      "message": "Bạn cần đăng nhập để tiếp tục.",
      "action": "LOGIN",
      "status_code": 401,
      "timestamp": "2026-09-28T00:00:00Z",
      "path": "/api/..."
    }
    """
    success: bool = Field(default=False, description="Trạng thái phản hồi luôn là False đối với lỗi")
    error_code: str = Field(..., description="Mã định danh lỗi (ví dụ: UNAUTHORIZED, FORBIDDEN, NOT_FOUND)")
    message: str = Field(..., description="Thông điệp hiển thị tiếng Việt thân thiện với người dùng")
    action: Optional[str] = Field(default=None, description="Hành động gợi ý cho người dùng: LOGIN, GO_BACK, HOME, RETRY")
    status_code: Optional[int] = Field(default=None, description="Mã HTTP Status Code tương ứng")
    timestamp: Optional[str] = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="Thời điểm xảy ra lỗi theo chuẩn ISO 8601"
    )
    path: Optional[str] = Field(default=None, description="Đường dẫn API endpoint xảy ra lỗi")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "success": False,
                    "error_code": "UNAUTHORIZED",
                    "message": "Bạn cần đăng nhập để tiếp tục.",
                    "action": "LOGIN",
                    "status_code": 401,
                    "timestamp": "2026-09-28T07:15:00Z",
                    "path": "/api/crm/customers"
                },
                {
                    "success": False,
                    "error_code": "FORBIDDEN",
                    "message": "Bạn không có quyền truy cập chức năng này.",
                    "action": "GO_BACK",
                    "status_code": 403,
                    "timestamp": "2026-09-28T07:15:00Z",
                    "path": "/api/admin/settings"
                },
                {
                    "success": False,
                    "error_code": "NOT_FOUND",
                    "message": "Không tìm thấy tài nguyên.",
                    "action": "GO_BACK",
                    "status_code": 404,
                    "timestamp": "2026-09-28T07:15:00Z",
                    "path": "/api/crm/customers/999"
                }
            ]
        }
    }

class SuccessResponse(BaseModel, Generic[T]):
    """Chuẩn phản hồi thành công chung của hệ thống API"""
    success: bool = Field(default=True, description="Trạng thái thành công")
    message: Optional[str] = Field(default="Thao tác thành công", description="Thông điệp thành công")
    data: Optional[T] = Field(default=None, description="Dữ liệu payload trả về")
