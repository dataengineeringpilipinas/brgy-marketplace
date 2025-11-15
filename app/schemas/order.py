"""
Order schemas
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class OrderItem(BaseModel):
    """Order item schema."""
    item_id: int
    quantity: int
    price: float


class OrderCreate(BaseModel):
    """Order creation schema."""
    business_id: int
    items: List[OrderItem]
    notes: Optional[str] = None


class OrderUpdate(BaseModel):
    """Order status update schema."""
    status: str  # pending, accepted, ready_for_pickup, delivered, completed


class OrderMessageCreate(BaseModel):
    """Order message creation schema."""
    message: str


class OrderMessageResponse(BaseModel):
    """Order message response schema."""
    id: int
    order_id: int
    sender_id: int
    sender_name: Optional[str] = None
    message: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    """Order response schema."""
    id: int
    business_id: int
    business_name: str
    buyer_id: int
    buyer_name: str
    items: Dict[str, Any]
    status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    messages: List[OrderMessageResponse] = []
    
    class Config:
        from_attributes = True

