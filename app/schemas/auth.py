from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str = Field(..., description="Tên đăng nhập hệ thống", min_length=2)
    password: str = Field(..., description="Mật khẩu người dùng", min_length=4)

class UserProfile(BaseModel):
    id: str
    username: str
    full_name: str
    email: str
    role: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserProfile
