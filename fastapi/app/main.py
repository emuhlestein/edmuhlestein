from fastapi import FastAPI
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from routers import (
    root_router,
    auth_router,
)

app = FastAPI(debug=True)
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

app.include_router(root_router)
app.include_router(auth_router)

DATABASE_URL = os.getenv("DATABASE_URL")
# engine = engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@app.on_event("startup")
async def on_startup():
    # Create tables if they don't exist (in production use Alembic migrations!)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
