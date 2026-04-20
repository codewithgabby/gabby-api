from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.db.session import engine
from app.db.base import Base

from app.routers import consultation, contact, product, service, tip, faq, success_story, profile

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI()

# Rate limiter state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # React/Next.js default
        "http://localhost:5173",      # Vite default
        "http://localhost:5500",      # Live Server default
        "http://127.0.0.1:5500",      # Live Server alternative
        "http://localhost:8080",      # Common dev port
        "https://yourportfolio.com",  # REPLACE WITH YOUR ACTUAL DOMAIN
        "https://www.yourportfolio.com",
        "https://gabby-api-production.up.railway.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
# Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(profile.router)
app.include_router(contact.router)
app.include_router(consultation.router)
app.include_router(product.router)
app.include_router(service.router)
app.include_router(tip.router)
app.include_router(faq.router)
app.include_router(success_story.router)


@app.get("/")
def root():
    return {"message": "Johnson API is running"}


