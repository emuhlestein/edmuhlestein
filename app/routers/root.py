from typing import Optional
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, timezone
from ..core.utils import is_likely_browser, render_template
from ..core.auth import get_current_user_optional
from ..models.user import User

router = APIRouter(tags=["root"])

@router.get("/", response_class=HTMLResponse, summary="Home page")
def read_root(
    request: Request,
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    current_utc = datetime.now(timezone.utc)

    return render_template(
        "index.html",
        request,
        title="FastAPI Task Manager",
        app_name="Task Manager API",
        message="Welcome to the FastAPI Task Manager API! 👋",
        version="1.0.0",
        current_time=current_utc.strftime("%Y-%m-%d %H:%M:%S UTC"),
        current_year=current_utc.year,
        current_user=current_user,
    )

@router.get("/health", summary="Health check for monitoring")
def health_check():
    """
    Lightweight health check endpoint.
    Used by load balancers, Kubernetes, Docker, monitoring tools, etc.
    Returns 200 OK if the service is healthy.
    """
    return JSONResponse(status_code=200, content={"status": "healthy"})


@router.get("/hello", summary="Basic welcome")
def hello():
    """hellohealth check endpoint.
    Used by load balancers, Kubernetes, Docker, monitoring tools, etc.
    Returns 200 OK if the service is healthy.
    """
    return JSONResponse(status_code=200, content={"status": "Hello from FastAPI! using a router"})