from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreateRequest(BaseModel):
    name: str
    email: EmailStr
    phone_number: Optional[str] = None
    grade_num: Optional[int] = None
    highschool: Optional[str] = None
    sex: Optional[str] = None

class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    grade_num: Optional[int] = None
    highschool: Optional[str] = None
    sex: Optional[str] = None

class UserResponse(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    grade_num: Optional[int] = None
    sex: Optional[str] = None
    token: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        } 