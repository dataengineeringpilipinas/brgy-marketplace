"""Promo routes"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.promo import PromoCreate, PromoUpdate, PromoResponse
from app.controllers.promo_controller import (
    create_promo,
    list_promos,
    update_promo,
    delete_promo
)
from app.utils.auth import get_current_user, require_admin
from app.models.user import User

router = APIRouter()


@router.get("", response_model=list[PromoResponse])
async def list_promos_endpoint(
    promo_type: Optional[str] = None,
    active_only: bool = True,
    db: AsyncSession = Depends(get_db)
):
    """List all promos."""
    promos = await list_promos(db, promo_type, active_only)
    
    # Enrich with business names
    enriched_promos = []
    for promo in promos:
        business_name = None
        if promo.business_id:
            from sqlmodel import select
            from app.models.business import Business
            
            result = await db.execute(select(Business).where(Business.id == promo.business_id))
            business = result.scalar_one_or_none()
            business_name = business.name if business else None
        
        enriched_promos.append(PromoResponse(
            id=promo.id,
            business_id=promo.business_id,
            business_name=business_name,
            title=promo.title,
            description=promo.description,
            image_url=promo.image_url,
            promo_type=promo.promo_type,
            start_date=promo.start_date,
            end_date=promo.end_date,
            created_at=promo.created_at
        ))
    
    return enriched_promos


@router.post("", response_model=PromoResponse, status_code=201)
async def create_promo_endpoint(
    promo_data: PromoCreate,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
) -> PromoResponse:
    """Create a promo (admin only)."""
    promo = await create_promo(
        db=db,
        admin_id=admin.id,
        business_id=promo_data.business_id,
        title=promo_data.title,
        description=promo_data.description,
        image_url=promo_data.image_url,
        promo_type=promo_data.promo_type,
        start_date=promo_data.start_date,
        end_date=promo_data.end_date
    )
    
    # Enrich response
    business_name = None
    if promo.business_id:
        from sqlmodel import select
        from app.models.business import Business
        
        result = await db.execute(select(Business).where(Business.id == promo.business_id))
        business = result.scalar_one_or_none()
        business_name = business.name if business else None
    
    return PromoResponse(
        id=promo.id,
        business_id=promo.business_id,
        business_name=business_name,
        title=promo.title,
        description=promo.description,
        image_url=promo.image_url,
        promo_type=promo.promo_type,
        start_date=promo.start_date,
        end_date=promo.end_date,
        created_at=promo.created_at
    )


@router.put("/{id}", response_model=PromoResponse)
async def update_promo_endpoint(
    id: int,
    promo_data: PromoUpdate,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
) -> PromoResponse:
    """Update promo (admin only)."""
    promo = await update_promo(
        db=db,
        promo_id=id,
        admin_id=admin.id,
        title=promo_data.title,
        description=promo_data.description,
        image_url=promo_data.image_url,
        promo_type=promo_data.promo_type,
        start_date=promo_data.start_date,
        end_date=promo_data.end_date
    )
    
    # Enrich response
    business_name = None
    if promo.business_id:
        from sqlmodel import select
        from app.models.business import Business
        
        result = await db.execute(select(Business).where(Business.id == promo.business_id))
        business = result.scalar_one_or_none()
        business_name = business.name if business else None
    
    return PromoResponse(
        id=promo.id,
        business_id=promo.business_id,
        business_name=business_name,
        title=promo.title,
        description=promo.description,
        image_url=promo.image_url,
        promo_type=promo.promo_type,
        start_date=promo.start_date,
        end_date=promo.end_date,
        created_at=promo.created_at
    )


@router.delete("/{id}", status_code=204)
async def delete_promo_endpoint(
    id: int,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Delete promo (admin only)."""
    await delete_promo(db, id, admin.id)
