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
from fastapi.responses import JSONResponse

from app.api.routes import document, health, query, user, dashboard
from app.config.config import get_settings
from app.utils.logger import get_logger, setup_logging

import subprocess
import sys
import time

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    setup_logging(settings.log_level)
    logger = get_logger(__name__)
    logger.info(f"Starting {settings.app_name}")
    logger.info(f"Log level: {settings.log_level}")

    yield

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


# Include routers
app.include_router(health.router)
app.include_router(document.router)
app.include_router(query.router)
app.include_router(user.router)
app.include_router(dashboard.router)


@app.get("/", tags=["Root"])
async def root():
    """Serve the main UI."""
  
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
    public_port = os.environ.get("PORT", "8501")

    # Start Streamlit in background on port 8502
    streamlit_proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "./ui/01_Login.py", "--server.port", "8002"],
        cwd=str(project_root),
    )

    # Give Streamlit a moment to start (optional)
    time.sleep(1)

    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
    )
