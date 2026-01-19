from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import engine  # sync engine (sqlalchemy.create_engine)
from models.base import Base   # DeclarativeBase subclass
from routers import root_router, auth_router

app = FastAPI(debug=True)
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

app.include_router(root_router)
app.include_router(auth_router)

@app.on_event("startup")
def on_startup():
    # Create tables if they don't exist (in production use Alembic migrations!)
    Base.metadata.create_all(bind=engine)
