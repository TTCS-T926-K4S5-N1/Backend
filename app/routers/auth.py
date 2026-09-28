from fastapi import APIRouter, Depends
from app.schemas.auth import LoginRequest, TokenResponse, UserProfile
from app.schemas.response import SuccessResponse
from app.core.security import verify_password, create_access_token
from app.core.exceptions import UnauthorizedException
from app.database.mock_db import get_user_by_username
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=SuccessResponse[TokenResponse], summary="Đăng nhập hệ thống CRM")
def login(login_data: LoginRequest):
    """
    Xác thực thông tin tài khoản và trả về JWT Bearer Token.
    Nếu sai mật khẩu hoặc tài khoản không tồn tại, trả HTTP 401 với action: LOGIN.
    """
    user = get_user_by_username(login_data.username)
    if not user or not verify_password(login_data.password, user["password_hash"]):
        raise UnauthorizedException(
            message="Tên đăng nhập hoặc mật khẩu không chính xác.",
            action="LOGIN"
        )
    
    if not user.get("is_active", True):
        raise UnauthorizedException(
            message="Tài khoản đã bị tạm khóa. Vui lòng liên hệ quản trị viên.",
            action="LOGIN"
        )
    
    token_payload = {
        "sub": user["username"],
        "role": user["role"],
        "user_id": user["id"]
    }
    token = create_access_token(token_payload)
    
    user_profile = UserProfile(
        id=user["id"],
        username=user["username"],
        full_name=user["full_name"],
        email=user["email"],
        role=user["role"]
    )
    
    return SuccessResponse[TokenResponse](
        message="Đăng nhập thành công",
        data=TokenResponse(
            access_token=token,
            token_type="bearer",
            user=user_profile
        )
    )

@router.get("/me", response_model=SuccessResponse[UserProfile], summary="Lấy thông tin người dùng hiện tại")
def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    """
    Endpoint yêu cầu đăng nhập. Nếu không truyền Token hoặc Token sai -> trả HTTP 401.
    """
    user_profile = UserProfile(
        id=current_user["id"],
        username=current_user["username"],
        full_name=current_user["full_name"],
        email=current_user["email"],
        role=current_user["role"]
    )
    return SuccessResponse[UserProfile](
        message="Lấy thông tin tài khoản thành công",
        data=user_profile
    )
