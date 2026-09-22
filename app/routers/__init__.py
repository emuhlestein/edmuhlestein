
from .root import router as root_router
from .auth import router as auth_router
from .about import router as about_router

__all__ = [
    "root_router",
    "auth_router",
    "about_router",
]