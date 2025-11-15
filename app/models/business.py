"""
Business models
"""
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, JSON, Column
from sqlalchemy import JSON as SQLJSON


class Business(SQLModel, table=True):
    """Business model for home-based businesses."""
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")
    name: str
    category: str  # Food, Services, Repairs, Rentals, Crafts, Beauty, etc.
    operating_hours: Optional[str] = None  # e.g., "Mon-Fri 9AM-5PM"
    location_zone: Optional[str] = None  # Zone/purok only, no exact address
    description: Optional[str] = None
    is_verified: bool = Field(default=False)
    verified_at: Optional[datetime] = None
    verified_by: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    
    # Relationships
    owner: "User" = Relationship(
        back_populates="businesses",
        sa_relationship_kwargs={"foreign_keys": "Business.owner_id"}
    )
    verified_by_user: Optional["User"] = Relationship(
        back_populates="verified_businesses",
        sa_relationship_kwargs={"foreign_keys": "Business.verified_by"}
    )
    items: List["BusinessItem"] = Relationship(back_populates="business")
    photos: List["BusinessPhoto"] = Relationship(back_populates="business")
    orders: List["Order"] = Relationship(back_populates="business")
    reviews: List["Review"] = Relationship(back_populates="business")
    promos: List["Promo"] = Relationship(back_populates="business")


class BusinessItem(SQLModel, table=True):
    """Menu/Service items for businesses."""
    id: Optional[int] = Field(default=None, primary_key=True)
    business_id: int = Field(foreign_key="business.id")
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    is_available: bool = Field(default=True)
    
    # Relationships
    business: Business = Relationship(back_populates="items")


class BusinessPhoto(SQLModel, table=True):
    """Photos for businesses."""
    id: Optional[int] = Field(default=None, primary_key=True)
    business_id: int = Field(foreign_key="business.id")
    image_url: str
    is_primary: bool = Field(default=False)
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    business: Business = Relationship(back_populates="photos")

