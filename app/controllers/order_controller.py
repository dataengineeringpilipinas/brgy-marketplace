"""
Order controller
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi import HTTPException, status

from app.models.order import Order, OrderMessage
from app.models.business import Business
from app.models.user import User
from app.models.analytics import AnalyticsEvent


async def create_order(
    db: AsyncSession,
    buyer_id: int,
    business_id: int,
    items: List[Dict[str, Any]],
    notes: Optional[str] = None
) -> Order:
    """Create a new order."""
    # Verify business exists
    result = await db.execute(select(Business).where(Business.id == business_id))
    business = result.scalar_one_or_none()
    
    if not business or not business.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    # Create order
    order = Order(
        business_id=business_id,
        buyer_id=buyer_id,
        items=items,
        notes=notes,
        status="pending"
    )
    
    db.add(order)
    await db.commit()
    await db.refresh(order)
    
    # Track order creation for analytics
    event = AnalyticsEvent(
        event_type="order_created",
        business_id=business_id,
        category=business.category
    )
    db.add(event)
    await db.commit()
    
    return order


async def get_order(
    db: AsyncSession,
    order_id: int,
    user_id: Optional[int] = None
) -> Optional[Order]:
    """Get an order by ID."""
    query = select(Order).where(Order.id == order_id)
    
    # If user_id provided, ensure user has access
    if user_id:
        query = query.where(
            (Order.buyer_id == user_id) | 
            (Order.business_id.in_(select(Business.id).where(Business.owner_id == user_id)))
        )
    
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def list_orders(
    db: AsyncSession,
    user_id: int,
    role: str = "resident"
) -> List[Order]:
    """List orders for a user."""
    if role == "admin":
        # Admins can see all orders
        result = await db.execute(select(Order))
    else:
        # Residents see their own orders or orders for their businesses
        result = await db.execute(
            select(Order).where(
                (Order.buyer_id == user_id) |
                (Order.business_id.in_(
                    select(Business.id).where(Business.owner_id == user_id)
                ))
            )
        )
    
    return result.scalars().all()


async def update_order_status(
    db: AsyncSession,
    order_id: int,
    new_status: str,
    user_id: int,
    role: str = "resident"
) -> Order:
    """Update order status."""
    order = await get_order(db, order_id, user_id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Verify user has permission (buyer or business owner)
    result = await db.execute(select(Business).where(Business.id == order.business_id))
    business = result.scalar_one_or_none()
    
    can_update = (
        order.buyer_id == user_id or
        (business and business.owner_id == user_id) or
        role == "admin"
    )
    
    if not can_update:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this order"
        )
    
    # Validate status transition
    valid_statuses = ["pending", "accepted", "ready_for_pickup", "delivered", "completed"]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    order.status = new_status
    order.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(order)
    
    return order


async def send_order_message(
    db: AsyncSession,
    order_id: int,
    sender_id: int,
    message: str
) -> OrderMessage:
    """Send a message in an order chat."""
    order = await get_order(db, order_id, sender_id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Verify sender has access
    result = await db.execute(select(Business).where(Business.id == order.business_id))
    business = result.scalar_one_or_none()
    
    can_message = (
        order.buyer_id == sender_id or
        (business and business.owner_id == sender_id)
    )
    
    if not can_message:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to send messages for this order"
        )
    
    order_message = OrderMessage(
        order_id=order_id,
        sender_id=sender_id,
        message=message
    )
    
    db.add(order_message)
    await db.commit()
    await db.refresh(order_message)
    
    return order_message


async def get_order_messages(
    db: AsyncSession,
    order_id: int,
    user_id: int
) -> List[OrderMessage]:
    """Get messages for an order."""
    order = await get_order(db, order_id, user_id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    result = await db.execute(
        select(OrderMessage)
        .where(OrderMessage.order_id == order_id)
        .order_by(OrderMessage.created_at)
    )
    
    return result.scalars().all()

