from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.db.session import engine
from app.db.base import Base

from app.routers import consultation, contact, product, service, tip, faq, success_story, profile, upload

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI()

# ==========================================
# FORCE HTTPS REDIRECT FIX FOR RAILWAY
# ==========================================

class ForceHTTPSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if response.status_code in (307, 308) and "location" in response.headers:
            location = response.headers["location"]
            if location.startswith("http://"):
                response.headers["location"] = location.replace("http://", "https://", 1)
        return response

app.add_middleware(ForceHTTPSMiddleware)

# ==========================================
# RATE LIMITER
# ==========================================

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ==========================================
# CORS CONFIGURATION
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "https://yourportfolio.com",
        "https://www.yourportfolio.com",
        "https://gabby-api-production.up.railway.app",
        "https://johnsongabby.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# ROUTERS
# ==========================================

app.include_router(profile.router)
app.include_router(contact.router)
app.include_router(consultation.router)
app.include_router(product.router)
app.include_router(service.router)
app.include_router(tip.router)
app.include_router(faq.router)
app.include_router(success_story.router)
app.include_router(upload.router)


@app.get("/")
def root():
    return {"message": "Johnson API is running"}