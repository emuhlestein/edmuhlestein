
from .root import router as root_router
from .auth import router as auth_router
from .about import router as about_router
from .project import router as project_router
from .therapists import router as therapists_router

__all__ = [
    "root_router",
    "auth_router",
    "about_router",
    "project_router",
    "therapists_router",
]