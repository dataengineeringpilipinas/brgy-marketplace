"""
Business schemas
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class BusinessItemCreate(BaseModel):
    """Business item creation schema."""
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    is_available: bool = True


class BusinessItemUpdate(BaseModel):
    """Business item update schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    is_available: Optional[bool] = None


class BusinessItemResponse(BaseModel):
    """Business item response schema."""
    id: int
    business_id: int
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    is_available: bool
    
    class Config:
        from_attributes = True


class BusinessPhotoResponse(BaseModel):
    """Business photo response schema."""
    id: int
    business_id: int
    image_url: str
    is_primary: bool
    uploaded_at: datetime
    
    class Config:
        from_attributes = True


class BusinessCreate(BaseModel):
    """Business creation schema."""
    name: str
    category: str
    operating_hours: Optional[str] = None
    location_zone: Optional[str] = None
    description: Optional[str] = None


class BusinessUpdate(BaseModel):
    """Business update schema."""
    name: Optional[str] = None
    category: Optional[str] = None
    operating_hours: Optional[str] = None
    location_zone: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class BusinessResponse(BaseModel):
    """Business response schema."""
    id: int
    owner_id: int
    name: str
    category: str
    operating_hours: Optional[str] = None
    location_zone: Optional[str] = None
    description: Optional[str] = None
    is_verified: bool
    verified_at: Optional[datetime] = None
    verified_by: Optional[int] = None
    created_at: datetime
    is_active: bool
    items: List[BusinessItemResponse] = []
    photos: List[BusinessPhotoResponse] = []
    
    class Config:
        from_attributes = True


class BusinessListResponse(BaseModel):
    """Business list response schema."""
    id: int
    name: str
    category: str
    location_zone: Optional[str] = None
    is_verified: bool
    description: Optional[str] = None
    primary_photo: Optional[str] = None
    
    class Config:
        from_attributes = True

