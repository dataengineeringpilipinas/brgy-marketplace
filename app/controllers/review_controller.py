"""
Review controller
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi import HTTPException, status

from app.models.review import Review
from app.models.order import Order
from app.models.business import Business


async def create_review(
    db: AsyncSession,
    order_id: int,
    reviewer_id: int,
    rating: int,
    comment: Optional[str] = None,
    photo_url: Optional[str] = None
) -> Review:
    """Create a review for a completed order."""
    # Verify order exists and belongs to reviewer
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    if order.buyer_id != reviewer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to review this order"
        )
    
    if order.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only review completed orders"
        )
    
    # Check if review already exists
    result = await db.execute(select(Review).where(Review.order_id == order_id))
    existing_review = result.scalar_one_or_none()
    
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Review already exists for this order"
        )
    
    # Create review
    review = Review(
        order_id=order_id,
        business_id=order.business_id,
        reviewer_id=reviewer_id,
        rating=rating,
        comment=comment,
        photo_url=photo_url
    )
    
    db.add(review)
    await db.commit()
    await db.refresh(review)
    
    return review


async def get_business_reviews(
    db: AsyncSession,
    business_id: int
) -> List[Review]:
    """Get all visible reviews for a business."""
    result = await db.execute(
        select(Review)
        .where(Review.business_id == business_id)
        .where(Review.is_visible == True)
        .order_by(Review.created_at.desc())
    )
    return result.scalars().all()


async def delete_review(
    db: AsyncSession,
    review_id: int,
    admin_id: int
) -> None:
    """Delete a review (admin only)."""
    result = await db.execute(select(Review).where(Review.id == review_id))
    review = result.scalar_one_or_none()
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    await db.delete(review)
    await db.commit()


async def moderate_review(
    db: AsyncSession,
    review_id: int,
    is_visible: bool,
    admin_id: int
) -> Review:
    """Moderate a review visibility (admin only)."""
    result = await db.execute(select(Review).where(Review.id == review_id))
    review = result.scalar_one_or_none()
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    review.is_visible = is_visible
    await db.commit()
    await db.refresh(review)
    
    return review

