from fastapi import FastAPI

from .adapters.inbound.api.images import router as images_router
from .adapters.inbound.api.social import router as social_router
from .adapters.inbound.api.users import router as users_router
from .adapters.outbound.persistence.database import create_tables

app = FastAPI(
    title="uGram API",
    description="Instagram-like application backend with user profiles, images, and social features",
    version="1.0.0",
)

# Create database tables on startup
create_tables()

app.include_router(users_router)
app.include_router(images_router)
app.include_router(social_router)


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
