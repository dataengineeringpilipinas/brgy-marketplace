"""Review routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.review import ReviewCreate, ReviewResponse
from app.controllers.review_controller import (
    create_review,
    get_business_reviews,
    delete_review,
    moderate_review
)
from app.utils.auth import get_current_user, require_admin
from app.models.user import User

router = APIRouter()


@router.get("/businesses/{business_id}", response_model=list[ReviewResponse])
async def get_business_reviews_endpoint(
    business_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get reviews for a business."""
    reviews = await get_business_reviews(db, business_id)
    
    # Enrich with reviewer names
    enriched_reviews = []
    for review in reviews:
        from sqlmodel import select
        result = await db.execute(select(User).where(User.id == review.reviewer_id))
        reviewer = result.scalar_one_or_none()
        
        enriched_reviews.append(ReviewResponse(
            id=review.id,
            order_id=review.order_id,
            business_id=review.business_id,
            reviewer_id=review.reviewer_id,
            reviewer_name=reviewer.full_name if reviewer else None,
            rating=review.rating,
            comment=review.comment,
            photo_url=review.photo_url,
            created_at=review.created_at,
            is_visible=review.is_visible
        ))
    
    return enriched_reviews


@router.post("/orders/{order_id}", response_model=ReviewResponse, status_code=201)
async def create_review_endpoint(
    order_id: int,
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> ReviewResponse:
    """Create a review for an order."""
    review = await create_review(
        db=db,
        order_id=order_id,
        reviewer_id=current_user.id,
        rating=review_data.rating,
        comment=review_data.comment,
        photo_url=review_data.photo_url
    )
    
    return ReviewResponse(
        id=review.id,
        order_id=review.order_id,
        business_id=review.business_id,
        reviewer_id=review.reviewer_id,
        reviewer_name=current_user.full_name,
        rating=review.rating,
        comment=review.comment,
        photo_url=review.photo_url,
        created_at=review.created_at,
        is_visible=review.is_visible
    )


@router.delete("/{id}", status_code=204)
async def delete_review_endpoint(
    id: int,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Delete a review (admin only)."""
    await delete_review(db, id, admin.id)
