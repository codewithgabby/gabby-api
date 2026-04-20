# Johnson Portfolio API

Backend API for my personal portfolio showcasing immigration consulting services, products, success stories, and immigration tips.

## Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- SlowAPI (rate limiting)

## Setup

1. Clone the repo
2. Create virtual environment: `python -m venv env`
3. Activate: `env\Scripts\activate` (Windows) or `source env/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Create `.env` file with:

## DATABASE_URL=postgresql://...
## ADMIN_API_KEY=your_secret_key

6. Run migrations: `alembic upgrade head`
7. Start server: `uvicorn app.main:app --reload`

## API Docs
Visit `/docs` for Swagger UI documentation.