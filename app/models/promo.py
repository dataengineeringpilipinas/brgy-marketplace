"""
Promo model
"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class Promo(SQLModel, table=True):
    """Promo highlights model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    business_id: Optional[int] = Field(default=None, foreign_key="business.id")
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    promo_type: str  # business_of_week, newly_registered, verified, barangay_endorsed
    start_date: datetime
    end_date: Optional[datetime] = None
    created_by: int = Field(foreign_key="user.id")  # Admin who created it
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    business: Optional["Business"] = Relationship(back_populates="promos")
    created_by_user: "User" = Relationship(back_populates="created_promos")

