from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated

from ..core.auth import authenticate_user, create_access_token, get_password_hash, verify_password
from ..core.config import settings
from ..core.utils import is_likely_browser
from ..database import get_db
from ..services.user import get_user_by_email, create_user  # your CRUD functions
from ..schemas.user import UserCreate  # your Pydantic model for registration
from ..schemas.user import RegisterForm
from ..models.user import User
from ..schemas.token import Token

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/auth", tags=["auth"])

# Show the login form
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, error: str = None):
    """
    GET /auth/login
    - Full page when loaded directly
    - Only the form fragment when requested via HTMX
    """
    context = {
        "request": request,
        "error": error,
        "email": request.query_params.get("email", ""),  # optional: pre-fill from query
    }


    # Check if request comes from HTMX
    is_htmx = request.headers.get("HX-Request") == "true"
    if is_htmx:
        # Return only the form + error partial
        return templates.TemplateResponse(
            "partials/login_form.html",  # ← new partial template
            context
        )
    else:
        # Full page for direct access / browser navigation
        try:
            return templates.TemplateResponse("login.html", {"request": request, "error": error})
        except Exception as e:
            return HTMLResponse(content=f"Template Error: {str(e)}", status_code=500)

@router.post("/login", response_model=Token)
def login(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, email=form_data.username, password=form_data.password)

    if user:
        # Success → redirect with cookie
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )
        response = RedirectResponse("/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(
            key="access_token",
            value=f"Bearer {token}",
            httponly=True,
            secure=False,          # True in production
            samesite="lax"
        )
        return response
    
    # Failure → return 200 + error HTML fragment
    # (HTMX will swap this into the target)
    context = {
        "request": request,
        "error": "Incorrect email or password. Please try again.",
        "email": form_data.username  # pre-fill
    }

    if is_likely_browser(request):
        # Browser → show form again with error (200 + HTML fragment)
        return templates.TemplateResponse(
            "partials/login_form.html",
            context,
            status_code=200
        )
    else:
        # API client → proper 401 JSON
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )


# Show registration form
@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request, error: str = None):
    return templates.TemplateResponse("register.html", {"request": request, "error": error})

@router.post("/register", response_class=HTMLResponse)
def register_post(
    request: Request,
    form_data: Annotated[RegisterForm, Form()],   # ← this line
    db: Session = Depends(get_db)
):

    """
    Handle registration form submission using a Pydantic model.
    """
    # 1. At this point, form_data is already validated by Pydantic
    #    → email is valid EmailStr
    #    → password >= 8 chars
    #    → passwords match

    # 2. Check if email already exists
    if get_user_by_email(db, email=form_data.email):
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": "Email already registered",
                "form_data": form_data.model_dump()  # preserve form values
            },
            status_code=400
        )

    # 3. Create new user
    try:
        user = create_user(
            db,
            email=form_data.email,
            password=form_data.password,   # plain password — hash inside create_user
            # username=... if you add it later
        )
    except Exception:
        # In real app: log the error
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": "An error occurred during registration. Please try again.",
                "form_data": form_data.model_dump()
            },
            status_code=500
        )

    # 4. Auto-login: create JWT
    access_token = create_access_token(
        subject=user.id,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        extra_claims={"role": user.role}
    )

    # 5. Redirect with secure cookie
    response = RedirectResponse(
        url="/dashboard",
        status_code=status.HTTP_303_SEE_OTHER
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,           # False only for local dev without HTTPS
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    return response