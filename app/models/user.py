"""
User model
"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    """User model for residents and admins."""
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    full_name: str
    phone: Optional[str] = None
    role: str = Field(default="resident")  # "resident" or "admin"
    address_zone: Optional[str] = None  # Zone/purok only, no exact address
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    
    # Relationships
    businesses: list["Business"] = Relationship(
        back_populates="owner",
        sa_relationship_kwargs={"foreign_keys": "Business.owner_id"}
    )
    orders_as_buyer: list["Order"] = Relationship(
        back_populates="buyer",
        sa_relationship_kwargs={"foreign_keys": "Order.buyer_id"}
    )
    reviews: list["Review"] = Relationship(back_populates="reviewer")
    order_messages: list["OrderMessage"] = Relationship(back_populates="sender")
    verified_businesses: list["Business"] = Relationship(
        back_populates="verified_by_user",
        sa_relationship_kwargs={"foreign_keys": "Business.verified_by"}
    )
    created_promos: list["Promo"] = Relationship(back_populates="created_by_user")

