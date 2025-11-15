"""
Review schemas
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    """Review creation schema."""
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None
    photo_url: Optional[str] = None


class ReviewResponse(BaseModel):
    """Review response schema."""
    id: int
    order_id: int
    business_id: int
    reviewer_id: int
    reviewer_name: Optional[str] = None
    rating: int
    comment: Optional[str] = None
    photo_url: Optional[str] = None
    created_at: datetime
    is_visible: bool
    
    class Config:
        from_attributes = True

