from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from app.core.config import ADMIN_API_KEY
from app.db.session import SessionLocal

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_admin(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key missing. Please include X-API-Key header."
        )
    
    if api_key != ADMIN_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key."
        )
    
    return api_key


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()