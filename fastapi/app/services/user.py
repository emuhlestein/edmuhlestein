from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User
from ..schemas.user import UserCreate
from ..core.security import get_password_hash


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    existing_user = await get_user_by_email(db, user_in.email)
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
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def user_exists(
    db: AsyncSession,
    *,
    email: str | None = None,
    username: str | None = None,
    user_id: int | None = None,
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
    elif username:
        stmt = stmt.where(User.username == username)
    elif user_id:
        stmt = stmt.where(User.id == user_id)

    result = await db.execute(stmt)
    return result.scalar() is not None