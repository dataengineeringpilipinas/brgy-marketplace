"""
Promo schemas
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class PromoCreate(BaseModel):
    """Promo creation schema."""
    business_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    promo_type: str  # business_of_week, newly_registered, verified, barangay_endorsed
    start_date: datetime
    end_date: Optional[datetime] = None


class PromoUpdate(BaseModel):
    """Promo update schema."""
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    promo_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class PromoResponse(BaseModel):
    """Promo response schema."""
    id: int
    business_id: Optional[int] = None
    business_name: Optional[str] = None
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    promo_type: str
    start_date: datetime
    end_date: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

