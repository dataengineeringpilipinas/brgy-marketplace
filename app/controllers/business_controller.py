"""
Business controller
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi import HTTPException, status

from app.models.business import Business, BusinessItem, BusinessPhoto
from app.models.user import User


async def create_business(
    db: AsyncSession,
    owner_id: int,
    name: str,
    category: str,
    operating_hours: Optional[str] = None,
    location_zone: Optional[str] = None,
    description: Optional[str] = None
) -> Business:
    """Create a new business."""
    business = Business(
        owner_id=owner_id,
        name=name,
        category=category,
        operating_hours=operating_hours,
        location_zone=location_zone,
        description=description
    )
    
    db.add(business)
    await db.commit()
    await db.refresh(business)
    
    return business


async def get_business(
    db: AsyncSession,
    business_id: int
) -> Optional[Business]:
    """Get a business by ID."""
    result = await db.execute(
        select(Business)
        .where(Business.id == business_id)
        .where(Business.is_active == True)
    )
    return result.scalar_one_or_none()


async def update_business(
    db: AsyncSession,
    business_id: int,
    owner_id: int,
    name: Optional[str] = None,
    category: Optional[str] = None,
    operating_hours: Optional[str] = None,
    location_zone: Optional[str] = None,
    description: Optional[str] = None,
    is_active: Optional[bool] = None
) -> Business:
    """Update a business."""
    business = await get_business(db, business_id)
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    if business.owner_id != owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this business"
        )
    
    if name is not None:
        business.name = name
    if category is not None:
        business.category = category
    if operating_hours is not None:
        business.operating_hours = operating_hours
    if location_zone is not None:
        business.location_zone = location_zone
    if description is not None:
        business.description = description
    if is_active is not None:
        business.is_active = is_active
    
    await db.commit()
    await db.refresh(business)
    
    return business


async def verify_business(
    db: AsyncSession,
    business_id: int,
    admin_id: int
) -> Business:
    """Verify a business (admin only)."""
    business = await get_business(db, business_id)
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    business.is_verified = True
    business.verified_at = datetime.utcnow()
    business.verified_by = admin_id
    
    await db.commit()
    await db.refresh(business)
    
    return business


async def delete_business(
    db: AsyncSession,
    business_id: int,
    owner_id: int
) -> None:
    """Delete (deactivate) a business."""
    business = await get_business(db, business_id)
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    if business.owner_id != owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this business"
        )
    
    business.is_active = False
    await db.commit()


async def add_business_item(
    db: AsyncSession,
    business_id: int,
    owner_id: int,
    name: str,
    price: float,
    description: Optional[str] = None,
    image_url: Optional[str] = None,
    is_available: bool = True
) -> BusinessItem:
    """Add an item to a business."""
    business = await get_business(db, business_id)
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    if business.owner_id != owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add items to this business"
        )
    
    item = BusinessItem(
        business_id=business_id,
        name=name,
        description=description,
        price=price,
        image_url=image_url,
        is_available=is_available
    )
    
    db.add(item)
    await db.commit()
    await db.refresh(item)
    
    return item


async def update_business_item(
    db: AsyncSession,
    business_id: int,
    item_id: int,
    owner_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    price: Optional[float] = None,
    image_url: Optional[str] = None,
    is_available: Optional[bool] = None
) -> BusinessItem:
    """Update a business item."""
    business = await get_business(db, business_id)
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    if business.owner_id != owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update items for this business"
        )
    
    result = await db.execute(
        select(BusinessItem).where(BusinessItem.id == item_id)
    )
    item = result.scalar_one_or_none()
    
    if not item or item.business_id != business_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    if name is not None:
        item.name = name
    if description is not None:
        item.description = description
    if price is not None:
        item.price = price
    if image_url is not None:
        item.image_url = image_url
    if is_available is not None:
        item.is_available = is_available
    
    await db.commit()
    await db.refresh(item)
    
    return item


async def delete_business_item(
    db: AsyncSession,
    business_id: int,
    item_id: int,
    owner_id: int
) -> None:
    """Delete a business item."""
    business = await get_business(db, business_id)
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    if business.owner_id != owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete items for this business"
        )
    
    result = await db.execute(
        select(BusinessItem).where(BusinessItem.id == item_id)
    )
    item = result.scalar_one_or_none()
    
    if not item or item.business_id != business_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    await db.delete(item)
    await db.commit()


async def upload_business_photo(
    db: AsyncSession,
    business_id: int,
    owner_id: int,
    image_url: str,
    is_primary: bool = False
) -> BusinessPhoto:
    """Upload a photo for a business."""
    business = await get_business(db, business_id)
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    if business.owner_id != owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to upload photos for this business"
        )
    
    # If this is set as primary, unset other primary photos
    if is_primary:
        result = await db.execute(
            select(BusinessPhoto).where(
                BusinessPhoto.business_id == business_id,
                BusinessPhoto.is_primary == True
            )
        )
        existing_primary = result.scalars().all()
        for photo in existing_primary:
            photo.is_primary = False
    
    photo = BusinessPhoto(
        business_id=business_id,
        image_url=image_url,
        is_primary=is_primary
    )
    
    db.add(photo)
    await db.commit()
    await db.refresh(photo)
    
    return photo


async def delete_business_photo(
    db: AsyncSession,
    business_id: int,
    photo_id: int,
    owner_id: int
) -> None:
    """Delete a business photo."""
    business = await get_business(db, business_id)
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    if business.owner_id != owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete photos for this business"
        )
    
    result = await db.execute(
        select(BusinessPhoto).where(BusinessPhoto.id == photo_id)
    )
    photo = result.scalar_one_or_none()
    
    if not photo or photo.business_id != business_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Photo not found"
        )
    
    await db.delete(photo)
    await db.commit()

