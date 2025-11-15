"""Order routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.order import (
    OrderCreate,
    OrderUpdate,
    OrderResponse,
    OrderMessageCreate,
    OrderMessageResponse
)
from app.controllers.order_controller import (
    create_order,
    get_order,
    list_orders,
    update_order_status,
    send_order_message,
    get_order_messages
)
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("", response_model=list[OrderResponse])
async def list_orders_endpoint(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List orders for the current user."""
    orders = await list_orders(db, current_user.id, current_user.role)
    
    # Enrich with business and buyer names
    enriched_orders = []
    for order in orders:
        from sqlmodel import select
        from app.models.business import Business
        
        result = await db.execute(select(Business).where(Business.id == order.business_id))
        business = result.scalar_one_or_none()
        
        result = await db.execute(select(User).where(User.id == order.buyer_id))
        buyer = result.scalar_one_or_none()
        
        messages = await get_order_messages(db, order.id, current_user.id)
        
        enriched_orders.append(OrderResponse(
            id=order.id,
            business_id=order.business_id,
            business_name=business.name if business else "Unknown",
            buyer_id=order.buyer_id,
            buyer_name=buyer.full_name if buyer else "Unknown",
            items=order.items,
            status=order.status,
            notes=order.notes,
            created_at=order.created_at,
            updated_at=order.updated_at,
            messages=[OrderMessageResponse.model_validate(m) for m in messages]
        ))
    
    return enriched_orders


@router.post("", response_model=OrderResponse, status_code=201)
async def create_order_endpoint(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> OrderResponse:
    """Create a new order."""
    # Convert items to dict format
    items_dict = [item.model_dump() for item in order_data.items]
    
    order = await create_order(
        db=db,
        buyer_id=current_user.id,
        business_id=order_data.business_id,
        items=items_dict,
        notes=order_data.notes
    )
    
    # Enrich response
    from sqlmodel import select
    from app.models.business import Business
    
    result = await db.execute(select(Business).where(Business.id == order.business_id))
    business = result.scalar_one_or_none()
    
    return OrderResponse(
        id=order.id,
        business_id=order.business_id,
        business_name=business.name if business else "Unknown",
        buyer_id=order.buyer_id,
        buyer_name=current_user.full_name,
        items=order.items,
        status=order.status,
        notes=order.notes,
        created_at=order.created_at,
        updated_at=order.updated_at,
        messages=[]
    )


@router.get("/{id}", response_model=OrderResponse)
async def get_order_endpoint(
    id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> OrderResponse:
    """Get order by ID."""
    order = await get_order(db, id, current_user.id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Enrich response
    from sqlmodel import select
    from app.models.business import Business
    
    result = await db.execute(select(Business).where(Business.id == order.business_id))
    business = result.scalar_one_or_none()
    
    result = await db.execute(select(User).where(User.id == order.buyer_id))
    buyer = result.scalar_one_or_none()
    
    messages = await get_order_messages(db, order.id, current_user.id)
    
    return OrderResponse(
        id=order.id,
        business_id=order.business_id,
        business_name=business.name if business else "Unknown",
        buyer_id=order.buyer_id,
        buyer_name=buyer.full_name if buyer else "Unknown",
        items=order.items,
        status=order.status,
        notes=order.notes,
        created_at=order.created_at,
        updated_at=order.updated_at,
        messages=[OrderMessageResponse.model_validate(m) for m in messages]
    )


@router.put("/{id}/status", response_model=OrderResponse)
async def update_order_status_endpoint(
    id: int,
    status_data: OrderUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> OrderResponse:
    """Update order status."""
    order = await update_order_status(
        db=db,
        order_id=id,
        new_status=status_data.status,
        user_id=current_user.id,
        role=current_user.role
    )
    
    # Enrich response
    from sqlmodel import select
    from app.models.business import Business
    
    result = await db.execute(select(Business).where(Business.id == order.business_id))
    business = result.scalar_one_or_none()
    
    result = await db.execute(select(User).where(User.id == order.buyer_id))
    buyer = result.scalar_one_or_none()
    
    messages = await get_order_messages(db, order.id, current_user.id)
    
    return OrderResponse(
        id=order.id,
        business_id=order.business_id,
        business_name=business.name if business else "Unknown",
        buyer_id=order.buyer_id,
        buyer_name=buyer.full_name if buyer else "Unknown",
        items=order.items,
        status=order.status,
        notes=order.notes,
        created_at=order.created_at,
        updated_at=order.updated_at,
        messages=[OrderMessageResponse.model_validate(m) for m in messages]
    )


@router.post("/{id}/messages", response_model=OrderMessageResponse, status_code=201)
async def send_message_endpoint(
    id: int,
    message_data: OrderMessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> OrderMessageResponse:
    """Send a message in an order chat."""
    message = await send_order_message(
        db=db,
        order_id=id,
        sender_id=current_user.id,
        message=message_data.message
    )
    
    # Enrich with sender name
    result = await db.execute(select(User).where(User.id == message.sender_id))
    sender = result.scalar_one_or_none()
    
    return OrderMessageResponse(
        id=message.id,
        order_id=message.order_id,
        sender_id=message.sender_id,
        sender_name=sender.full_name if sender else "Unknown",
        message=message.message,
        created_at=message.created_at
    )


@router.get("/{id}/messages", response_model=list[OrderMessageResponse])
async def get_messages_endpoint(
    id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get messages for an order."""
    messages = await get_order_messages(db, id, current_user.id)
    
    # Enrich with sender names
    enriched_messages = []
    for msg in messages:
        from sqlmodel import select
        result = await db.execute(select(User).where(User.id == msg.sender_id))
        sender = result.scalar_one_or_none()
        
        enriched_messages.append(OrderMessageResponse(
            id=msg.id,
            order_id=msg.order_id,
            sender_id=msg.sender_id,
            sender_name=sender.full_name if sender else "Unknown",
            message=msg.message,
            created_at=msg.created_at
        ))
    
    return enriched_messages
