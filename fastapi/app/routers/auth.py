from pathlib import Path
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="/app/app/templates")
router = APIRouter(prefix="/auth", tags=["auth"])
# router = APIRouter(tags=["auth"])

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, error: str = None):
    try:
        return templates.TemplateResponse("login.html", {"request": request, "error": error})
    except Exception as e:
        return HTMLResponse(content=f"Template Error: {str(e)}", status_code=500)

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request, error: str = None):
    return templates.TemplateResponse("register.html", {"request": request, "error": error})

# POST handlers would go here (with actual user creation/login logic)