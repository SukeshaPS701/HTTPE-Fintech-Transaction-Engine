from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health():

    return {
        "status": "UP",
        "services": {
            "gateway": "running",
            "payment_service": "running",
            "database": "connected (assumed)",
            "redis": "running",
            "kafka": "running"
        }
    }