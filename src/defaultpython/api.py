import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .config import get_settings
from .main import main as run_main_logic

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    """
    Lifecycle manager for the FastAPI app.
    Startup and Shutdown logic goes here.
    """
    # Startup logic
    settings = get_settings()
    logger.info(
        "Starting %s in %s mode...", settings.PROJECT_NAME, settings.ENVIRONMENT
    )

    yield

    # Shutdown logic
    logger.info("Shutting down %s...", settings.PROJECT_NAME)


def create_app() -> FastAPI:
    """Factory function to create the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        lifespan=lifespan,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
    )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Global exception handler to return consistent JSON errors."""
        logger.exception(
            "Unhandled exception: %s", exc, extra={"path": request.url.path}
        )

        # Don't expose internal error details in production
        error_detail = str(exc) if settings.DEBUG else "Internal Server Error"

        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error", "error": error_detail},
        )

    @app.get("/health")
    async def health_check() -> dict[str, str]:
        """Health check endpoint for probes."""
        return {"status": "ok", "version": settings.VERSION}

    @app.get("/")
    async def root() -> dict[str, str]:
        """Root endpoint example."""
        return {"message": f"Hello from {settings.PROJECT_NAME} API"}

    @app.get("/run")
    async def trigger_run() -> dict[str, str]:
        """Trigger the main logic via API."""
        run_main_logic()
        return {"status": "Main logic executed"}

    return app


app = create_app()
