from datetime import datetime, timedelta, timezone
from typing import Any

import jwt  # or from jose import jwt if using python-jose

from core.config import settings  # assuming settings has SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(
    subject: Any,                           # user.id, user.email, or any unique identifier
    expires_delta: timedelta | None = None,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    """
    Create a signed JWT access token.

    Args:
        subject: The unique identifier for the token subject (usually user ID or email)
        expires_delta: Optional custom expiration delta
        extra_claims: Optional additional claims to include

    Returns:
        Signed JWT string
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # Avoid mutating the input dict
    to_encode = dict(extra_claims) if extra_claims else {}
    to_encode.update(
        {
            "sub": str(subject),                    # always coerce to string
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            # Recommended additions (optional but useful in production)
            # "iss": settings.TOKEN_ISSUER,         # e.g. "https://api.yourdomain.com"
            # "aud": settings.TOKEN_AUDIENCE,       # e.g. "your-frontend-domain"
        }
    )

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt