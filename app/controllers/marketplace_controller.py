"""
Marketplace listing controller
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, or_
from sqlalchemy import func

from app.models.business import Business, BusinessItem, BusinessPhoto
from app.models.analytics import AnalyticsEvent
from app.utils.distance import filter_by_distance


async def list_businesses(
    db: AsyncSession,
    category: Optional[str] = None,
    verified: Optional[bool] = None,
    distance: Optional[str] = None,  # "200m" or "500m"
    search: Optional[str] = None,
    user_zone: Optional[str] = None
) -> List[Business]:
    """List businesses with filters."""
    query = (
        select(Business)
        .where(Business.is_active == True)
        .options(
            selectinload(Business.items),
            selectinload(Business.photos)
        )
    )
    
    # Category filter
    if category:
        query = query.where(Business.category == category)
    
    # Verified filter
    if verified is not None:
        query = query.where(Business.is_verified == verified)
    
    # Search filter
    if search:
        search_term = f"%{search.lower()}%"
        query = query.where(
            or_(
                func.lower(Business.name).like(search_term),
                func.lower(Business.description).like(search_term)
            )
        )
        
        # Track search for analytics
        event = AnalyticsEvent(
            event_type="search",
            search_term=search,
            category=category
        )
        db.add(event)
        await db.commit()
    
    result = await db.execute(query)
    businesses = result.scalars().all()
    
    # Distance filter (after fetching)
    if distance and user_zone:
        max_distance = float(distance.replace("m", ""))
        business_zones = [(b.id, b.location_zone) for b in businesses]
        filtered_ids = filter_by_distance(user_zone, business_zones, max_distance)
        businesses = [b for b in businesses if b.id in filtered_ids]
    
    return businesses


async def track_business_view(
    db: AsyncSession,
    business_id: int,
    category: Optional[str] = None
) -> None:
    """Track a business view for analytics."""
    event = AnalyticsEvent(
        event_type="business_view",
        business_id=business_id,
        category=category
    )
    db.add(event)
    await db.commit()

