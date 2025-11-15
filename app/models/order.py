"""
Order models
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlmodel import SQLModel, Field, Relationship, JSON, Column
from sqlalchemy import JSON as SQLJSON


class Order(SQLModel, table=True):
    """Order/Inquiry model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    business_id: int = Field(foreign_key="business.id")
    buyer_id: int = Field(foreign_key="user.id")
    items: Dict[str, Any] = Field(sa_column=Column(SQLJSON))  # JSON: [{"item_id": 1, "quantity": 2, "price": 100}]
    status: str = Field(default="pending")  # pending, accepted, ready_for_pickup, delivered, completed
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    business: "Business" = Relationship(back_populates="orders")
    buyer: "User" = Relationship(
        back_populates="orders_as_buyer",
        sa_relationship_kwargs={"foreign_keys": "Order.buyer_id"}
    )
    messages: List["OrderMessage"] = Relationship(back_populates="order")
    review: Optional["Review"] = Relationship(back_populates="order")


class OrderMessage(SQLModel, table=True):
    """Chat messages for orders."""
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id")
    sender_id: int = Field(foreign_key="user.id")
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    order: Order = Relationship(back_populates="messages")
    sender: "User" = Relationship(back_populates="order_messages")

