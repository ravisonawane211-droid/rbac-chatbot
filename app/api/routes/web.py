"""Web page routes for the public and protected frontend pages."""

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.config.config import get_settings

router = APIRouter(tags=["Web"])
project_root = Path(__file__).resolve().parents[3]
templates = Jinja2Templates(directory=str(project_root / "app" / "templates"))
settings = get_settings()


@router.get("/", include_in_schema=False)
async def landing_page(request: Request):
    """Redirect the root URL to the dedicated Home page."""
    return RedirectResponse(url="/home", status_code=307)


@router.get("/home")
async def home_page(request: Request):
    """Serve the Home page."""
    return templates.TemplateResponse(request, "home.html", {"request": request})


@router.get("/features")
async def features_page(request: Request):
    """Serve the Features page."""
    return templates.TemplateResponse(request, "features.html", {"request": request})


@router.get("/about")
async def about_page(request: Request):
    """Serve the About Us page."""
    return templates.TemplateResponse(request, "about.html", {"request": request})


@router.get("/contact")
async def contact_page(request: Request):
    """Serve the Contact page."""
    return templates.TemplateResponse(request, "contact.html", {"request": request})


@router.get("/login")
async def login_page(request: Request):
    """Serve the login page."""
    return templates.TemplateResponse(request, "login.html", {"request": request})


@router.get("/chat")
async def chat_page(request: Request):
    """Serve the chat page."""
    return templates.TemplateResponse(request, "chat.html", {"request": request})


@router.get("/admin")
async def admin_page(request: Request):
    """Serve the admin page."""
    return templates.TemplateResponse(request, "admin.html", {"request": request})


@router.get("/dashboard")
async def dashboard_page(request: Request):
    """Serve the Dashboard page."""
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "request": request,
            "evaluation_service_url": settings.evaluation_service_url.rstrip("/").removesuffix("/evaluate"),
        },
    )


@router.get("/upload")
async def upload_page(request: Request):
    """Serve the upload page."""
    return templates.TemplateResponse(request, "upload.html", {"request": request})
