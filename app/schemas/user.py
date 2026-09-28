from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

class UserImportSchema(BaseModel):
    full_name: str
    email: EmailStr
    department: str
    role: Optional[str] = "User"

    @field_validator("full_name", "department")
    @classmethod
    def must_not_be_empty(cls, value):
        if not str(value).strip():
            raise ValueError("Trường này không được để trống")
        return str(value).strip()