"""FastAPI application entry point."""

from dotenv import load_dotenv
import os

load_dotenv()
import sys
from pathlib import Path

# When running app/main.py directly (e.g. `python app/main.py`), Python
# doesn't treat `app` as an installed package, so `from app import ...`
# fails. Add project root to sys.path as a fallback so package imports work
# when invoked directly (this keeps behavior consistent for debugging).
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routes import document, health, query, user, dashboard
from app.config.config import get_settings
from app.utils.logger import get_logger, setup_logging

settings = get_settings()
templates = Jinja2Templates(directory=str(project_root / "app" / "templates"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    setup_logging(settings.log_level)
    logger = get_logger(__name__)
    logger.info(f"Starting {settings.app_name}")
    logger.info(f"Log level: {settings.log_level}")

    yield

    try:
        from langfuse import get_client

        get_client().flush()
    except Exception:  # pragma: no cover - optional observability dependency
        pass

    # Shutdown
    logger.info("Shutting down application")



# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="""
## RAG Q&A System API

A Retrieval-Augmented Generation (RAG) question-answering system built with:
- **FastAPI** for the API layer
- **LangChain** for RAG orchestration
- **Qdrant Cloud** for vector storage
- **OpenAI** for embeddings and LLM

### Features
- Upload PDF, TXT, and CSV documents
- Ask questions and get AI-powered answers
- View source documents for transparency
- Streaming responses for real-time feedback
    """,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Serve frontend static assets
app.mount("/static", StaticFiles(directory=str(project_root / "app" / "static")), name="static")

# Include routers
app.include_router(health.router)
app.include_router(document.router)
app.include_router(query.router)
app.include_router(user.router)
app.include_router(dashboard.router)


@app.middleware("http")
async def auth_redirect_middleware(request: Request, call_next):
    """Redirect unauthenticated users away from protected frontend pages."""
    protected_paths = {"/chat", "/admin", "/dashboard", "/upload"}
    if request.url.path in protected_paths:
        token = request.cookies.get("access_token")
        if not token:
            redirect_url = request.url_for("login_page")
            return RedirectResponse(url=str(redirect_url), status_code=307)

    return await call_next(request)


@app.get("/", tags=["Web"])
async def landing_page(request: Request):
    """Redirect the root URL to the dedicated Home page."""
    return RedirectResponse(url="/home", status_code=307)


@app.get("/home", tags=["Web"])
async def home_page(request: Request):
    """Serve the Home page."""
    return templates.TemplateResponse(request, "home.html", {"request": request})


@app.get("/features", tags=["Web"])
async def features_page(request: Request):
    """Serve the Features page."""
    return templates.TemplateResponse(request, "features.html", {"request": request})


@app.get("/about", tags=["Web"])
async def about_page(request: Request):
    """Serve the About Us page."""
    return templates.TemplateResponse(request, "about.html", {"request": request})


@app.get("/contact", tags=["Web"])
async def contact_page(request: Request):
    """Serve the Contact page."""
    return templates.TemplateResponse(request, "contact.html", {"request": request})


@app.get("/login", tags=["Web"])
async def login_page(request: Request):
    """Serve the login page."""
    return templates.TemplateResponse(request, "login.html", {"request": request})


@app.get("/chat", tags=["Web"])
async def chat_page(request: Request):
    """Serve the chat page."""
    return templates.TemplateResponse(request, "chat.html", {"request": request})


@app.get("/admin", tags=["Web"])
async def admin_page(request: Request):
    """Serve the admin page."""
    return templates.TemplateResponse(request, "admin.html", {"request": request})


@app.get("/dashboard", tags=["Web"])
async def dashboard_page(request: Request):
    """Serve the dashboard page."""
    return templates.TemplateResponse(request, "dashboard.html", {"request": request})


@app.get("/upload", tags=["Web"])
async def upload_page(request: Request):
    """Serve the upload page."""
    return templates.TemplateResponse(request, "upload.html", {"request": request})


@app.get("/api", tags=["Root"])
async def root():
    """Serve API metadata."""
    return {"message": "Welcome to the ChatBot API. Visit /docs for API documentation."}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger = get_logger(__name__)
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
        },
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=False,
    )
