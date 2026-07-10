from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse

from app.schemas.redirect import RedirectCreate, RedirectUpdate, RedirectResponse
from app.services.redirect_service import (
    create_redirect,
    get_all_redirects,
    get_redirect_by_slug,
    get_redirect_by_id,
    increment_click_count,
    update_redirect,
    delete_redirect
)
from app.dependencies import verify_admin, get_db

router = APIRouter(prefix="/go", tags=["Redirect"])


# ==========================================
# PUBLIC ROUTE - Landing Page
# ==========================================

@router.get("/{slug}", response_class=HTMLResponse)
def redirect_landing_page(
    slug: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Public: Show branded landing page before redirecting"""
    redirect = get_redirect_by_slug(db, slug)
    
    if not redirect:
        raise HTTPException(status_code=404, detail="Redirect not found")
    
    # Increment click count
    increment_click_count(db, redirect)
    
    # Build the landing page HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{redirect.title} | Johnson Gabriel</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background: #0f0f12;
                color: #f0f0f0;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                padding: 20px;
            }}
            
            .redirect-card {{
                background: #1a1a1f;
                border-radius: 32px;
                padding: 48px 40px;
                max-width: 560px;
                width: 100%;
                text-align: center;
                border: 1px solid #2a2a30;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            }}
            
            .redirect-image {{
                width: 80px;
                height: 80px;
                border-radius: 50%;
                object-fit: cover;
                border: 3px solid #0f766e;
                margin-bottom: 24px;
            }}
            
            .redirect-title {{
                font-size: 28px;
                font-weight: 800;
                letter-spacing: -0.5px;
                margin-bottom: 16px;
                color: #ffffff;
            }}
            
            .redirect-description {{
                font-size: 16px;
                color: #a0a0a8;
                line-height: 1.7;
                margin-bottom: 32px;
            }}
            
            .redirect-btn {{
                display: inline-block;
                padding: 16px 36px;
                background: #0f766e;
                color: white;
                border-radius: 100px;
                text-decoration: none;
                font-weight: 600;
                font-size: 16px;
                transition: all 0.2s;
                border: none;
                cursor: pointer;
            }}
            
            .redirect-btn:hover {{
                background: #0a5c55;
                transform: translateY(-2px);
            }}
            
            .countdown-section {{
                margin-top: 32px;
                padding-top: 24px;
                border-top: 1px solid #2a2a30;
            }}
            
            .countdown-text {{
                font-size: 14px;
                color: #6a6a7a;
                margin-bottom: 12px;
            }}
            
            .progress-bar {{
                width: 100%;
                height: 4px;
                background: #2a2a30;
                border-radius: 2px;
                overflow: hidden;
            }}
            
            .progress-fill {{
                height: 100%;
                background: #0f766e;
                width: 0%;
                transition: width 0.1s linear;
            }}
            
            .redirect-footer {{
                margin-top: 24px;
                font-size: 14px;
                color: #4a4a5a;
            }}
            
            .redirect-footer a {{
                color: #0f766e;
                text-decoration: none;
            }}
            
            .redirect-footer a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="redirect-card">
            {('<img src="' + redirect.image_url + '" alt="Johnson Gabriel" class="redirect-image">') if redirect.image_url else ''}
            <h1 class="redirect-title">{redirect.title}</h1>
            <p class="redirect-description">{redirect.description or ''}</p>
            <a href="{redirect.destination_url}" class="redirect-btn">{redirect.button_text} →</a>
            
            <div class="countdown-section">
                <p class="countdown-text">Redirecting in <span id="countdown">{redirect.redirect_seconds}</span> seconds...</p>
                <div class="progress-bar">
                    <div class="progress-fill" id="progress-fill"></div>
                </div>
            </div>
            
            <div class="redirect-footer">
                <p>Powered by <a href="/">Johnson Gabriel</a></p>
            </div>
        </div>
        
        <script>
            const totalSeconds = {redirect.redirect_seconds};
            const destinationUrl = "{redirect.destination_url}";
            let remaining = totalSeconds;
            
            const countdownEl = document.getElementById('countdown');
            const progressFill = document.getElementById('progress-fill');
            
            const interval = setInterval(() => {{
                remaining--;
                countdownEl.textContent = remaining;
                
                const progressPercent = ((totalSeconds - remaining) / totalSeconds) * 100;
                progressFill.style.width = progressPercent + '%';
                
                if (remaining <= 0) {{
                    clearInterval(interval);
                    window.location.href = destinationUrl;
                }}
            }}, 1000);
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)


# ==========================================
# ADMIN ROUTES
# ==========================================

@router.get("/admin/redirects", response_model=list[RedirectResponse])
def get_redirects_admin(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    """Admin: Get all redirects with pagination"""
    return get_all_redirects(db, page=page, limit=limit)


@router.post("/admin/redirects", response_model=RedirectResponse)
def create_redirect_endpoint(
    data: RedirectCreate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    """Admin: Create a new redirect"""
    # Check if slug already exists
    existing = get_redirect_by_slug(db, data.slug)
    if existing:
        raise HTTPException(status_code=400, detail="Slug already exists")
    
    return create_redirect(db, data)


@router.put("/admin/redirects/{redirect_id}", response_model=RedirectResponse)
def update_redirect_endpoint(
    redirect_id: int,
    data: RedirectUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    """Admin: Update a redirect"""
    redirect = update_redirect(db, redirect_id, data)
    
    if not redirect:
        raise HTTPException(status_code=404, detail="Redirect not found")
    
    return redirect


@router.delete("/admin/redirects/{redirect_id}")
def delete_redirect_endpoint(
    redirect_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin)
):
    """Admin: Delete a redirect"""
    success = delete_redirect(db, redirect_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Redirect not found")
    
    return {"message": "Redirect deleted successfully"}