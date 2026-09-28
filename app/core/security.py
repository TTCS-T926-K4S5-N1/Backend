import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import jwt
from app.core.config import settings
from app.core.exceptions import UnauthorizedException

def hash_password(password: str) -> str:
    """Băm mật khẩu bằng SHA-256 kèm salt cố định đơn giản cho môi trường nội bộ/lab"""
    salt = "crm_ttcs_salt_"
    return hashlib.sha256(f"{salt}{password}".encode("utf-8")).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """So khớp mật khẩu plain text với chuỗi hash"""
    return hash_password(plain_password) == hashed_password

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Tạo JWT access token với thời hạn hết hạn cụ thể"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Giải mã và kiểm tra tính hợp lệ của JWT token.
    Bắt lỗi ExpiredSignatureError và InvalidTokenError để ném UnauthorizedException chuẩn hoá.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException(
            message="Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.",
            action="LOGIN"
        )
    except jwt.PyJWTError:
        raise UnauthorizedException(
            message="Token xác thực không hợp lệ. Vui lòng đăng nhập lại.",
            action="LOGIN"
        )
