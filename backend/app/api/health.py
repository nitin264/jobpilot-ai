from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings

router = APIRouter(tags=["system"])


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy"}


@router.get("/ready")
async def ready(settings: Settings = Depends(get_settings)) -> dict[str, str]:
    return {
        "status": "ready",
        "environment": settings.environment,
    }
