"""Business routes"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.utils.auth import get_current_user, get_current_user_optional, require_admin
from app.schemas.business import (
    BusinessCreate,
    BusinessUpdate,
    BusinessResponse,
    BusinessItemCreate,
    BusinessItemUpdate,
    BusinessItemResponse,
    BusinessPhotoResponse
)
from app.controllers.business_controller import (
    create_business,
    get_business,
    update_business,
    verify_business,
    delete_business,
    add_business_item,
    update_business_item,
    delete_business_item,
    upload_business_photo,
    delete_business_photo
)
from app.utils.auth import get_current_user, require_admin
from app.models.user import User

router = APIRouter()


@router.get("", response_model=list[BusinessResponse])
async def list_businesses_endpoint(
    category: Optional[str] = None,
    verified: Optional[bool] = None,
    distance: Optional[str] = None,
    search: Optional[str] = None,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """List all businesses with filters."""
    from app.controllers.marketplace_controller import list_businesses
    
    user_zone = current_user.address_zone if current_user else None
    businesses = await list_businesses(
        db=db,
        category=category,
        verified=verified,
        distance=distance,
        search=search,
        user_zone=user_zone
    )
    return [BusinessResponse.model_validate(b) for b in businesses]


@router.post("", response_model=BusinessResponse, status_code=201)
async def create_business_endpoint(
    business_data: BusinessCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> BusinessResponse:
    """Create a new business."""
    business = await create_business(
        db=db,
        owner_id=current_user.id,
        name=business_data.name,
        category=business_data.category,
        operating_hours=business_data.operating_hours,
        location_zone=business_data.location_zone,
        description=business_data.description
    )
    return BusinessResponse.model_validate(business)


@router.get("/{id}", response_model=BusinessResponse)
async def get_business_endpoint(
    id: int,
    db: AsyncSession = Depends(get_db)
) -> BusinessResponse:
    """Get business by ID."""
    business = await get_business(db, id)
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    return BusinessResponse.model_validate(business)


@router.put("/{id}", response_model=BusinessResponse)
async def update_business_endpoint(
    id: int,
    business_data: BusinessUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> BusinessResponse:
    """Update business."""
    business = await update_business(
        db=db,
        business_id=id,
        owner_id=current_user.id,
        name=business_data.name,
        category=business_data.category,
        operating_hours=business_data.operating_hours,
        location_zone=business_data.location_zone,
        description=business_data.description,
        is_active=business_data.is_active
    )
    return BusinessResponse.model_validate(business)


@router.post("/{id}/verify", response_model=BusinessResponse)
async def verify_business_endpoint(
    id: int,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
) -> BusinessResponse:
    """Verify business (admin only)."""
    business = await verify_business(db, id, admin.id)
    return BusinessResponse.model_validate(business)


@router.delete("/{id}", status_code=204)
async def delete_business_endpoint(
    id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete (deactivate) a business."""
    await delete_business(db, id, current_user.id)


@router.post("/{id}/items", response_model=BusinessItemResponse, status_code=201)
async def add_business_item_endpoint(
    id: int,
    item_data: BusinessItemCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> BusinessItemResponse:
    """Add an item to a business."""
    item = await add_business_item(
        db=db,
        business_id=id,
        owner_id=current_user.id,
        name=item_data.name,
        price=item_data.price,
        description=item_data.description,
        image_url=item_data.image_url,
        is_available=item_data.is_available
    )
    return BusinessItemResponse.model_validate(item)


@router.put("/{id}/items/{item_id}", response_model=BusinessItemResponse)
async def update_business_item_endpoint(
    id: int,
    item_id: int,
    item_data: BusinessItemUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> BusinessItemResponse:
    """Update a business item."""
    item = await update_business_item(
        db=db,
        business_id=id,
        item_id=item_id,
        owner_id=current_user.id,
        name=item_data.name,
        description=item_data.description,
        price=item_data.price,
        image_url=item_data.image_url,
        is_available=item_data.is_available
    )
    return BusinessItemResponse.model_validate(item)


@router.delete("/{id}/items/{item_id}", status_code=204)
async def delete_business_item_endpoint(
    id: int,
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a business item."""
    await delete_business_item(db, id, item_id, current_user.id)


@router.post("/{id}/photos", response_model=BusinessPhotoResponse, status_code=201)
async def upload_business_photo_endpoint(
    id: int,
    image_url: str,
    is_primary: bool = False,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> BusinessPhotoResponse:
    """Upload a photo for a business."""
    photo = await upload_business_photo(
        db=db,
        business_id=id,
        owner_id=current_user.id,
        image_url=image_url,
        is_primary=is_primary
    )
    return BusinessPhotoResponse.model_validate(photo)


@router.delete("/{id}/photos/{photo_id}", status_code=204)
async def delete_business_photo_endpoint(
    id: int,
    photo_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a business photo."""
    await delete_business_photo(db, id, photo_id, current_user.id)

