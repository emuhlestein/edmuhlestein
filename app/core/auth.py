from datetime import datetime, timedelta, timezone
from typing import Any, List, Optional, Annotated

import jwt
from jwt import PyJWTError
from fastapi import Depends, HTTPException, status, Request
from pydantic import ValidationError
from sqlalchemy.orm import Session

from .config import settings
from .security import oauth2_scheme, pwd_context
from ..database import get_db
from ..models.user import User
from ..schemas.token import TokenPayload  # Pydantic model for JWT payload


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate a secure hash for a password."""
    return pwd_context.hash(password)

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Verify user credentials and return the user object if valid.

    Returns:
        User object if email exists and password is correct and account is active
        None otherwise

    Raises:
        HTTPException: only in exceptional internal cases (rare)
    """
    # 1. Find user by email
    user = db.query(User).filter(User.email == email).first()

    # 2. No user → early return None (don't leak existence)
    if not user:
        return None

    # 3. Verify password
    if not pwd_context.verify(password, user.hashed_password):
        return None

    # 4. Check if account is active
    if not user.is_active:
        # You can raise here or return None depending on your preference
        # Returning None is more common → login fails silently
        return None

    # 5. All checks passed → return the user
    return user


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(
    subject: Any,
    expires_delta: Optional[timedelta] = None,
    extra_claims: Optional[dict[str, Any]] = None,
) -> str:
    """
    Create a new JWT access token.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = dict(extra_claims) if extra_claims else {}
    to_encode.update(
        {
            "sub": str(subject),
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            # Optional but recommended in production:
            # "iss": settings.PROJECT_NAME or "your-api",
            # "aud": "your-frontend-domain",
        }
    )

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def decode_access_token(token: str) -> TokenPayload:
    """
    Decode and validate JWT token → return payload.
    Raises credentials_exception on failure.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return TokenPayload(**payload)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValidationError):
        raise credentials_exception


# ────────────────────────────────────────────────
# Dependency: get current authenticated user
# ────────────────────────────────────────────────
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Returns the currently authenticated user.
    Validates JWT and fetches user from database.
    """
    token_data = decode_access_token(token)

    user = db.query(User).filter(User.id == int(token_data.sub)).first()
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    return user


# ────────────────────────────────────────────────
# Optional: Role-based access control helper
# ────────────────────────────────────────────────
def require_roles(required_roles: List[str]):
    """
    Dependency factory for role-based authorization.

    Example:
        @router.get("/admin")
        def admin_route(user: User = Depends(require_roles(["admin"]))):
            ...
    """
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return role_checker


def get_current_user_optional(
    request: Request,
    token: Annotated[str | None, Depends(oauth2_scheme)] = None,
    db: Session = Depends(get_db)
) -> Optional[User]:
    if not token:
        # Try cookie fallback
        cookie_token = request.cookies.get("access_token")
        if cookie_token and cookie_token.startswith("Bearer "):
            token = cookie_token[7:]
        else:
            return None

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            return None
    except PyJWTError:
        return None

    user = db.query(User).filter(User.email == email).first()
    return user