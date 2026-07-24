from fastapi import APIRouter, Depends

from app.dependencies import verify_admin

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/verify")
async def verify_admin_access(_: str = Depends(verify_admin)):
    """
    Verify that the supplied X-API-Key is valid.
    Used by the admin login page and dashboard.
    """
    return {
        "authenticated": True,
        "message": "Authentication successful."
    }