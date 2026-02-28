from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict, field_validator, Field

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: Optional[str] = "user"

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[bool] = None

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: Optional[datetime]


class RegisterForm(BaseModel):
    """
    Pydantic model for user registration form input.
    
    Used both for:
    - HTML form submission (with Form data)
    - JSON API registration endpoint (if you add one later)
    """
    email: EmailStr = Field(
        ...,
        description="User's email address (must be valid)",
        examples=["user@example.com"]
    )
    
    password: str = Field(
        ...,
        min_length=8,
        description="User's password (minimum 8 characters)",
        examples=["SecurePass123!"]
    )
    
    password_confirm: str = Field(
        ...,
        description="Must match the password field",
        examples=["SecurePass123!"]
    )
    
    # Optional fields – uncomment/add as needed
    # username: Optional[str] = Field(
    #     None,
    #     min_length=3,
    #     max_length=30,
    #     pattern=r"^[a-zA-Z0-9_-]+$",
    #     description="Unique username (letters, numbers, underscore, hyphen)",
    #     examples=["ed123"]
    # )
    
    # accept_terms: bool = Field(
    #     ...,
    #     description="User must accept terms of service",
    #     examples=[True]
    # )

    # ────────────────────────────────────────────────
    # Cross-field validation: passwords must match
    # ────────────────────────────────────────────────
    @field_validator("password_confirm")
    @classmethod
    def passwords_must_match(cls, v: str, info) -> str:
        password = info.data.get("password")
        if password is not None and v != password:
            raise ValueError("Passwords do not match")
        return v

    # ────────────────────────────────────────────────
    # Optional: extra password strength rules
    # ────────────────────────────────────────────────
    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        # You can add more rules (special characters, length patterns, etc.)
        return v

    model_config = {
        "extra": "forbid",          # reject any unknown fields
        "str_strip_whitespace": True,
        "json_schema_extra": {
            "examples": [
                {
                    "email": "ed@example.com",
                    "password": "MySecurePass2026!",
                    "password_confirm": "MySecurePass2026!",
                    # "username": "ed_saltlake",
                    # "accept_terms": true
                }
            ]
        }
    }


# Optional: Response schema after successful registration
class RegisterResponse(BaseModel):
    message: str = "Registration successful"
    email: EmailStr
    # You usually do NOT return the password or token here
    # (token goes in cookie or separate field if API-style)