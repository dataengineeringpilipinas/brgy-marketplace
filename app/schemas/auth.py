"""
Authentication schemas (Pydantic models)
"""
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    """User registration schema."""
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None
    address_zone: Optional[str] = None


class UserLogin(BaseModel):
    """User login schema."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response schema."""
    id: int
    email: str
    full_name: str
    phone: Optional[str] = None
    role: str
    address_zone: Optional[str] = None
    is_active: bool
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str
    user: UserResponse

