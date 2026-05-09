from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.routes import auth_router

app = FastAPI(title="InclusiTrip API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


@app.get("/")
async def home():
    return FileResponse(FRONTEND_DIR / "welcome.html")


@app.get("/login")
async def login():
    return FileResponse(FRONTEND_DIR / "login.html")


@app.get("/create-account")
async def create_account():
    return FileResponse(FRONTEND_DIR / "create-account.html")
