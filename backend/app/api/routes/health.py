from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def healthcheck():
    return {
        "status": "healthy",
        "service": "fluxforge-backend",
    }