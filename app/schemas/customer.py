from pydantic import BaseModel, Field
from typing import Optional

class CustomerResponse(BaseModel):
    id: str
    name: str
    tax_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    owner_id: str
    status: str

class CustomerCreate(BaseModel):
    name: str = Field(..., min_length=2, description="Tên công ty hoặc khách hàng")
    tax_code: Optional[str] = Field(None, description="Mã số thuế")
    phone: Optional[str] = Field(None, description="Số điện thoại liên lạc")
    email: Optional[str] = Field(None, description="Email liên lạc")
    address: Optional[str] = Field(None, description="Địa chỉ trụ sở")

class SystemSettingsResponse(BaseModel):
    system_name: str
    maintenance_mode: bool
    max_login_attempts: int
    session_timeout_minutes: int
    audit_log_enabled: bool
