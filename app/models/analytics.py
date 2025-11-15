"""
Analytics model
"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class AnalyticsEvent(SQLModel, table=True):
    """Analytics event tracking model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    event_type: str  # business_view, search, order_created, etc.
    business_id: Optional[int] = Field(default=None, foreign_key="business.id")
    category: Optional[str] = None  # Business category
    search_term: Optional[str] = None  # For search events
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)

