from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas.user import UserCreate
from ..core.auth import get_password_hash


def get_user_by_email(db: Session, email: str) -> User | None:
    result = db.execute(select(User).where(User.email == email))
    return result.scalars().first()


def create_user(db: Session, user_in: UserCreate) -> User:
    existing_user = get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        full_name=user_in.full_name,
    )

    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered",
        )
    db.refresh(db_user)
    return db_user

def user_exists(
    db: Session,
    *,
    email: Optional[str] = None,
    username: Optional[str] = None,
    user_id: Optional[int] = None,
) -> bool:
    """
    Check if a user exists by email, username, or ID.
    Returns True if at least one matching user is found.
    
    Usage examples:
        await user_exists(db, email="user@example.com")
        await user_exists(db, username="johndoe")
        await user_exists(db, user_id=42)
    """
    if not any([email, username, user_id]):
        return False

    stmt = select(User.id).limit(1)  # we only need to know if it exists

    if email:
        stmt = stmt.where(User.email == email)
    if username:
        stmt = stmt.where(User.username == username)
    if user_id:
        stmt = stmt.where(User.id == user_id)

    result = db.execute(stmt)
    return result.scalars().first() is not None