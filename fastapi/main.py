from fastapi import FastAPI
from app.routers import (
    root_router,
)

app = FastAPI()

app.include_router(root_router)

# @app.get("/health")
# def health():
#     return {"status": "ok"}

# @app.get("/hello")
# def hello():
#     return {"message": "Hello from FastAPI!"}