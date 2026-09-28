from typing import Optional, Any
from app.schemas.response import ActionEnum, ErrorCodeEnum

class AppException(Exception):
    """
    Base Exception cho toàn bộ ứng dụng CRM.
    Cho phép chỉ định status_code, error_code chuẩn hoá, message và action gợi ý.
    """
    def __init__(
        self,
        status_code: int = 400,
        error_code: str = ErrorCodeEnum.BAD_REQUEST.value,
        message: str = "Đã xảy ra lỗi khi xử lý yêu cầu.",
        action: Optional[str] = ActionEnum.GO_BACK.value,
        details: Optional[Any] = None
    ):
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.action = action
        self.details = details

class UnauthorizedException(AppException):
    """Lỗi HTTP 401: Người dùng chưa xác thực hoặc token không hợp lệ"""
    def __init__(
        self,
        message: str = "Bạn cần đăng nhập để tiếp tục.",
        action: str = ActionEnum.LOGIN.value,
        details: Optional[Any] = None
    ):
        super().__init__(
            status_code=401,
            error_code=ErrorCodeEnum.UNAUTHORIZED.value,
            message=message,
            action=action,
            details=details
        )

class ForbiddenException(AppException):
    """Lỗi HTTP 403: Người dùng đã đăng nhập nhưng không đủ quyền hạn truy cập tài nguyên"""
    def __init__(
        self,
        message: str = "Bạn không có quyền truy cập chức năng này.",
        action: str = ActionEnum.GO_BACK.value,
        details: Optional[Any] = None
    ):
        super().__init__(
            status_code=403,
            error_code=ErrorCodeEnum.FORBIDDEN.value,
            message=message,
            action=action,
            details=details
        )

class NotFoundException(AppException):
    """Lỗi HTTP 404: Không tìm thấy tài nguyên hoặc endpoint yêu cầu"""
    def __init__(
        self,
        message: str = "Không tìm thấy tài nguyên.",
        action: str = ActionEnum.GO_BACK.value,
        details: Optional[Any] = None
    ):
        super().__init__(
            status_code=404,
            error_code=ErrorCodeEnum.NOT_FOUND.value,
            message=message,
            action=action,
            details=details
        )

class ValidationException(AppException):
    """Lỗi HTTP 422: Dữ liệu gửi lên không đúng định dạng hoặc vi phạm ràng buộc nghiệp vụ"""
    def __init__(
        self,
        message: str = "Dữ liệu gửi lên không hợp lệ.",
        action: str = ActionEnum.CHECK_INPUT.value,
        details: Optional[Any] = None
    ):
        super().__init__(
            status_code=422,
            error_code=ErrorCodeEnum.VALIDATION_ERROR.value,
            message=message,
            action=action,
            details=details
        )
