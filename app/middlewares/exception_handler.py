import logging
from datetime import datetime, timezone
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.exceptions import AppException
from app.schemas.response import ErrorResponse, ActionEnum, ErrorCodeEnum

logger = logging.getLogger("crm.exceptions")

def register_exception_handlers(app: FastAPI) -> None:
    """
    Đăng ký toàn bộ Global Exception Handlers cho hệ thống FastAPI.
    Đảm bảo mọi lỗi (401, 403, 404, 422, 500) đều được format thống nhất
    theo đặc tả User Story SCRUM-38 và không để lộ thông tin nhạy cảm.
    """

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        """Xử lý các ngoại lệ nghiệp vụ do ứng dụng chủ động ném ra"""
        error_payload = ErrorResponse(
            success=False,
            error_code=exc.error_code,
            message=exc.message,
            action=exc.action,
            status_code=exc.status_code,
            timestamp=datetime.now(timezone.utc).isoformat(),
            path=request.url.path
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=error_payload.model_dump()
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """
        Bắt các lỗi HTTP tiêu chuẩn từ FastAPI/Starlette (bao gồm truy cập sai URL 404,
        hoặc ngoại lệ do middleware ném ra).
        """
        status_code = exc.status_code

        if status_code == 401:
            error_code = ErrorCodeEnum.UNAUTHORIZED.value
            message = "Bạn cần đăng nhập để tiếp tục." if exc.detail in ["Not authenticated", "Unauthorized"] else str(exc.detail)
            action = ActionEnum.LOGIN.value
        elif status_code == 403:
            error_code = ErrorCodeEnum.FORBIDDEN.value
            message = "Bạn không có quyền truy cập chức năng này." if exc.detail == "Forbidden" else str(exc.detail)
            action = ActionEnum.GO_BACK.value
        elif status_code == 404:
            error_code = ErrorCodeEnum.NOT_FOUND.value
            message = "Không tìm thấy tài nguyên." if exc.detail == "Not Found" else str(exc.detail)
            action = ActionEnum.GO_BACK.value
        elif status_code == 400:
            error_code = ErrorCodeEnum.BAD_REQUEST.value
            message = str(exc.detail)
            action = ActionEnum.GO_BACK.value
        else:
            error_code = f"HTTP_{status_code}"
            message = str(exc.detail)
            action = ActionEnum.GO_BACK.value

        error_payload = ErrorResponse(
            success=False,
            error_code=error_code,
            message=message,
            action=action,
            status_code=status_code,
            timestamp=datetime.now(timezone.utc).isoformat(),
            path=request.url.path
        )
        return JSONResponse(
            status_code=status_code,
            content=error_payload.model_dump()
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Xử lý lỗi dữ liệu đầu vào không hợp lệ (HTTP 422)"""
        error_payload = ErrorResponse(
            success=False,
            error_code=ErrorCodeEnum.VALIDATION_ERROR.value,
            message="Dữ liệu gửi lên không đúng định dạng. Vui lòng kiểm tra lại thông tin.",
            action=ActionEnum.CHECK_INPUT.value,
            status_code=422,
            timestamp=datetime.now(timezone.utc).isoformat(),
            path=request.url.path
        )
        return JSONResponse(
            status_code=422,
            content=error_payload.model_dump()
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """
        Bắt tất cả lỗi hệ thống chưa được kiểm soát (HTTP 500).
        Ghi log chi tiết trên server nhưng KHÔNG trả stack trace, database info ra client.
        """
        logger.error(f"Lỗi hệ thống chưa được xử lý tại {request.url.path}: {str(exc)}", exc_info=True)
        
        error_payload = ErrorResponse(
            success=False,
            error_code=ErrorCodeEnum.INTERNAL_SERVER_ERROR.value,
            message="Đã xảy ra lỗi máy chủ nội bộ. Vui lòng thử lại sau hoặc liên hệ quản trị viên.",
            action=ActionEnum.RETRY.value,
            status_code=500,
            timestamp=datetime.now(timezone.utc).isoformat(),
            path=request.url.path
        )
        return JSONResponse(
            status_code=500,
            content=error_payload.model_dump()
        )
