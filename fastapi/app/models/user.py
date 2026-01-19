from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base  # Or directly inherit from DeclarativeBase if in one file

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True) # PK is indexed implicitly
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Optional fields
    full_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    is_superuser: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now() # timezone-aware timestamps
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=func.now(), server_default=func.now() # timezone-aware timestamps
    )