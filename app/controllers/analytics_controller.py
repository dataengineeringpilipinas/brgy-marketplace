"""
Analytics controller
"""
from datetime import datetime, timedelta
from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func
from sqlalchemy import extract

from app.models.business import Business
from app.models.order import Order
from app.models.analytics import AnalyticsEvent


async def get_business_stats(db: AsyncSession) -> Dict[str, int]:
    """Get business statistics."""
    total = await db.execute(select(func.count(Business.id)))
    total_count = total.scalar() or 0
    
    active = await db.execute(
        select(func.count(Business.id)).where(Business.is_active == True)
    )
    active_count = active.scalar() or 0
    
    verified = await db.execute(
        select(func.count(Business.id)).where(Business.is_verified == True)
    )
    verified_count = verified.scalar() or 0
    
    return {
        "total_businesses": total_count,
        "active_businesses": active_count,
        "verified_businesses": verified_count
    }


async def get_category_stats(db: AsyncSession) -> List[Dict[str, any]]:
    """Get statistics by category."""
    # Get total businesses for percentage calculation
    total_result = await db.execute(select(func.count(Business.id)))
    total = total_result.scalar() or 1
    
    # Get count by category
    result = await db.execute(
        select(Business.category, func.count(Business.id).label("count"))
        .where(Business.is_active == True)
        .group_by(Business.category)
        .order_by(func.count(Business.id).desc())
    )
    
    stats = []
    for row in result.all():
        percentage = (row.count / total) * 100 if total > 0 else 0
        stats.append({
            "category": row.category,
            "count": row.count,
            "percentage": round(percentage, 2)
        })
    
    return stats


async def get_search_stats(db: AsyncSession, limit: int = 10) -> List[Dict[str, any]]:
    """Get top search terms."""
    result = await db.execute(
        select(
            AnalyticsEvent.search_term,
            func.count(AnalyticsEvent.id).label("count")
        )
        .where(AnalyticsEvent.event_type == "search")
        .where(AnalyticsEvent.search_term.isnot(None))
        .group_by(AnalyticsEvent.search_term)
        .order_by(func.count(AnalyticsEvent.id).desc())
        .limit(limit)
    )
    
    return [
        {"search_term": row.search_term, "count": row.count}
        for row in result.all()
    ]


async def get_order_stats(db: AsyncSession) -> Dict[str, int]:
    """Get order statistics."""
    total_result = await db.execute(select(func.count(Order.id)))
    total = total_result.scalar() or 0
    
    # Orders by status
    status_result = await db.execute(
        select(Order.status, func.count(Order.id).label("count"))
        .group_by(Order.status)
    )
    
    orders_by_status = {}
    for row in status_result.all():
        orders_by_status[row.status] = row.count
    
    return {
        "total_orders": total,
        "orders_by_status": orders_by_status
    }


async def get_time_stats(db: AsyncSession) -> List[Dict[str, any]]:
    """Get order statistics by hour of day."""
    # Get orders from last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    result = await db.execute(
        select(
            extract("hour", Order.created_at).label("hour"),
            func.count(Order.id).label("count")
        )
        .where(Order.created_at >= thirty_days_ago)
        .group_by(extract("hour", Order.created_at))
        .order_by(extract("hour", Order.created_at))
    )
    
    # Create a dict for all 24 hours, defaulting to 0
    hour_counts = {hour: 0 for hour in range(24)}
    for row in result.all():
        hour_counts[int(row.hour)] = row.count
    
    return [
        {"hour": hour, "count": count}
        for hour, count in sorted(hour_counts.items())
    ]


async def get_dashboard_stats(db: AsyncSession) -> Dict[str, any]:
    """Get all dashboard statistics."""
    business_stats = await get_business_stats(db)
    category_stats = await get_category_stats(db)
    search_stats = await get_search_stats(db)
    order_stats = await get_order_stats(db)
    time_stats = await get_time_stats(db)
    
    return {
        **business_stats,
        "category_stats": category_stats,
        "top_searches": search_stats,
        "orders_by_hour": time_stats,
        "orders_by_status": order_stats.get("orders_by_status", {}),
        "total_orders": order_stats.get("total_orders", 0)
    }

