"""
Analytics schemas
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel


class CategoryStats(BaseModel):
    """Category statistics."""
    category: str
    count: int
    percentage: float


class SearchStats(BaseModel):
    """Search statistics."""
    search_term: str
    count: int


class TimeStats(BaseModel):
    """Time-based statistics."""
    hour: int
    count: int


class DashboardStats(BaseModel):
    """Dashboard statistics."""
    total_businesses: int
    active_businesses: int
    verified_businesses: int
    total_orders: int
    category_stats: List[CategoryStats]
    top_searches: List[SearchStats]
    orders_by_hour: List[TimeStats]
    orders_by_status: Dict[str, int]

