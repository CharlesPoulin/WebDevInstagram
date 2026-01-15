from fastapi import FastAPI

from .adapters.inbound.api.images import router as images_router
from .adapters.inbound.api.social import router as social_router
from .adapters.inbound.api.users import router as users_router

app = FastAPI(title="uGram API")

app.include_router(users_router)
app.include_router(images_router)
app.include_router(social_router)


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
