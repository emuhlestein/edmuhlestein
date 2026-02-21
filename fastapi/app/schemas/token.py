# app/schemas/token.py
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: int
    iat: int
    # Add any other claims you use
    role: str | None = None
    # iss: str | None = None
    # aud: str | None = None