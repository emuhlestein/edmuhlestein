from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    root_router,
    auth_router,
)

app = FastAPI(debug=True)
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

app.include_router(root_router)
app.include_router(auth_router)



# @app.get("/health")
# def health():
#     return {"status": "ok"}

# @app.get("/hello")
# def hello():
#     return {"message": "Hello from FastAPI!"}