from typing import Optional, List, Dict, Any, Callable
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.core.security import decode_access_token
from app.database.mock_db import get_user_by_username

# Sử dụng HTTPBearer với auto_error=False để tự kiểm soát ngoại lệ 401 theo đúng format SCRUM-38
security_bearer = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer)
) -> Dict[str, Any]:
    """
    Dependency lấy thông tin người dùng hiện tại từ Bearer JWT Token.
    Nếu thiếu token hoặc token không hợp lệ -> ném UnauthorizedException (HTTP 401).
    """
    if credentials is None:
        raise UnauthorizedException(
            message="Bạn cần đăng nhập để tiếp tục.",
            action="LOGIN"
        )
    
    token = credentials.credentials
    payload = decode_access_token(token)
    username = payload.get("sub")
    if not username:
        raise UnauthorizedException(
            message="Token không chứa định danh người dùng.",
            action="LOGIN"
        )
    
    user = get_user_by_username(username)
    if not user:
        raise UnauthorizedException(
            message="Tài khoản không tồn tại trong hệ thống.",
            action="LOGIN"
        )
    
    if not user.get("is_active", True):
        raise UnauthorizedException(
            message="Tài khoản của bạn đã bị khóa hoặc ngừng hoạt động.",
            action="LOGIN"
        )
    
    return user

def require_roles(allowed_roles: List[str]) -> Callable:
    """
    Dependency kiểm tra quyền hạn (Role-Based Access Control - RBAC).
    Xử lý trực tiếp tại Backend: Nếu người dùng không có role trong allowed_roles -> ném ForbiddenException (HTTP 403).
    Không phụ thuộc vào việc Frontend có ẩn/hiện menu hay button.
    """
    def role_checker(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        user_role = current_user.get("role")
        if user_role not in allowed_roles:
            raise ForbiddenException(
                message="Bạn không có quyền truy cập chức năng này.",
                action="GO_BACK"
            )
        return current_user
    
    return role_checker
