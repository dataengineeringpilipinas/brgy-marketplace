"""Web routes for HTML pages"""
from pathlib import Path
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

from app.utils.auth import get_current_user_optional
from app.models.user import User

# Templates
templates_dir = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request, current_user: Optional[User] = Depends(get_current_user_optional)):
    """Marketplace homepage."""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "current_user": current_user
    })


@router.get("/businesses", response_class=HTMLResponse)
async def business_list(request: Request, current_user: Optional[User] = Depends(get_current_user_optional)):
    """Business listings page."""
    return templates.TemplateResponse("business_list.html", {
        "request": request,
        "current_user": current_user
    })


@router.get("/businesses/{id}", response_class=HTMLResponse)
async def business_detail(request: Request, id: int, current_user: Optional[User] = Depends(get_current_user_optional)):
    """Business detail page."""
    return templates.TemplateResponse("business_detail.html", {
        "request": request,
        "business_id": id,
        "current_user": current_user
    })


@router.get("/orders", response_class=HTMLResponse)
async def orders_list(request: Request, current_user: Optional[User] = Depends(get_current_user_optional)):
    """User orders page."""
    if not current_user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("orders_list.html", {
        "request": request,
        "current_user": current_user
    })


@router.get("/orders/{id}", response_class=HTMLResponse)
async def order_detail(request: Request, id: int, current_user: Optional[User] = Depends(get_current_user_optional)):
    """Order detail page."""
    if not current_user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("order_detail.html", {
        "request": request,
        "order_id": id,
        "current_user": current_user
    })


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, current_user: Optional[User] = Depends(get_current_user_optional)):
    """Analytics dashboard (admin only)."""
    if not current_user or current_user.role != "admin":
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/")
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "current_user": current_user
    })


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Registration page."""
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page."""
    return templates.TemplateResponse("login.html", {"request": request})

