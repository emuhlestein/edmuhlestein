from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

# ────────────────────────────────────────────────
# Password hashing
# ────────────────────────────────────────────────
pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto",
    argon2__time_cost=2,
    argon2__memory_cost=102400,
    argon2__parallelism=8,
)

# ────────────────────────────────────────────────
# JWT handling
# ────────────────────────────────────────────────
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login",
    scheme_name="JWT",
    description="JWT Authorization header using the Bearer scheme.",
)