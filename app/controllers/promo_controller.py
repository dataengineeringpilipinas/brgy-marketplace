"""
Promo controller
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi import HTTPException, status

from app.models.promo import Promo
from app.models.business import Business


async def create_promo(
    db: AsyncSession,
    admin_id: int,
    business_id: Optional[int],
    title: str,
    promo_type: str,
    start_date: datetime,
    description: Optional[str] = None,
    image_url: Optional[str] = None,
    end_date: Optional[datetime] = None
) -> Promo:
    """Create a promo (admin only)."""
    # Verify business exists if provided
    if business_id:
        result = await db.execute(select(Business).where(Business.id == business_id))
        business = result.scalar_one_or_none()
        
        if not business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business not found"
            )
    
    promo = Promo(
        business_id=business_id,
        title=title,
        description=description,
        image_url=image_url,
        promo_type=promo_type,
        start_date=start_date,
        end_date=end_date,
        created_by=admin_id
    )
    
    db.add(promo)
    await db.commit()
    await db.refresh(promo)
    
    return promo


async def list_promos(
    db: AsyncSession,
    promo_type: Optional[str] = None,
    active_only: bool = True
) -> List[Promo]:
    """List promos."""
    query = select(Promo)
    
    if promo_type:
        query = query.where(Promo.promo_type == promo_type)
    
    if active_only:
        now = datetime.utcnow()
        query = query.where(
            Promo.start_date <= now,
            (Promo.end_date.is_(None)) | (Promo.end_date >= now)
        )
    
    query = query.order_by(Promo.start_date.desc())
    
    result = await db.execute(query)
    return result.scalars().all()


async def update_promo(
    db: AsyncSession,
    promo_id: int,
    admin_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    image_url: Optional[str] = None,
    promo_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> Promo:
    """Update a promo (admin only)."""
    result = await db.execute(select(Promo).where(Promo.id == promo_id))
    promo = result.scalar_one_or_none()
    
    if not promo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Promo not found"
        )
    
    if title is not None:
        promo.title = title
    if description is not None:
        promo.description = description
    if image_url is not None:
        promo.image_url = image_url
    if promo_type is not None:
        promo.promo_type = promo_type
    if start_date is not None:
        promo.start_date = start_date
    if end_date is not None:
        promo.end_date = end_date
    
    await db.commit()
    await db.refresh(promo)
    
    return promo


async def delete_promo(
    db: AsyncSession,
    promo_id: int,
    admin_id: int
) -> None:
    """Delete a promo (admin only)."""
    result = await db.execute(select(Promo).where(Promo.id == promo_id))
    promo = result.scalar_one_or_none()
    
    if not promo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Promo not found"
        )
    
    await db.delete(promo)
    await db.commit()

