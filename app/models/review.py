"""
Review model
"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class Review(SQLModel, table=True):
    """Review model for business ratings."""
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id", unique=True)  # One review per order
    business_id: int = Field(foreign_key="business.id")
    reviewer_id: int = Field(foreign_key="user.id")
    rating: int = Field(ge=1, le=5)  # 1-5 stars
    comment: Optional[str] = None
    photo_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_visible: bool = Field(default=True)  # Admin can hide abusive reviews
    
    # Relationships
    order: "Order" = Relationship(back_populates="review")
    business: "Business" = Relationship(back_populates="reviews")
    reviewer: "User" = Relationship(back_populates="reviews")

